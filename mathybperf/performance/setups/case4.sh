#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare in global matfree mode
# compare to the same setup just with including locally matrix-free stuff too
export ORDERS=(0 1 2 3)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(3)
export QUADS=true
export FLAME=true
export BASEP='gtmg_global_matfree_nested_schur_params'
export PERFORMP='gtmg_fully_matfree_params'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case4/'