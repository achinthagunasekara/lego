"""
Executable for Lego configuration management tool.
"""

import sys
import logging
from lego.builder import Builder


SUPPORTED_COMMANDS = [
    'build'
]


def lego_help():
    """
    Print help text for the executable.
    Args:
        None
    Returns:
        None
    Raises:
        None
    """
    help_text = ('Lego Configuration Management Tool\n'
                 '\n'
                 'You must use one of the following supported commands.\n'
                 '\n'
                 'Currently Supported Commands\n'
                 '============================\n'
                 '* build\n'
                 '\n'
                 'Options for Supported Commands\n'
                 '==============================\n'
                 '\n'
                 'build\n'
                 '-----\n'
                 'build command must be followed by a builder file.\n'
                 'Please refer to the tool documentation for builder file syntax\n')
    print(help_text)  # pylint: disable=superfluous-parens


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

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2 or sys.argv[1] not in SUPPORTED_COMMANDS:
        lego_help()
        sys.exit(1)

    if sys.argv[1] == 'build':
        if len(sys.argv) < 3:
            lego_help()
            sys.exit(1)
        builder = Builder(builder_file=sys.argv[2])
        builder.build()
