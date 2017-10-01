#!/bin/sh

virtualenv -p `which python3` .ve
.ve/bin/pip install -r requirements.txt
