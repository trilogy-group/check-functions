#!/bin/bash

# Get the directory containing the script
script_dir=$(dirname "$(realpath "$0")")
checks_dir=$script_dir/../src/checks

find $checks_dir -mindepth 1 -maxdepth 1 -type d -exec bash $script_dir/createUtilsSymlink.sh {} \;
