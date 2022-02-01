# Here are parameters defined used in the case files of my setups
# 1) HELPER DICTs

# MG params
mgmatfree_mtf = {'snes_type': 'ksponly',
                 'ksp_type': 'preonly',
                 'mat_type': 'matfree',
                 'pc_type': 'mg',
                 'pc_mg_type': 'full',
                 'mg_coarse_ksp_type': 'preonly',
                 'mg_coarse_pc_type': 'python',
                 'mg_coarse_pc_python_type': 'firedrake.AssembledPC',
                 'mg_coarse_assembled_pc_type': 'lu',
                 'mg_coarse_assembled_pc_factor_mat_solver_type': 'superlu_dist',
                 # 'mg_coarse_assembled_pc_mat_mumps_icntl_14': 200,
                 'mg_levels_ksp_type': 'chebyshev',
                 'mg_levels_ksp_max_it': 3,
                 'mg_levels_pc_type': 'none'}

mgmatfree_mtx = {'snes_type': 'ksponly',
                 'ksp_type': 'preonly',
                 'pc_type': 'mg',
                 'pc_mg_type': 'full',
                 'mg_coarse_ksp_type': 'preonly',
                 'mg_coarse_pc_type': 'python',
                 'mg_coarse_pc_python_type': 'firedrake.AssembledPC',
                 'mg_coarse_assembled_ksp_type': 'preonly',
                 'mg_coarse_assembled_pc_type': 'lu',
                 'mg_coarse_assembled_pc_factor_mat_solver_type': 'superlu_dist',
                 'mg_coarse_assembled_ksp_rtol': 1.e-10,
                 'mg_levels_ksp_type': 'chebyshev',
                 'mg_levels_ksp_max_it': 3,
                 'mg_levels_pc_type': 'none'}

mgmatexp = {'ksp_type': 'preonly',
            'pc_type': 'mg',
            'pc_mg_type': 'full',
            'mg_coarse': {'ksp_type': 'preonly',
                          'pc_type': 'lu',
                          'pc_factor_mat_solver_type': 'superlu_dist'},
            'mg_levels': {'ksp_type': 'chebyshev',
                          'pc_type': 'jacobi',
                          'ksp_max_it': 3}}

# Params for solves on levels
cheby_jacobi = {'ksp_type': 'chebyshev',
                'ksp_max_it': 3,
                'pc_type': 'jacobi'}
cheby_none = {'ksp_type': 'chebyshev',
              'ksp_max_it': 3,
              'pc_type': 'none'}

# Params for GTMG
gt_params_matexp = {'mg_levels': cheby_jacobi,
                    'mg_coarse': mgmatexp}
gt_params_global_matfree = {'mg_coarse': mgmatfree_mtf,
                            'mg_levels': cheby_none,
                            'mat_type': 'matfree'}
gt_params_fully_matfree = {'mg_coarse': mgmatfree_mtf,
                           'mg_levels': cheby_none,
                           'mat_type': 'matfree'}

# 2) FULL PARAMS
# Matrix explicit, direct hybridization
hybridization_lu_params = {'mat_type': 'matfree',
                           'ksp_type': 'preonly',
                           'pc_type': 'python',
                           'pc_python_type': 'firedrake.HybridizationPC',
                           'hybridization': {'ksp_type': 'preonly', 'pc_type': 'lu', 'pc_factor_mat_solver_type': 'superlu_dist', 'ksp_rtol': 1.e-8},
                           'ksp_view': None}

# Hyridization, globally matfree with CG, used in Thomas' matrix-free hybridization test
hybridization_global_matfree_cg = {'mat_type': 'matfree',
                                   'ksp_type': 'preonly',
                                   'pc_type': 'python',
                                   'pc_python_type': 'firedrake.HybridizationPC',
                                   'hybridization': {'ksp_type': 'cg',
                                                     'pc_type': 'none',
                                                     'ksp_rtol': 1.e-8,
                                                     'mat_type': 'matfree'}}

# These are the tests used for Jacks GTMG test in the Firedrake test suite
gtmg_matexpl_params = {'mat_type': 'matfree',
                       'ksp_type': 'preonly',
                       'pc_type': 'python',
                       'pc_python_type': 'firedrake.HybridizationPC',
                       'hybridization': {'ksp_type': 'cg',
                                         'pc_type': 'python',
                                         'ksp_rtol': 1e-8,
                                         'pc_python_type': 'firedrake.GTMGPC',
                                         'gt': {'mg_levels': cheby_jacobi,
                                                'mg_coarse': mgmatexp},
                                         'ksp_view': None}}

# These are the tests used for Jacks GTMG test in the Firedrake test suite
# but the Schur complement in the trace solve is nested
gtmg_matexpl_nested_schur_params = {'mat_type': 'matfree',
                                    'ksp_type': 'preonly',
                                    'pc_type': 'python',
                                    'pc_python_type': 'firedrake.HybridizationPC',
                                    'hybridization': {'ksp_type': 'cg',
                                                      'pc_type': 'python',
                                                      'ksp_rtol': 1.e-8,
                                                      # nested schur option
                                                      'localsolve': {'ksp_type': 'preonly',
                                                                     'pc_type': 'fieldsplit',
                                                                     'pc_fieldsplit_type': 'schur'},
                                                      'pc_python_type': 'firedrake.GTMGPC',
                                                      'gt': {'mg_levels': cheby_jacobi,
                                                             'mg_coarse': mgmatexp}}}

