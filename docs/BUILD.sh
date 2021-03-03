#!/bin/bash

rm ./source/texturizer.rst
rm ./source/modules.rst

make clean
sphinx-apidoc -o ./source ../texturizer
make html

