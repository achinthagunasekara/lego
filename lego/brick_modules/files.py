"""
Module to manage files on the system.
"""


import logging
from os.path import isfile
from os import chmod, chown
from hashlib import md5
from shutil import copyfile, rmtree
import pwd
import grp
from lego.brick import Brick
from lego.common import LegoException


def get_md5_checksum(file_to_get_md5):
    """
    Get the md5 checksum of a given file.
    Args:
        file_get_md5 (str): File to get it's md5 checksum.
    Returns:
        str: md5 checksum of the given file.
    Raises:
        None
    """
    hash_md5 = md5()
    with open(file_to_get_md5, "rb") as open_file:
        for chunk in iter(lambda: open_file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_file(destination, source=None):
    """
    Create a file based on a source and a destination.
    If no source is provided, this function will simply return.
    Args:
        destination (str): Destination file to be created.
        source (str): Source file to use for creating the destination.
    Returns:
        None
    Raises:
        None
    """
    logger = logging.getLogger('lego.brick_modules.files.create_file')

    if not source:
        logger.info("No source file provided for destination file `%s`. File will not be changed",
                    destination)
        return

    logger.info("Creating file `%s` from `%s`", destination, source)

    # Check if destination file exisits
    if isfile(destination):
        source_file_md5 = get_md5_checksum(file_to_get_md5=source)
        destination_file_md5 = get_md5_checksum(file_to_get_md5=destination)
        if source_file_md5 == destination_file_md5:
            logger.info("Both source file `%s` and destination file `%s` "
                        "are the same with md5 checksum `%s`",
                        source, destination, source_file_md5)
            logger.info('Skipping - Nothing to do')
            return
        logger.info("Destination file `%s` exists, but different to the source `%s`. "
                    "It'll be overwritten.", destination, source)
    copyfile(source, destination)

def remove_path(path):
    """
    Remove a given file or directory.
    Args:
        path (str): Path to remove.
    Returns:
        None.
    Raises:
        LegoException: Raises LegoException.
    """
    logger = logging.getLogger('lego.brick_modules.files.remove_path')
    try:
        logger.info("Removing path `%s`", path)
        rmtree(path)
    except OSError as os_ex:
        raise LegoException("Failed to remove `{0}` with "
                            "error `{1}`".format(path, os_ex))


def run_chown(path, user, group):
    """
    Set the owner and group of a given file.
    Args:
        path (str): Path the file.
        user (str): User file ownership is set to.
        group (str): Group file ownership is set to.
    Returns:
        None
    Raises:
        None
    """
    logger = logging.getLogger('lego.brick_modules.files.run_chown')
    uid = pwd.getpwnam(user).pw_uid
    gid = grp.getgrnam(group).gr_gid
    logger.info("Changing user to `%s(%s)` and group to `%s(%s)` for `%s`",
                user, uid, group, gid, path)
    chown(path, uid, gid)


def run_chmod(path, mode):
    """
    Set the mode on a given file.
    Args:
        path (str): Path the file.
        mode (int): Mode to set on the file.
    Returns:
        None
    Raises:
        LegoException: Raises LegoException.
    """
    logger = logging.getLogger('lego.brick_modules.files.run_chmod')
    if len(str(mode)) == 4 and mode.isdigit():
        raise LegoException("Mode `{0}` provided for file "
                            "`{1}` is invalid".format(mode, path))
    logger.info("Setting mode to `%s` on `%s`", mode, path)
    chmod(path, mode)



class FileBrick(Brick):  # pylint: disable=too-few-public-methods
    """
    Models a file brick.
    """

    supported_attributes = compulsory_attributes = [
        'type',
        'state',
        'owner',
        'group',
        'mode',
        'files'
    ]

    def __init__(self, brick_set_name, provided_attributes):
        self.brick_set_name = brick_set_name
        self.provided_attributes = provided_attributes
        super(FileBrick, self).__init__(name='file_brick',
                                        provided_attributes=self.provided_attributes,
                                        supported_attributes=FileBrick.supported_attributes,
                                        compulsory_attributes=FileBrick.compulsory_attributes)

    def run_brick(self):
        """
        Manage a given set of files.
        Args:
            None
        Returns:
            None
        Raises:
            LegoException: Raises LegoException.
        """
        for each_file in self.provided_attributes['files']:
            if 'source' in each_file.keys():
                source_file = "brick_sets/{0}/files/{1}".format(self.brick_set_name,
                                                                each_file['source'])
            else:
                source_file = None

            if 'destination' not in each_file.keys():
                raise LegoException("In a file brick, files attribute "
                                    "must have at least the `destination`")

            if self.provided_attributes['state'] not in ['present', 'absent']:
                raise LegoException("Unsupported state `{0}` "
                                    "for `{1}`".format(self.provided_attributes['state'],
                                                       each_file['destination']))

            if self.provided_attributes['state'] == 'absent':
                remove_path(path=each_file['destination'])
            else:
                create_file(destination=each_file['destination'],
                            source=source_file)

                run_chmod(path=each_file['destination'],
                          mode=self.provided_attributes['mode'])

                run_chown(path=each_file['destination'],
                          user=self.provided_attributes['owner'],
                          group=self.provided_attributes['group'])
