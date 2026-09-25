#!/bin/bash
# Mac: double-click this file to run the setup.
# It just runs setup.sh, which is the real script.
cd "$(dirname "$0")" || exit 1
./setup.sh
read -n 1 -s -r -p "Press any key to close this window..."
echo
