"""Setup script for async_savers"""

from setuptools import setup

requirements = [
    'numpy',
    'pandas',
    'scikit-image',
    'simple_zmq'
]

setup(name='async_savers',
        version='0.1.3',
        author='Jacky Liang',
        author_email='',
        package_dir = {'': '.'},
        packages=['async_savers'],
        install_requires=requirements
        )