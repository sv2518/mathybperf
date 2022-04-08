#!/bin/sh

# Same as 4c but we do the P1 solve matrix-explicit in the matrix-free setup
export ORDERS=(0 1 2 3)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(3)
export QUADS=true
export FLAME=true
export BASEP='gtmg_global_matfree_params_matexpmg_nested_schur_fgmres'
export PERFORMP='gtmg_fully_matfree_params_matexpmg_fgmres'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case4d/'