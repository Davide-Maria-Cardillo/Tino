#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# bash /home/tino/Desktop/Tino2/launcher.sh

# start new MAIN.PY
cd "$(dirname "$(readlink -f "$0")")"

# Activate the virtual environment
source  ~/etereum/bin/activate

# Execute the Python script
python3 main.py
#python3 EventLogitech.py
#bash /home/tino/Desktop/Tino2/launcher.sh