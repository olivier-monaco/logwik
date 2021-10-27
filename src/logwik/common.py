import logging
import mariadb

from argparse import ArgumentParser
from os.path import isdir, isfile, realpath
from yaml import load as load_yaml, SafeLoader

from . import ExitException
from .version import __version__


from sys import stderr, stdout

_logger = logging.getLogger(__name__)

class Context:
    def __init__(self, args, config):
        self._args = args
        self._config = config

    def create_connection(self):
        config = self.config
        return mariadb.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['name'],
        )

    @property
    def config(self):
        return self._config

    @property
    def args(self):
        return self._args

def create_base_arg_parser():
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', default='/etc/logwik/logwik.conf',
                        help='Increase verbosity')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Increase verbosity')
    parser.add_argument('--quiet', '-q', action='count', default=0,
                        help='Decrease verbosity')
    parser.add_argument('--version', '-V', action='version', version=__version__,
                        help='Increase verbosity')
    return parser

def create_context(args):
    config = load_config(args.config)
    context = Context(args, config)
    return context

def init_logging(args, force_stderr=False):
    verbosity = args.verbose - args.quiet
    if verbosity < 0:
        level = logging.ERROR
    elif verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    elif verbosity == 2:
        level = logging.DEBUG
    else:
        level = logging.NOTSET

    format = '%(asctime)s\t%(levelname)s\t%(message)s'
    formatter = logging.Formatter(format)

    handler = logging.StreamHandler(
        stderr if force_stderr else stdout
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(level)

def load_config(filename):
    if not isfile(filename):
        _logger.error('Missing configuration file "{0}"'.format(filename))
        raise ExitException(1)
    with open(filename) as f:
        config = load_yaml(f.read(), SafeLoader)
    if 'database' not in config:
        _logger.error('Missing database parameters in config file')
        raise ExitException(1)
    if 'host' not in config['database']:
        _logger.error('Missing database hostname in config file')
        raise ExitException(1)
    if 'user' not in config['database']:
        _logger.error('Missing database user in config file')
        raise ExitException(1)
    if 'password' not in config['database']:
        _logger.error('Missing database password in config file')
        raise ExitException(1)
    if 'name' not in config['database']:
        _logger.error('Missing database name in config file')
        raise ExitException(1)
    return config
