from distutils.core import setup

# add dependency for python-bs4

setup(
    name='pybindxml',
    version = '0.1',
    description='Read ISC BIND\'s statistics XML for processing.',
    author='Jeffrey Forman',
    author_email='code@jeffreyforman.net',
    license='MIT',
    packages = ['pybindxml'],
    url = 'https://github.com/jforman/pybindxml',
)
