#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:$(pwd):$(pwd)/util

ps -ef | grep $(pwd)/gigglevc.py | grep -v grep | awk  '{print "kill " $2}' | /bin/bash

python3 $(pwd)/gigglevc.py &
