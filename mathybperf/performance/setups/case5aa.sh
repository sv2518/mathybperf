#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare in global matfree mode
# compare to the same setup just with including locally matrix-free stuff too
export ORDERS=(0 1 2 3)
export LEVELS=2
export SCALING=(2)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(4)
export QUADS=true
export FLAME=true
export BASEP='gtmg_global_matfree_params_matexpmg_assembledjacobi_fgmres'
export PERFORMP='gtmg_fully_matfree_params_matexpmg_assembledjacobi_fs0_cg_jacobi_fgmres_evenlesstolonS'
export SOLTYPE='exponential'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case5aa/'