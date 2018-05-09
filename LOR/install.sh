#!/bin/bash
python3 -m pip install requests
python3 -m pip install beautifulsoup4
ABS_FILENAME=`readlink -e "$0"`
DIRECTORY=`dirname "$ABS_FILENAME"`
NEW_PATH=$DIRECTORY'/top_pcg/main.py'
touch /usr/bin/lorviewer
echo python3 "$NEW_PATH" >> /usr/bin/lorviewer
chmod +x /usr/bin/lorviewer
