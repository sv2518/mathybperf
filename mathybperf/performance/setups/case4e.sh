#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare in global matfree mode
# compare to the same setup just with including locally matrix-free stuff too

# I decreased the tolerance in the local solver for this run because we check for absolute tol
# We do the P1 solve matrix-explicit in the matrix-free setup
# and have no jacobi on the matrix-explicit GTMG base run
# without local logging
export ORDERS=(0 1 2 3)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(3)
export QUADS=true
export FLAME=true
export BASEP='gtmg_matexpl_nested_schur_params_chebynone'
export PERFORMP='gtmg_fully_matfree_params_matexpmg'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case4e/'