#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare to lu on the trace solves
export ORDERS=(2 3 4 5)
export LEVELS=2
export SCALING=(2)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(1 2 3 4)
export QUADS=true
export FLAME=true
export BASEP='hybridization_lu_params'
export PERFORMP='hybridization_cg_params'
export SOLTYPE='exponential'
export PROJECTEXACTSOL="--projectexactsol"
export CASE='/case0/'
