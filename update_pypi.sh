#!/bin/bash

rm -rf dist/
/usr/bin/python setup.py build sdist bdist bdist_wheel
twine upload dist/*
