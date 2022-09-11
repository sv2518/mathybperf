#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare in global matfree mode
# compare to the same setup just with including locally matrix-free stuff too
export ORDERS=(0 1 2 3 4 5)
export LEVELS=2
export SCALING=(2)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(1 2 3 4)
export QUADS=true
export FLAME=true
export BASEP='gtmg_matexpl_params'
export PERFORMP='native_dg'
export SOLTYPE='exponential'
export PROJECTEXACTSOL="--projectexactsol"
export CASE='/case8/'
