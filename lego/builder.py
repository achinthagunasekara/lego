"""
Lego Builder.
"""

import logging
import yaml
from lego.common import LegoException
from lego.builder_modules.packages import manage_packages


class Builder(object):
    """
    Builder for Lego tool.
    """

    __supported_modules = [
        'package',
        'service',
        'file'
    ]

    def __init__(self, builder_file):
        self.__logger = logging.getLogger('Builder')
        self.__builder_file = builder_file
        self.__bricks = {}
        self.__load_bricks()

    @property
    def bricks(self):
        """
        Return builder instructions property.
        Args:
            None
        Returns:
            dictionary: Builder instructions dictionary.
        """
        return self.__bricks

    def __load_bricks(self):
        """
        This function loads and validates the given builder file.
        Args:
            None
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        self.__logger.debug("Loading builder file %s", self.__builder_file)

        with open(self.__builder_file, 'r') as stream:
            try:
                brick_sets = yaml.load(stream)['brick_sets']
            except yaml.YAMLError as yaml_ex:
                raise LegoException(message="Something went wrong while loading "
                                            "the builder file with error {0}".format(yaml_ex))
            except KeyError:
                raise LegoException(message="Builder file is missing `brick_sets`")

        for each_brick_set in brick_sets:
            self.__logger.debug("Loading brick set %s", each_brick_set)

            with open("brick_sets/{0}/bricks.yaml".format(each_brick_set), 'r') as stream:
                try:
                    self.__bricks.update(yaml.load(stream))
                except yaml.YAMLError as yaml_ex:
                    raise LegoException(message="Something went wrong while loading "
                                                "brick set `{0}` the builder file with "
                                                "error {1}".format(each_brick_set, yaml_ex))

    def build(self):
        """
        Run module to handle each brick.
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        for brick_name, brick_details in self.__bricks.items():

            self.__logger.info("Running brick `%s`", brick_name)

            if brick_details['type'] not in self.__supported_modules:
                raise LegoException(message="Unknown brick type `{0}`. Only brick types {1} "
                                            "are supported".format(brick_details['type'],
                                                                   self.__supported_modules))

            if brick_details['type'] == 'package':
                manage_packages(attributes=brick_details)
