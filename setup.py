from setuptools import find_packages, setup

setup(
    name='mailbox_org_api',
    packages=find_packages(),
    version='1.4',
    description='A library to access the mailbox.org Business API',
    author='Hendrik Schlange',
    install_requires=['requests'],
    tests_require=['pytest'],
    test_suite='tests',
)
