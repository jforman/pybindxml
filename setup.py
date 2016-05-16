from setuptools import setup

setup(
    name='pybindxml',
    version = '0.6',
    description='Read ISC BIND\'s statistics XML for processing.',
    author='Jeffrey Forman',
    author_email='code@jeffreyforman.net',
    license='MIT',
    packages = ['pybindxml'],
    url = 'http:://github.com/jforman/pybindxml',
    install_requires = ['beautifulsoup4'],
)
