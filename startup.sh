#!/bin/bash

source venv/scripts/activate
pwd=`pwd`
export FLASK_DEBUG=1
export FLASK_APP=application.py
cd src
flask run
cd ..