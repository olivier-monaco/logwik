import re

from base64 import b85encode, b64encode
from binascii import crc32
from hashlib import md5
from logging import getLogger
from socket import gethostbyaddr, herror
from ua_parser import user_agent_parser

from .mimetype import get_category
from .useragent import get_infos


_logger = getLogger(__name__)

_MATCHER = re.compile(r"""
    ^
    (?P<server_name>\S+)\s
    (?P<host>.+?)\s
    (?P<remote_addr>[0-9.:]+)\s
    (?P<remote_port>[0-9]+)\s
    (?P<remote_user>.+?)\s
    \[(?P<date>[^\]]+)\]\s
    (?:(?P<request_id>[a-f0-9]+)\s)?
    "(?P<request>
        (?P<verb>\S+)\s(?P<request_uri>.+?)\sHTTP/(?P<http_version>[0-9.]+)
    |
        (?:[^"]|\\")*
    )"\s
    (?P<status>[0-9]{3})\s
    (?P<size>[0-9]+|-)\s
    "(?P<referer>(?:[^"]|\\")*?)"\s
    "(?P<useragent>(?:[^"]|\\")*?)"\s
    (?:(?P<hostname>\S+)\s)?
    (?P<duration>[0-9.]+)\s
    (?P<gzip_ratio>[0-9.]+|-)\s
    "(?P<mimetype>(?:[^"]|\\")+?)"\s
    (?P<responder>\S+)(?:,\s\S+)*\s
    (?P<responder_status>[0-9]{3}|-)(?:,\s\S+)*\s
    (?P<responder_connect_time>[0-9.]+|-)(?:,\s\S+)*\s
    (?P<responder_header_time>[0-9.]+|-)(?:,\s\S+)*\s
    (?P<responder_response_time>[0-9.]+|-)(?:,\s\S+)*\s
    $
""", re.VERBOSE)

_RESPONDER_MATCHER = re.compile(r'^[0-9.]+:[0-9]+$')

def _is_empty(value):
    return value is None or value in ('-', '')

class InvalidVersionValueException(Exception):
    def __init__(self, message, type, value):
        super().__init__(message)
        self.message = message
        self.type = type
        self.value = value

def _build_client_part(m):
    ip = m['remote_addr']
    ua = get_infos(m['useragent'])
    return {
        'ip': ip,
        'port': m['remote_port'],
        'user_agent': ua['user_agent'],
        'os': ua['os'],
        'device': ua['device'],
    }

def _build_responder_part(m):
    if _is_empty(m['responder']):
        return {
            'ip': None,
            'host': None,
            'status': None,
            'connect_time': None,
            'header_time': None,
            'response_time': None,
        }
    if not _RESPONDER_MATCHER.match(m['responder']):
        return {
            'ip': None,
            'host': m['responder'],
            'status': int(m['responder_status'])
                if not _is_empty(m['responder_status']) else None,
            'connect_time': None,
            'header_time': None,
            'response_time': None,
        }
    ip = m['responder'].split(':')[0]
    try:
        host = gethostbyaddr(ip)[0]
    except herror:
        host = None
    return {
        'ip': ip,
        'host': host,
        'status': int(m['responder_status'])
            if not _is_empty(m['responder_status']) else None,
        'connect_time': float(m['responder_connect_time'])
             if not _is_empty(m['responder_connect_time']) else None,
        'header_time': float(m['responder_header_time'])
             if not _is_empty(m['responder_header_time']) else None,
        'response_time': float(m['responder_response_time'])
             if not _is_empty(m['responder_response_time']) else None,
    }    

class InvalidLogException(Exception):
    pass

class LogTooLongException(Exception):
    pass

def extract(log):
    if len(log) >= 4096:
        raise LogTooLongException
    m = _MATCHER.match(log)
    if not m:
        _logger.error('Invalid log: {}'.format(log))
        raise InvalidLogException
    doc = {
        # Request
        'request_id': m['request_id'],
        'hosting': m['server_name'].lower(),
        'domain': m['host'].lower(),
        'date': m['date'],
        'verb': None if m['verb'] is None else m['verb'].lower(),
        # Client
        'client': _build_client_part(m),
        # Processing
        'duration': float(m['duration']),
        # Response
        'status': int(m['status']),
        'type': get_category(m['mimetype']),
        'size': m['size'],
        # Responder
        'responder': _build_responder_part(m),
    }

    if m['referer'] != '-':
        doc['referer'] = m['referer']

    return doc
