#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare in global matfree mode
# but with a nesting of the schur complements and cg replaced with fgmres
# to the exact same setup just with including locally matrix-free stuff too

# We do still have the P1 solve matrix-free in the matrix-free setup in this setup
export ORDERS=(0 1 2 3)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(3)
export QUADS=true
export FLAME=true
export BASEP='gtmg_global_matfree_nested_schur_params_fgmres'
export PERFORMP='gtmg_fully_matfree_params_fgmres'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case4c/'