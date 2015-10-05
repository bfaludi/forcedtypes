
from setuptools import setup, find_packages
import sys, os

version = '1.0.1'

setup(
    name = 'forcedtypes',
    version = version,
    description = "Force crappy data into python type.",
    packages = find_packages( exclude = [ 'ez_setup'] ),
    include_package_data = True,
    zip_safe = False,
    author = 'Bence Faludi',
    author_email = 'bence@ozmo.hu',
    license = 'GPL',
    install_requires = [
        'dateutils',
        'babel',
    ],
    test_suite = "forcedtypes.tests",
    url = 'http://bfaludi.com'
)