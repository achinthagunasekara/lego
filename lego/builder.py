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
        self.__builder_instructions = {}
        self.__load_builder_instructions()

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

    def __load_builder_instructions(self):
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
                brick_sets = yaml.load(stream)['brick_sets']
            except yaml.YAMLError as yaml_ex:
                raise LegoException(message="Something went wrong while loading "
                                            "the builder file with error {0}".format(yaml_ex))
            except KeyError:
                raise LegoException(message="Builder file is missing `brick_sets`")

        for each_brick_set in brick_sets:
            with open("brick_sets/{0}/bricks.yaml".format(each_brick_set), 'r') as stream:
                try:
                    self.__builder_instructions.update(yaml.load(stream))
                except yaml.YAMLError as yaml_ex:
                    raise LegoException(message="Something went wrong while loading "
                                                "brick set `{0}` the builder file with "
                                                "error {1}".format(each_brick_set, yaml_ex))
