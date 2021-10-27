import logging

from argparse import ArgumentParser
from logwik import ExitException

from logwik.common import init_logging

from .. import ExitException
from .bulk import create_arg_parser as bulk_parser
from ..common import create_base_arg_parser, create_context, init_logging

_logger = logging.getLogger(__name__)

def build_arg_parser():
    parser = create_base_arg_parser()
    subs = parser.add_subparsers()
    bulk_parser(subs)
    return parser

def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    init_logging(args)

    if 'handler' not in args:
        parser.print_help()
        return 1

    try:
        context = create_context(args)
        return args.handler(context)
    except ExitException as e:
        return e.code
