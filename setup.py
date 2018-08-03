"""
Setup for Lego configuration management tool.
"""

from distutils.core import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()  # pylint: disable=invalid-name


setup(
    name='lego',
    version='0.1',
    packages=['lego',],
    license='GNU General Public License v3.0+ '
            '(see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)',
    long_description='Lego Configuration Management Tool',
    requires=required
)
