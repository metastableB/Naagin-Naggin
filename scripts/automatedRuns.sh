#!/bin/bash
#
# @author:Don Dennis (metastableB)
# automatedRuns.sh
#
# Automatically run simulation without text graphics
# for a specified number of times
#
# Here is a sample Time output for referrence
# 	time ./automatedRuns.sh > '00_100_ReflexAgent_RandomFoodAgent.csv'
# 	real	1m23.778s
# 	user	1m29.413s
# 	sys	0m54.193s
# RandomFoodAgnet and ReflexAgent were used for 100 trials


# TODO: Move to command line arguments
numRuns=40
foodAgent='MaxManhattanFoodAgent'
snakeAgent='MinMaxAgent'
currdepth=$1
# add dlsnake to python path
dlsnakePATH=$(pwd)/../
export PYTHONPATH=${PYTHONPATH}:${dlsnakePATH}

# Run for numRun tries
for i in $(seq 1 ${numRuns}); do
	python -m dlsnake.snakeGame --agent=MinMaxAgent   --food-agent=MaxManhattanFoodAgent --depth=${currdepth} --csv --silent
done
