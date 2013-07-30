#!/bin/sh

# This script setup a virtualenvironment for developing washr

virtualenv -p python2.7 .venv

source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-test.txt
