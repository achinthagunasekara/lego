"""
Shared functions and classes for the Lego configuration management tool.
"""

class LegoException(Exception):
    """
    Custom LegoException specific to Lego configuration management tool.
    """

    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return repr(self.__message)
