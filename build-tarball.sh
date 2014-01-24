#!/bin/bash

# This script assumes the use of the sites-packages directory
# to play nicely with OpenBSD
# Usage: ./build-tarball <version>

version=$1

fpm -s python \
    -t tar \
    -v $version \
    -n python-pybindxml_$version \
    --python-install-lib /usr/local/lib/python2.7/site-packages \
    setup.py

gzip -v python-pybindxml_$version.tar