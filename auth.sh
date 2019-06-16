#!/bin/bash

cd "$(dirname "${BASH_SOURCE-$0}")"

T=`date +"%y-%m-%d %R"`
R=`./auth.py`

echo $T '  ' $R >> auth.log
