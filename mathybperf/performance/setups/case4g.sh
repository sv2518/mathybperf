#!/bin/sh

# Like case 4c but with some local solver option set
export ORDERS=(1)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(3)
export QUADS=true
export FLAME=true
export BASEP='gtmg_global_matfree_nested_schur_params_fgmres'
export PERFORMP='gtmg_fully_matfree_params_fs0_cg_jacobi_fgmres'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case4g/'