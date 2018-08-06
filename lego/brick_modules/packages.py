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

    def __init__(self, name):
        self.logger = logging.getLogger("lego.brick_modules.packages.{0}Package".format(name))

    def __setup(self):
        pass

    def install(self, package):
        """
        Install a package.
        Must be implemented in the subclass.
        Args:
            package: Name of the package to install.
        Returns:
            None
        Raises:
            None
        """
        pass

    def uninstall(self, package):
        """
        Uninstall already installed package.
        Must be implemented in the subclass.
        Args:
            package: Name of the package to uninstall.
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
        super(AptPackageManager, self).__init__(name='Apt')
        self.__setup()

    def __setup(self):
        import apt  # pylint: disable=import-error
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
            raise LegoException("No package named `{0}` available".format(package))

        if apt_package.is_installed:
            self.logger.info("`%s` is already installed", package)
        else:
            self.logger.info("`%s` is not installed. Making for install.", package)
            apt_package.mark_install()

        try:
            self.logger.info('Installing marked packages')
            self.__cache.commit()
        except Exception as ex:
            raise LegoException("Package `{0}` failed to install. Error: {1}".format(package, ex))

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
            raise LegoException("No package named `{0}` available".format(package))

        if apt_package.is_installed:
            self.logger.info("Marking package `%s` for unintsall", package)
            apt_package.mark_delete(True, purge=True)
        else:
            self.logger.info("`%s` is not installed", package)

        try:
            self.logger.info('Uninstall marked packages')
            self.__cache.commit()
        except Exception as ex:
            raise LegoException("Package `{0}` failed to uninstall. "
                                "Error: {1}".format(package, ex))


class PackageBrick(Brick):  # pylint: disable=too-few-public-methods
    """
    Brick for managing packages.
    """

    supported_attributes = compulsory_attributes = [
        'type',
        'provider',
        'state',
        'packages'
    ]

    def __init__(self, provided_attributes):
        self.provided_attributes = provided_attributes
        super(PackageBrick, self).__init__(name='package_brick',
                                           provided_attributes=self.provided_attributes,
                                           supported_attributes=PackageBrick.supported_attributes,
                                           compulsory_attributes=PackageBrick.compulsory_attributes)
        self.__run_setup()

    def __run_setup(self):
        """
        Get the package manager object.
        Args:
            None
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        if self.provided_attributes['provider'] == 'apt':
            self.package_manager = AptPackageManager()
        else:
            raise LegoException("Package provider `{0}` is not supported. "
                                "Supported package providers "
                                "are `{1}`".format(self.provided_attributes['provider'], ['apt']))

    def run_brick(self):
        """
        Manage packages on the system with given details.
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        for each_package in self.provided_attributes['packages']:
            self.logger.info("Managing package `%s` with package manager `%s`",
                             each_package, self.provided_attributes['provider'])

            if self.provided_attributes['state'] == 'present':
                self.package_manager.install(package=each_package)

            if self.provided_attributes['state'] == 'absent':
                self.package_manager.uninstall(package=each_package)
