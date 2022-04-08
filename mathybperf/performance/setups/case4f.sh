#!/bin/sh

# Same as 4e but we are comparing to the actual baseline (fully matrix explicit)
export ORDERS=(0 1 2 3)
export LEVELS=2
export SCALING=(1)
export DEFORM=(0)
export TRAFO='none' # 'affine'
export ATQD=(0 0)
export CELLSPD=(3)
export QUADS=true
export FLAME=true
export BASEP='gtmg_matexpl_nested_schur_params'
export PERFORMP='gtmg_fully_matfree_params_matexpmg_fgmres_assembledjacobi'
export SOLTYPE='quadratic'
export PROJECTEXACTSOL="" #--projectexactsol
export CASE='/case4f/'