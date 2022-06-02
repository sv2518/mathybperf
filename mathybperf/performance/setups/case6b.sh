#!/bin/sh

# This run just compares how Jacks GTMG on the trace solve compare in global matfree mode
# compare to the same setup just with including locally matrix-free stuff too
export ORDERS=(0 1 2 3 4 5 6 7)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(3)
export QUADS=true
export FLAME=true
export PERFORMP='gtmg_global_matfree_params_matexpmg_assembledjacobi_fgmres'
export BASEP='gtmg_fully_matfree_params_fs0_cg_jacobi_fs1_cg_laplacian_jacobi_fgmres_outerfgmres_withgtmg'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case6b/'