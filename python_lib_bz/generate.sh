#! /bin/bash
rm doc/*.rst
sphinx-apidoc -o ./doc ./
cd doc
make html

open _build/html/index.html
