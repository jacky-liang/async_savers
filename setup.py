"""Setup script for async_savers"""

from setuptools import setup

requirements = [
    'numpy',
    'pandas',
    'scikit-image',
    'simple_zmq'
]

setup(name='async_savers',
        version='0.1.0',
        author='Jacky Liang',
        author_email='jackyliang42@gmail.com',
        package_dir = {'': '.'},
        packages=['async_savers'],
        install_requires=requirements
        )