# These are the tests used for Jacks GTMG test in the Firedrake test suite
# with globally matrix-free solves on the levels
gtmg_global_matfree_params = {'snes_type': 'ksponly',
                              'mat_type': 'matfree',
                              'ksp_type': 'preonly',
                              'pc_type': 'python',
                              'pc_python_type': 'firedrake.HybridizationPC',
                              'hybridization': {'ksp_type': 'cg',
                                                'pc_type': 'python',
                                                # global matfree
                                                'mat_type': 'matfree',
                                                'pc_python_type': 'firedrake.GTMGPC',
                                                'ksp_rtol': 1.e-8,
                                                'gt': gt_params_global_matfree,
                                                'ksp_view': None}}

# These are the tests used for Jacks GTMG test in the Firedrake test suite
# with globally matrix-free solves on the levels and a nesting of schur complements on the trace solve
gtmg_global_matfree_nested_schur_params = {'snes_type': 'ksponly',
                                           'mat_type': 'matfree',
                                           'ksp_type': 'preonly',
                                           'pc_type': 'python',
                                           'pc_python_type': 'firedrake.HybridizationPC',
                                           'hybridization': {'ksp_type': 'cg',
                                                             'pc_type': 'python',
                                                             # global matfree
                                                             'mat_type': 'matfree',
                                                             # nested schur option, but not locally matfree!
                                                             'localsolve': {'ksp_type': 'preonly',
                                                                            # 'mat_type': 'matfree',
                                                                            'pc_type': 'fieldsplit',
                                                                            'pc_fieldsplit_type': 'schur'},
                                                             'ksp_rtol': 1.e-8,
                                                             'pc_python_type': 'firedrake.GTMGPC',
                                                             'gt': gt_params_global_matfree,
                                                             'ksp_view': None}}

# Fully matrix-free GTMG
# We need nested schur for local matfree
gtmg_fully_matfree_params = {'snes_type': 'ksponly',
                             'mat_type': 'matfree',
                             'ksp_type': 'preonly',
                             'pc_type': 'python',
                             'pc_python_type': 'firedrake.HybridizationPC',
                             'hybridization': {'ksp_type': 'cg',
                                               'pc_type': 'python',
                                               'mat_type': 'matfree',
                                               'ksp_rtol': 1.e-8,
                                               'localsolve': {'ksp_type': 'preonly',
                                                              'mat_type': 'matfree',  # local-matfree!
                                                              'pc_type': 'fieldsplit',
                                                              'pc_fieldsplit_type': 'schur'},
                                               'pc_python_type': 'firedrake.GTMGPC',
                                               'gt': gt_params_fully_matfree,
                                               'ksp_view': None}}


gtmg_fully_matfree_params_fs0_cg_jacobi = {'snes_type': 'ksponly',
                                           'mat_type': 'matfree',
                                           'ksp_type': 'preonly',
                                           'pc_type': 'python',
                                           'pc_python_type': 'firedrake.HybridizationPC',
                                           'hybridization': {'ksp_type': 'cg',
                                                             'pc_type': 'python',
                                                             'mat_type': 'matfree',
                                                             'ksp_rtol': 1.e-8,
                                                             'localsolve': {'ksp_type': 'preonly',
                                                                            'mat_type': 'matfree',  # local-matfree!
                                                                            'pc_type': 'fieldsplit',
                                                                            'pc_fieldsplit_type': 'schur',
                                                                            'fieldsplit_0': {'ksp_type': 'default',
                                                                                             'pc_type': 'jacobi'}},
                                                             'pc_python_type': 'firedrake.GTMGPC',
                                                             'gt': gt_params_fully_matfree,
                                                             'ksp_view': None}}

gtmg_fully_matfree_params_fs0_cg_jacobi_fs1_cg_jacobi = {'snes_type': 'ksponly',
                                                         'mat_type': 'matfree',
                                                         'ksp_type': 'preonly',
                                                         'pc_type': 'python',
                                                         'pc_python_type': 'firedrake.HybridizationPC',
                                                         'hybridization': {'ksp_type': 'cg',
                                                                           'pc_type': 'python',
                                                                           'mat_type': 'matfree',
                                                                           'ksp_rtol': 1.e-8,
                                                                           'localsolve': {'ksp_type': 'preonly',
                                                                                          'mat_type': 'matfree',  # local-matfree!
                                                                                          'pc_type': 'fieldsplit',
                                                                                          'pc_fieldsplit_type': 'schur',
                                                                                          'fieldsplit_0': {'ksp_type': 'default',
                                                                                                           'pc_type': 'jacobi'},
                                                                                          'fieldsplit_1': {'ksp_type': 'default',
                                                                                                           'pc_type': 'jacobi'}},
                                                                           'pc_python_type': 'firedrake.GTMGPC',
                                                                           'gt': gt_params_fully_matfree,
                                                                           'ksp_view': None}}
