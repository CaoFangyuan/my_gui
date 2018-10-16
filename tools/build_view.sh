#!/bin/bash
#
# @file build_view.sh
#
# @brief Convert ui files into python files
#
# @author David Chiasson (dchiasso@sjtu.edu.cn)
#

if [ ! -d "view" ]
then
    echo "Please run this from the sage_controller directory"
    exit
fi

for ui_file in view/*.ui
do
  output=$(basename $ui_file .ui).py
  pyuic5 $ui_file -o controller/forms/$output
done

