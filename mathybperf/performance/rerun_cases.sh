#!/bin/sh
C='case1'
sh ./run_profiler.sh $C 0 --tex

C='case2'
sh ./run_profiler.sh $C 0 --tex

C='case2d'
sh ./run_profiler.sh $C 0 --tex

C='case2i'
sh ./run_profiler.sh $C 0 --tex

C='case2j'
sh ./run_profiler.sh $C 0 --tex

C='case3'
sh ./run_profiler.sh $C 0 --tex

C='case4'
sh ./run_profiler.sh $C 0 --tex
