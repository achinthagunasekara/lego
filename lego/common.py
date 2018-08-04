"""
Shared functions and classes for the Lego configuration management tool.
"""

import logging


class LegoException(Exception):
    """
    Custom LegoException specific to Lego configuration management tool.
    """

    def __init__(self, message):  # pylint: disable=super-init-not-called
        self.__message = message

    def __str__(self):
        return repr(self.__message)


def validate_attributes(provided_attributes, supported_attributes, compulsory_attributes):
    """
    Manage packages on the system with given details.
    Args:
        provided_attributes (list): List of attributes provided by the user.
        supported_attributes (list): List of supported attributes by the module.
        compulsory_attributes (list): List of compulsory attributes that must be provided.
    Returns:
        bool: True if the input is valid, false otherwise.
    Raises:
        None
    """
    logger = logging.getLogger('lego.common.validate')
    logger.debug("Validating provided_attributes %s with supported_attributes `%s` "
                 "and compulsory_attributes `%s`",
                 provided_attributes, supported_attributes, compulsory_attributes)
    for provided_attribute in provided_attributes:
        if provided_attribute not in supported_attributes:
            logger.error("Unknown attribute `%s`. Supported attributes are `%s`",
                         provided_attribute, supported_attributes)
            return False
    for compulsory_attribute in compulsory_attributes:
        if compulsory_attribute not in provided_attributes:
            logger.error("Compulsory attribute `%s` is not provided", compulsory_attribute)
            return False
    return True
