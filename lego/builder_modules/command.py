"""
Module to manage services on the system.
"""

import logging
from lego.common import LegoException, validate_attributes


SUPPORTED_ATTRIBUTES = COMPULSORY_ATTRIBUTE = [
    'type',
    'commands'
]


def manage_commands(attributes):
    """
    Manage a given set of commands.
    Args:
        attributes (dictionary): Attribute of the current running brick.
    Returns:
        None
    Raises:
        LegoException: Raises LegoException.
    """
    logger = logging.getLogger('lego.builder_modules.services.manage_services')
    if not validate_attributes(provided_attributes=attributes.keys(),
                               supported_attributes=SUPPORTED_ATTRIBUTES,
                               compulsory_attributes=COMPULSORY_ATTRIBUTE):
        raise LegoException(message='Attribute validation failed')
    for each_command in attributes['commands']:
        logger.info("Command `%s` will run on the system", each_command)
