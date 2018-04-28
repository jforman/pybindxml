from setuptools import setup

setup(
    name='pybindxml',
    version='0.6.3',
    description='Read ISC BIND\'s statistics XML for processing.',
    author='Jeffrey Forman',
    author_email='code@jeffreyforman.net',
    license='MIT',
    url='https://github.com/jforman/pybindxml',
    packages=['pybindxml'],
    install_requires=['beautifulsoup4'],
)
