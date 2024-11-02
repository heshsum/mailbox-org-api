from setuptools import find_packages, setup

setup(
    name='mailbox-api-client',
    packages=find_packages(),
    version='0.1.0',
    description='A library to access the mailbox.org Business API',
    author='Hendrik Schlange',
    install_requires=['json, requests'],
    tests_require=['pytest'],
    test_suite='tests',
)