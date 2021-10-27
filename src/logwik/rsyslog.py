import logging

from sys import stdout, stderr, stdin

from . import ExitException
from .common import create_base_arg_parser, create_context, init_logging
from .engine import Worker
from .version import __version__

_logger = logging.getLogger(__name__)

def main():
    parser = create_base_arg_parser()
    args = parser.parse_args()

    init_logging(args, True)

    try:
        context = create_context(args)
        return loop(context)
    except ExitException as e:
        return e.code

def loop(context):
    cnx = context.create_connection()
    cursor = cnx.cursor()
    worker = Worker()

    worker.begin(cursor)
    in_transaction = False
    _logger.info('logwik-rslg ready.')
    stdout.write('OK\n')
    stdout.flush()
    for line in stdin:
        if line == 'BEGIN TRANSACTION\n':
            if in_transaction:
                raise Exception('Transaction already begun')
            worker.begin(cursor)
            in_transaction = True
            _logger.info('Starting transaction.')
            stdout.write('OK\n')
            stdout.flush()
        elif line == 'COMMIT TRANSACTION\n':
            if not in_transaction:
                raise Exception('Not in a transation')
            worker.commit()
            in_transaction = False
            _logger.info(f'Ending transaction ({worker.appended} lines).')
            stdout.write('OK\n')
            stdout.flush()
        else:
            if not in_transaction:
                raise Exception('Not in a transaction')
            _logger.debug(f'New line: {line}')
            worker.append(line)
            stdout.write('DEFER_COMMIT\n')
            stdout.flush()
