"""
Lego Builder.
"""

import logging
import oyaml as yaml
from lego.common import LegoException
from lego.brick_modules.packages import PackageBrick
from lego.brick_modules.files import FileBrick
from lego.brick_modules.command import CommandBrick


class Builder(object):
    """
    Builder for Lego tool.
    """

    supported_modules = [
        'package',
        'file',
        'command'
    ]

    def __init__(self, builder_file):
        self.__logger = logging.getLogger('lego.builder.Builder')
        self.__builder_file = builder_file
        self.__brick_sets = {}
        self.__load_bricks()

    @property
    def brick_sets(self):
        """
        Return builder instructions property.
        Args:
            None
        Returns:
            dictionary: Builder instructions dictionary.
        Raises:
            None
        """
        return self.__brick_sets

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
                raise LegoException("Something went wrong while loading "
                                    "the builder file with error {0}".format(yaml_ex))
            except KeyError:
                raise LegoException("Builder file is missing `brick_sets`")

        for each_brick_set in brick_sets:
            self.__logger.debug("Loading brick set %s", each_brick_set)

            with open("brick_sets/{0}/bricks.yaml".format(each_brick_set), 'r') as stream:
                try:
                    self.__brick_sets[each_brick_set] = yaml.load(stream)
                except yaml.YAMLError as yaml_ex:
                    raise LegoException("Something went wrong while loading "
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
            LegoException: Raises LegoException.
        """
        for brick_set_name, brick_set in self.__brick_sets.items():
            self.__logger.info("Running brick set `%s`", brick_set_name)

            for brick_name, brick_details in brick_set.items():

                self.__logger.info("Running brick `%s`", brick_name)

                if brick_details['type'] == 'package':
                    brick = PackageBrick(provided_attributes=brick_details)
                elif brick_details['type'] == 'file':
                    brick = FileBrick(brick_set_name=brick_set_name,
                                      provided_attributes=brick_details)
                elif brick_details['type'] == 'command':
                    brick = CommandBrick(provided_attributes=brick_details)
                else:
                    raise LegoException("Unknown brick type `{0}`. Only brick types {1} "
                                        "are supported".format(brick_details['type'],
                                                               self.supported_modules))

                brick.run_brick()
