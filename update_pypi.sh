#!/bin/bash

/usr/bin/python setup.py bdist_wheel
twine update dist/*
