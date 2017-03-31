#!/bin/bash
#
# @author:Don Dennis (metastableB)
# automatedRuns.sh
#
# Automatically run simulation without text graphics
# for a specified number of times

# TODO: Move to command line arguments
numRuns=10
foodAgent='RandomFoodAgent'
snakeAgent='ReflexAgent'

# add dlsnake to python path
dlsnakePATH=$(pwd)/../
export PYTHONPATH=${PYTHONPATH}:${dlsnakePATH}

# Run for numRun tries
for i in $(seq 1 ${numRuns}); do
	python -m dlsnake.snakeGame --agent ${snakeAgent} --no-graphics --silent --csv
done
