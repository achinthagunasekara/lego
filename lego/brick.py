"""
Brick modle and related items.
"""


from lego.common import LegoException


class Brick(object):  # pylint: disable=too-few-public-methods
    """
    Models a brick object.
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 name,
                 logger,
                 provided_attributes,
                 supported_attributes,
                 compulsory_attributes):
        self.__name = name
        self.__logger = logger
        self.__provided_attributes = provided_attributes
        self.__supported_attributes = supported_attributes
        self.__compulsory_attributes = compulsory_attributes
        self.__logger.info("Validating provided main attributes for the brick `%s`", name)
        if not self.__validate_attributes():
            raise LegoException(message='Attribute validation failed')

    def __validate_attributes(self):
        """
        Manage packages on the system with given details.
        Args:
            self.__provided_attributes (list): List of attributes provided by the user.
            self.__supported_attributes (list): List of supported attributes by the module.
            self.__compulsory_attributes (list): List of compulsory attributes.
        Returns:
            bool: True if the input is valid, false otherwise.
        Raises:
            None
        """
        self.__logger.debug("Validating self.__provided_attributes %s "
                            "with self.__supported_attributes `%s` "
                            "and self.__compulsory_attributes `%s`",
                            self.__provided_attributes, self.__supported_attributes,
                            self.__compulsory_attributes)
        for provided_attribute in self.__provided_attributes:
            if provided_attribute not in self.__supported_attributes:
                self.__logger.error("Unknown attribute `%s`. Supported attributes are `%s`",
                                    provided_attribute, self.__supported_attributes)
                return False
        for compulsory_attribute in self.__compulsory_attributes:
            if compulsory_attribute not in self.__provided_attributes:
                self.__logger.error("Compulsory attribute `%s` is not provided",
                                    compulsory_attribute)
                return False
        return True
