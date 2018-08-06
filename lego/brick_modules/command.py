"""
Module to manage services on the system.
"""


from os import system
from lego.brick import Brick
from lego.common import LegoException


class CommandBrick(Brick):  # pylint: disable=too-few-public-methods
    """
    Modles a command brick.
    """

    supported_attributes = compulsory_attributes = [
        'type',
        'commands'
    ]

    def __init__(self, provided_attributes):
        self.provided_attributes = provided_attributes
        super(CommandBrick, self).__init__(name='command_brick',
                                           provided_attributes=self.provided_attributes,
                                           supported_attributes=CommandBrick.supported_attributes,
                                           compulsory_attributes=CommandBrick.compulsory_attributes)

    def run_brick(self):
        """
        Manage a given set of commands.
        Args:
            None
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        for each_command in self.provided_attributes['commands']:
            self.logger.info("Command `%s` will run on the system", each_command)
            return_code = system(each_command)
            if return_code != 0:
                raise LegoException("None 0 exit code `{0}` returned from "
                                    "command `{1}`".format(return_code, each_command))
