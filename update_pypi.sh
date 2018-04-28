#!/bin/bash

rm -rf dist/
/usr/bin/python setup.py build bdist
twine upload dist/*
