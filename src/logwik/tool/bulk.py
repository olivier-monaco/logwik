import logging

from argparse import FileType
from sys import stdin

from ..engine import Worker
from ..engine.nginx import LogTooLongException

_logger = logging.getLogger(__name__)

def create_arg_parser(parent):
    subparser = parent.add_parser('bulk')
    subparser.add_argument('file', nargs='*', type=FileType('r'), default=None)
    subparser.set_defaults(handler=bulk)

def bulk(context):
    cnx = context.create_connection()
    cur = cnx.cursor()
    files = context.args.file
    if len(files) == 0:
        files = [stdin]
    worker = Worker()
    for file in files:
        _logger.info(f'Reading from {file.name}')
        worker.begin(cur)
        for line in file:
            try:
                worker.append(line)
            except LogTooLongException:
                logging.error('Too long log line, skipping: {}'.format(line))
            except:
                print(line)
                raise
            if worker.total % 10000 == 0:
                _logger.info(f'Done : {worker.total} lignes')
                worker.commit()
                worker.begin(cur)
        _logger.info(f'Done : {worker.total} lignes')
        worker.commit()
