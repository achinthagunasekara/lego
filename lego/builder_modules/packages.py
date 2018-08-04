"""
Module to manage packges on a system and it's supporting modules.
"""

import logging
from lego.common import LegoException, validate


SUPPORTED_PACKAGE_PROVIDERS = [
    'apt'
]


SUPPORTED_ATTRIBUTES = COMPULSORY_ATTRIBUTE = [
    'type',
    'provider',
    'state',
    'packages'
]


def manage_packages(attributes):
    """
    Manage packages on the system with given details.
    Args:
        attributes (dictionary): Details on how to manage this package.
    Returns:
        None
    Raises:
        LegoException: Raises LegoException.
    """
    logger = logging.getLogger('packages.manage_packages')
    if not validate(provided_attributes=attributes.keys(),
                    supported_attributes=SUPPORTED_ATTRIBUTES,
                    compulsory_attributes=COMPULSORY_ATTRIBUTE):
        raise LegoException(message='Attribute validation failed')

    if attributes['provider'] not in SUPPORTED_PACKAGE_PROVIDERS:
        raise LegoException(message="Package provider `{0}` is not "
                                    "supported. Supported package providers "
                                    "are `{1}`".format(attributes['provider'],
                                                       SUPPORTED_PACKAGE_PROVIDERS))

    for each_package in attributes['packages']:
        logger.info("Managing package `%s` with package manager `%s`",
                    each_package, attributes['provider'])

        if attributes['provider'] == 'apt':
            package_manager = AptPackageManager()

        if attributes['state'] == 'present':
            package_manager.install(package=each_package)

        if attributes['state'] == 'absent':
            package_manager.uninstall(package=each_package)


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
        self.__logger = logging.getLogger('AptPackage')
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
