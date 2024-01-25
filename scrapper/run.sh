#!/bin/bash

set -e

source venv/bin/activate

echo -16 > /proc/$$/oom_adj
echo -1000 > /proc/$$/oom_score_adj

if [ "$1" == '-r' ]; then
	python main.py -s -s -i -i
else
	python main.py -s -s
fi
