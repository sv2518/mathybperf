#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare to the same setup just globally matrix-free
export ORDERS=(0)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(3)
export QUADS=true
export FLAME=true
export BASEP='gtmg_matexpl_params_maxitscg'
export PERFORMP='gtmg_global_matfree_params_maxitscg'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case2a/'