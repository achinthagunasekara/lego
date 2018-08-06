"""
Executable for Lego configuration management tool.
"""


import sys
import logging
import argparse
from lego.builder import Builder
from lego.common import LegoException


SUPPORTED_COMMANDS = [
    'build'
]

def main():
    """
    Main function to run the Lego executable.
    Args:
        None
    Returns:
        None
    Raises:
        None
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', default=argparse.SUPPRESS,
                        help="Action to preform. Currently supported actions "
                        "are {0}".format(SUPPORTED_COMMANDS))
    parser.add_argument('--action', dest='action', default=None,
                        help="Action to preform. Currently supported actions "
                        "are {0}".format(SUPPORTED_COMMANDS))
    parser.add_argument('builder_file', nargs='?', default=argparse.SUPPRESS,
                        help="Builder file to run")
    parser.add_argument('--builder_file', dest='builder_file', default=None,
                        help="Builder file to run")
    parser.add_argument('--debug', default=False, action='store_true',
                        help="Print debugging logs as well")
    args = parser.parse_args()

    print args

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('lego.executable.main')


    if args.action not in SUPPORTED_COMMANDS:
        parser.print_help()
        sys.exit(1)

    if args.action == 'build':
        if not args.builder_file:
            parser.print_help()
            sys.exit(1)
        try:
            builder = Builder(builder_file=sys.argv[2])
            builder.build()
        except LegoException as lego_ex:
            logger.error("Something went wrong while running `lego build` with error %s", lego_ex)
        except Exception as ex:  # pylint: disable=broad-except
            logger.error("Something badly went wrong while running 'lego build` with error %s", ex)
