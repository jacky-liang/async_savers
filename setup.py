"""Setup script for async_savers"""

from setuptools import setup

requirements = [
    'numpy',
    'pandas',
    'scikit-image',
    'simple_zmq'
]

setup(name='async_savers',
        version='0.2.0',
        author='Jacky Liang',
        author_email='jackyliang@cmu.edu',
        package_dir = {'': '.'},
        packages=['async_savers'],
        install_requires=requirements
        )