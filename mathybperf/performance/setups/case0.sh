#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare to lu on the trace solves
export ORDERS=(0 1 2 3 4 5)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(2)
export QUADS=true
export FLAME=true
export BASEP='hybridization_cg_params'
export PERFORMP='hybridization_global_matfree_cg'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case0/'