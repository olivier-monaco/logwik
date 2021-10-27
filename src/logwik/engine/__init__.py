from logging import getLogger
from math import trunc

from .nginx import extract as extract_nginx, LogTooLongException

_logger = getLogger(__name__)

def build_insert_or_update(table, key_columns, data_columns):
    columns = '`' + '`, `'.join(key_columns + data_columns) + '`'
    values = ', '.join(['?' for x in key_columns + data_columns])
    updates = ', '.join([f'`{x}` = `{x}` + VALUES(`{x}`)' for x in data_columns])
    return f'insert into `{table}` ({columns}) values ({values}) on duplicate key update {updates}'

class Resolver:
    def __init__(self, table, field):
        self._ins = f'insert ignore into `{table}` (`{field}`) values (?)'
        _logger.debug(f'Insert for resolver of {table}: {self._ins}')
        self._sel = f'select `id` from `{table}` where `{field}`= ?'
        _logger.debug(f'Select for resolver of {table}: {self._sel}')
        self._cache = {}
    
    def resolve(self, cursor, value):
        if value is None:
            return 0
        if value not in self._cache:
            cursor.execute(self._ins, (value,))
            cursor.execute(self._sel, (value,))
            row = cursor.fetchone()
            self._cache[value] = row[0]
        return self._cache[value]

class Resolvers:
    def __init__(self):
        self._resolvers = {
            'device': Resolver('device', 'name'),
            'domain': Resolver('domain', 'name'),
            'hosting': Resolver('hosting', 'name'),
            'os': Resolver('os', 'name'),
            'os_version': Resolver('os_version', 'version'),
            'responder': Resolver('responder', 'name'),
            'type': Resolver('type', 'name'),
            'ua': Resolver('ua', 'name'),
            'ua_version': Resolver('ua_version', 'version'),
            'verb': Resolver('verb', 'name'),
        }
    
    def resolve(self, cursor, type, value):
        return self._resolvers[type].resolve(cursor, value)

class Stat:
    def __init__(self, table):
        self._cache = {}
        self._lock  = f'lock table {table} write'
        self._insert = build_insert_or_update(
            table,
            ['date', 'hosting_id', 'domain_id', 'verb_id', 'responder_id', 'os_id',
            'os_version_id', 'ua_id', 'ua_version_id', 'device_id', 'type', 'status'],
            ['total_duration', 'delay_duration', 'responder_duration', 'number', 'bytes']
        )
        _logger.debug(f'Insert for statistics of {table}: {self._insert}')

    def add(self, record_key, record_data):
        if record_key in self._cache:
            self._cache[record_key] = (
                self._cache[record_key][0] + record_data[0],
                self._cache[record_key][1] + record_data[1],
                self._cache[record_key][2] + record_data[2],
                self._cache[record_key][3] + record_data[3],
                self._cache[record_key][4] + record_data[4],
            )
        else:
            self._cache[record_key] = record_data

    def flush(self, cursor):
        cursor.execute(self._lock)
        for key, data in self._cache.items():
            try:
                cursor.execute(self._insert, key + data)
            except:
                print(key, data)
                raise
        self._cache = {}
        cursor.execute('unlock table')

class Worker:
    def __init__(self):
        self._appended = 0
        self._total = 0
        self._resolvers = Resolvers()
        self._stat_day = Stat('access_day')
        self._stat_hour = Stat('access_hour')
        self._stat_quarter = Stat('access_quarter')
        self._stat_minute = Stat('access_minute')

    def resolve(self, type, value):
        return self._resolvers.resolve(
            self._cursor, type, value
        )

    def begin(self, cursor):
        self._appended = 0
        self._cursor = cursor

    def commit(self):
        _logger.info('Flushing statistics to database')
        self._stat_day.flush(self._cursor)
        self._stat_hour.flush(self._cursor)
        self._stat_quarter.flush(self._cursor)
        self._stat_minute.flush(self._cursor)
        self._cursor.execute('commit')
        self._cursor = None
        _logger.info('Statistics flushed')

    def append(self, line):
        log = extract_nginx(line)
        partial_key = (
            self.resolve('hosting', log['hosting']),
            self.resolve('domain', log['domain']),
            self.resolve('verb', log['verb']),
            self.resolve('responder', log['responder']['ip']),
            self.resolve('os', log['client']['os']['name']),
            self.resolve('os_version', log['client']['os']['version']),
            self.resolve('ua', log['client']['user_agent']['name']),
            self.resolve('ua_version', log['client']['user_agent']['version']),
            self.resolve('device', log['client']['device']),
            log['type'] if log['type'] is not None else '',
            log['status'],
        )
        response_time = log['responder']['response_time']
        if response_time is None:
            response_time = 0
        delay = log['duration'] - response_time
        if delay < 0:
            delay = 0
        record_data = (
            log['duration'],
            delay,
            response_time,
            1,
            int(log['size']),
        )
        # ex. 2021-10-19T03:04:05
        self._stat_day.add(
            (log["date"][:10],) + partial_key,
            record_data
        )
        self._stat_hour.add(
            (f'{log["date"][:10]} {log["date"][11:13]}:00:00',) + partial_key,
            record_data
        )
        quarter = trunc(int(log["date"][14:16]) / 15) * 15
        self._stat_quarter.add(
            (f'{log["date"][:10]} {log["date"][11:13]}:{quarter:02d}:00',) + partial_key,
            record_data
        )
        self._stat_minute.add(
            (f'{log["date"][:10]} {log["date"][11:16]}:00',) + partial_key,
            record_data
        )
        self._appended += 1
        self._total += 1

    @property
    def appended(self):
        return self._appended

    @property
    def total(self):
        return self._total
