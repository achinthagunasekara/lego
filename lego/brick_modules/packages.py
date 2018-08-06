"""
Module to manage packges on a system and it's supporting modules.
"""

import logging
from lego.brick import Brick
from lego.common import LegoException


class PackageManager(object):  # pylint: disable=too-few-public-methods
    """
    Generic package manager object.
    """

    def __init__(self):
        pass

    def __setup(self):
        pass

    def install(self, package):
        """
        Install a package.
        Args:
            package: Name of the package to install.
        Returns:
            None
        Raises:
            None
        """
        pass


class AptPackageManager(PackageManager):
    """
    Apt package manager object.
    """
    def __init__(self):
        super(AptPackageManager, self).__init__()
        self.__logger = logging.getLogger('lego.builder_modules.packages.AptPackage')
        self.__setup()

    def __setup(self):
        import apt
        self.__cache = apt.cache.Cache()
        self.__cache.update()
        self.__cache.open()

    def install(self, package):
        """
        Install a package.
        Args:
            package: Name of the package to install.
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        try:
            apt_package = self.__cache[package]
        except KeyError:
            raise LegoException(message="No package named `{0}` available".format(package))

        if apt_package.is_installed:
            self.__logger.info("`%s` is already installed", package)
        else:
            self.__logger.info("`%s` is not installed. Making for install.", package)
            apt_package.mark_install()

        try:
            self.__logger.info('Installing marked packages')
            self.__cache.commit()
        except Exception as ex:
            raise LegoException(message="Package `{0}` failed to install. "
                                        "Error: {1}".format(package, ex))

    def uninstall(self, package):
        """
        Uninstall already installed package.
        Args:
            package: Name of the package to uninstall.
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        try:
            apt_package = self.__cache[package]
        except KeyError:
            raise LegoException(message="No package named `{0}` available".format(package))

        if apt_package.is_installed:
            self.__logger.info("Marking package `%s` for unintsall", package)
            apt_package.mark_delete(True, purge=True)
        else:
            self.__logger.info("`%s` is not installed", package)

        try:
            self.__logger.info('Uninstall marked packages')
            self.__cache.commit()
        except Exception as ex:
            raise LegoException(message="Package `{0}` failed to uninstall. "
                                        "Error: {1}".format(package, ex))


class PackageBrick(Brick):  # pylint: disable=too-few-public-methods
    """
    Brick for managing packages.
    """

    def __init__(self, provided_attributes):
        self.__logger = logging.getLogger('lego.brick_modules.packages')
        self.__provided_attributes = provided_attributes
        self.__supported_attributes = self.__compulsory_attributes = [
            'type',
            'provider',
            'state',
            'packages'
        ]
        super(PackageBrick, self).__init__(name='lego.brick_modules.package_brick',
                                           logger=self.__logger,
                                           provided_attributes=self.__provided_attributes,
                                           supported_attributes=self.__supported_attributes,
                                           compulsory_attributes=self.__compulsory_attributes)

        self.__setup_package_manager()

    def __setup_package_manager(self):
        """
        Get the package manager object.
        Args:
            None
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        if self.__provided_attributes['provider'] == 'apt':
            self.__package_manager = AptPackageManager()
        else:
            raise LegoException(message="Package provider `{0}` is not "
                                        "supported. Supported package providers "
                                        "are `{1}`".format(self.__provided_attributes['provider'],
                                                           ['apt']))

    def manage_packages(self):
        """
        Manage packages on the system with given details.
        Args:
            attributes (dictionary): Details on how to manage this package.
        Returns:
            None
        Raises:
            None
        """
        for each_package in self.__provided_attributes['packages']:
            self.__logger.info("Managing package `%s` with package manager `%s`",
                               each_package, self.__provided_attributes['provider'])

            if self.__provided_attributes['state'] == 'present':
                self.__package_manager.install(package=each_package)

            if self.__provided_attributes['state'] == 'absent':
                self.__package_manager.uninstall(package=each_package)
