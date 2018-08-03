"""
Module to manage packges on a system and it's supporting modules.
"""

class PackageManager(object):
    """
    Module for managing packages on a system.
    """

    SUPPORTED_PACKAGE_MANAGERS = [
        'apt'
    ]

    def __init__(self, package_info):
        self.__package_info = package_info
