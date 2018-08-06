"""
Module to manage services on the system.
"""

import logging
from os import system
from lego.brick import Brick
from lego.common import LegoException


class CommandBrick(Brick):  # pylint: disable=too-few-public-methods
    """
    Modles a command brick.
    """
    def __init__(self, provided_attributes):
        self.__logger = logging.getLogger('lego.brick_modules.command')
        self.__provided_attributes = provided_attributes
        self.__supported_attributes = self.__compulsory_attributes = [
            'type',
            'commands'
        ]
        super(CommandBrick, self).__init__(name='lego.brick_modules.command_brick',
                                           logger=self.__logger,
                                           provided_attributes=self.__provided_attributes,
                                           supported_attributes=self.__supported_attributes,
                                           compulsory_attributes=self.__compulsory_attributes)

    def manage_commands(self):
        """
        Manage a given set of commands.
        Args:
            attributes (dictionary): Attribute of the current running brick.
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        for each_command in self.__provided_attributes['commands']:
            self.__logger.info("Command `%s` will run on the system", each_command)
            return_code = system(each_command)
            if return_code != 0:
                raise LegoException(message="None 0 exit code `{0}` returned from "
                                            "command `{1}`".format(return_code, each_command))
