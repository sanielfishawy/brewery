#!/bin/bash

SERVER_DIR=/home/pi/dev/brew_server
cd $SERVER_DIR

source ./venv/bin/activate

/home/pi/dev/brew_server/venv/bin/python server.py