"""
Brick modle and related items.
"""


import logging
from lego.common import LegoException


class Brick(object):  # pylint: disable=too-few-public-methods
    """
    Models a brick object.
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 name,
                 provided_attributes,
                 supported_attributes,
                 compulsory_attributes):
        self.name = name
        self.logger = logging.getLogger("lego.brick_modules.package_brick.{0}".format(name))
        self.provided_attributes = provided_attributes
        self.supported_attributes = supported_attributes
        self.compulsory_attributes = compulsory_attributes
        self.logger.info("Validating provided main attributes for the brick `%s`", name)
        if not self.__validate_attributes():
            raise LegoException('Attribute validation failed')

    def __validate_attributes(self):
        """
        Manage packages on the system with given details.
        Args:
            None
        Returns:
            bool: True if the input is valid, false otherwise.
        Raises:
            None
        """
        self.logger.debug("Validating provided_attributes %s "
                          "with supported_attributes `%s` "
                          "and compulsory_attributes `%s`",
                          self.provided_attributes, self.supported_attributes,
                          self.compulsory_attributes)
        for provided_attribute in self.provided_attributes:
            if provided_attribute not in self.supported_attributes:
                self.logger.error("Unknown attribute `%s`. Supported attributes are `%s`",
                                  provided_attribute, self.supported_attributes)
                return False
        for compulsory_attribute in self.compulsory_attributes:
            if compulsory_attribute not in self.provided_attributes:
                self.logger.error("Compulsory attribute `%s` is not provided",
                                  compulsory_attribute)
                return False
        return True

    def __run_setup(self):
        """
        Do any setup work needed by bricks.
        If needed must be overwritten by the subclasses.
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        pass

    def run_brick(self):
        """
        Run this brick.
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        pass
