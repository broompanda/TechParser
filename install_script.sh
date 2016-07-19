#!/bin/bash

curr_dir=$(pwd)

gt="alias gt='python $curr_dir/FileChar.py'"
pt="alias pt=put_file"
echo $gt >> ~/.bash_profile
echo $pt >> ~/.bash_profile
printf '%s\n\t%s\n\t%s\n\t%s\n\t\t%s\n\t\t%s\n\t%s\n\t%s\n%s' 'put_file(){' 'file_number=$1' 'short_file_name=$2' 'if [ ! -z "$short_file_name" ]; then' 'directory=$(pwd)' 'full_file_name="$directory/$short_file_name"' 'fi' 'python '$(pwd)/TrackFile2.py' '\$file_number' '\$full_file_name'' '}' >> ~/.bash_profile
