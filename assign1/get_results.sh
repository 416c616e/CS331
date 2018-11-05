#!/bin/bash

pythonversion="python"
pythonfile="prog1.py"

modes="bfs dfs iddfs astar"
files="1 2 3"

startname="starts/start"
goalname="goals/goal"
outputname="outputs/output"

filetype="txt"

for mode in $modes;
do
    for file in $files;
    do
        echo -e "$mode $file\n"
        $pythonversion $pythonfile "${startname}${file}.${filetype}" "${goalname}${file}.${filetype}" $mode "${outputname}-$mode-${file}.${filetype}" --dont-print-solution-path
        echo -e "\n"
    done
done
