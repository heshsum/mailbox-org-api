from setuptools import find_packages, setup

setup(
    name='mailbox_org_api',
    packages=find_packages(),
    version='2.6',
    description='A library to access the mailbox Business API',
    author='Hendrik Schlange',
    install_requires=[
        'requests>=2.32.3',
        'urllib3>=2.8.0',
    ],
    tests_require=['pytest'],
    test_suite='tests',
)
