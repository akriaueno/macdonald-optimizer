#!/usr/bin/env bash 
set -x
dir_name=$(cd $(dirname $0) && pwd)

cd $dir_name

mkdir -p ../data/
./get_data.sh
./save_to_sqlite.py

set +x