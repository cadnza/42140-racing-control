#!/usr/bin/env bash

# Make sure to install pybricks firmware first! You can do that here:
# https://code.pybricks.com/

# Activate virtual environment
. ./venv/bin/activate

# Send main to hub
pybricksdev run ble main.py

# Exit
exit 0
