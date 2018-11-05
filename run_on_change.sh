#!/bin/bash

PROGRAM=$1

START=$2
GOAL=$3
METHODS="bfs dfs iddfs astar"
OUTPUT=$4

shift

inotifywait -m -e close_write,moved_to --format %e/%f . | 
while IFS=/ read -r events file; do
	if [ "$file" = "$PROGRAM" ]; then
		clear
		echo Start file: $START
		echo Goal file: $GOAL
		echo
		echo Started: `date`
		echo
		for METHOD in $METHODS; do
			./$PROGRAM $START $GOAL $METHOD "$OUTPUT.$METHOD"
			echo
		done
		echo Finished: `date`
	fi
done
