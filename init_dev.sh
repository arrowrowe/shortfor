#!/bin/bash

if [ -d env ]; then
    echo already
else
    virtualenv -p `which python3` env
fi

