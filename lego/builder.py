"""
Lego Builder.
"""


import yaml
from lego.common import LegoException


class Builder(object):
    """
    Builder for Lego tool.
    """

    def __init__(self, builder_file):
        self.__builder_file = builder_file
        self.__builder_instructions = self.__load()

    @property
    def builder_instructions(self):
        """
        Return builder instructions property.
        Args:
            None
        Returns:
            dictionary: Builder instructions dictionary.
        """
        return self.__builder_instructions

    def __load(self):
        """
        This function loads and validates the given builder file.
        Args:
            None
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        with open(self.__builder_file, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as yaml_ex:
                raise LegoException(message="Something went wrong "
                                            "while loading the builder file {0}".format(yaml_ex))
