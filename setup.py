"""
Setup for Lego configuration management tool.
"""

from setuptools import setup


with open('requirements.txt') as requirements_file:
    required = requirements_file.read().splitlines()  # pylint: disable=invalid-name

setup(
    name='lego',
    version='0.1',
    packages=['lego','lego.builder_modules',],
    license='GNU General Public License v3.0+ '
            '(see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)',
    long_description='Lego Configuration Management Tool',
    install_requires=required,
    entry_points={
        'console_scripts': [
            'lego=lego.executable:main',
        ],
    }
)
