#!/bin/sh

export ORDERS=(0 1 2 3 4 5 6)
export LEVELS=0
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(6)
export QUADS=true
export FLAME=true
export BASEP='hybridization_lu_params'
export PERFORMP='gtmg_fully_matfree_params_fs0_cg_jacobi_fs1_cg_laplacian_jacobi_fgmres_outerfgmres'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case6a/'