#!/bin/bash

# Usage: ./build-dpkg.sh $version
# Example: ./build-dpkg.sh 3.14

if [[ "$#" -lt 1 ]]; then
    echo "You did not provide enough command line parameters. Example: tagrelease-builddpkg \$version"
    exit 1
fi

if [ -x "`which fpm`" ]; then
echo "FPM found, attempting to build package."
else
echo "Unable to find 'fpm', which is required to build package tarball. See https://github.com/jordansissel/fpm."
    exit 1
fi

version="$1"
package_name="python-pybindxml"
deb_name="${package_name}_$version.deb"

fpm -s python -t deb -n $package_name \
    -v $version \
    --package $deb_name \
    -x ".git" \
    `dirname $0`

if [ $? -ne 0 ]; then
echo "fpm executed exited with an error. Package was not built correctly."
    exit
fi
