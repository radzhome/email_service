#!/bin/bash

# Make sure not in a virtualenv
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment detected. Deactivate and retry."
    exit 1
fi


# Create virtualenv for the project, pip install all the things
VIRTUALENV_DIR=.venv
virtualenv $VIRTUALENV_DIR --python=python3
. $VIRTUALENV_DIR/bin/activate
pip install -r requirements.txt
echo ""
echo ""

echo "Setup completed."