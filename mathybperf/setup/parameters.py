from .auxiliary import DGLaplacian

parameters_schur_preonly_lu = {
    "ksp_monitor_true_residual": None,
    "ksp_type": "fgmres",
    "ksp_rtol": 1.0e-6,
    "ksp_atol": 1.0e-6,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",
    "fieldsplit_0_ksp_type": "preonly",
    "fieldsplit_0_pc_type": "lu",
    "fieldsplit_0_ksp_rtol": 1e-12,
    "fieldsplit_0_ksp_atol": 1e-12,
    "fieldsplit_0_ksp_max_it": 2000,
    "fieldsplit_1_ksp_type": "preonly",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_aux_pc_type": "lu",
    "fieldsplit_1_ksp_rtol": 1e-8,
    "fieldsplit_1_ksp_atol": 1e-8,
    "fieldsplit_1_ksp_max_it": 2000
}

parameters_schur_preonly_lu_cg_lu = {
    "ksp_monitor_true_residual": None,
    "ksp_type": "fgmres",
    "ksp_rtol": 1e-10,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",
    "fieldsplit_0_ksp_type": "preonly",
    "fieldsplit_0_pc_type": "lu",
    "fieldsplit_0_ksp_rtol": 1e-12,
    "fieldsplit_1_ksp_type": "cg",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_aux_pc_type": "lu",
    "fieldsplit_1_ksp_rtol": 1e-12
}

parameters_schur_preonly_jacobi_cg_jacobi = {
    "ksp_monitor_true_residual": None,
    "ksp_type": "fgmres",
    "ksp_rtol": 1e-10,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",
    "fieldsplit_0_ksp_type": "preonly",
    "fieldsplit_0_pc_type": "jacobi",
    "fieldsplit_0_ksp_rtol": 1e-12,
    "fieldsplit_1_ksp_type": "cg",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_aux_pc_type": "jacobi",
    "fieldsplit_1_ksp_rtol": 1e-12
}

parameters_schur_cheby_jacobi_cg_jacobi = {
    "ksp_monitor_true_residual": None,
    "ksp_type": "fgmres",
    "ksp_rtol": 1e-10,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",
    "fieldsplit_0_ksp_type": "chebyshev",
    "fieldsplit_0_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_type": "cg",
    "fieldsplit_0_esteig_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_max_it": 2,
    "fieldsplit_0_ksp_rtol": 1e-12,

    "fieldsplit_1_ksp_type": "cg",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_aux_pc_type": "jacobi",
    "fieldsplit_1_ksp_rtol": 1e-12,
}

parameters_changemaxits_schur_cg_jacobi_cg_jacobi = {
    "ksp_type": "fgmres",
    "ksp_rtol": 1.0e-6,
    "ksp_atol": 1.0e-6,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "diag",
    "fieldsplit_0_ksp_type": "cg",
    "fieldsplit_0_pc_type": "jacobi",
    # "fieldsplit_0_pc_type": "python",
    # "fieldsplit_0_pc_python_type": __name__+ ".Mass",
    # "fieldsplit_0_aux_pc_type": "ksp",
    # "fieldsplit_0_aux_ksp_ksp_type": "chebyshev",
    # "fieldsplit_0_aux_ksp_pc_type": "jacobi",
    # "fieldsplit_0_aux_ksp_ksp_max_it": 2,
    # "fieldsplit_0_aux_ksp_ksp_convergence_test": "skip",
    # "fieldsplit_0_aux_ksp_esteig_ksp_type": "cg",
    # "fieldsplit_0_aux_ksp_esteig_pc_type": "jacobi",
    # "fieldsplit_0_aux_ksp_esteig_ksp_max_it": 1500,
    # "fieldsplit_0_aux_ksp_esteig_ksp_rtol": 1e-16,
    "fieldsplit_0_ksp_rtol": 1e-12,
    "fieldsplit_0_ksp_atol": 1e-12,
    "fieldsplit_0_ksp_max_it": 2000,
    # "fieldsplit_0_ksp_convergence_test": "skip", #make cheby stationary

    "fieldsplit_1_ksp_type": "cg",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_ksp_rtol": 1e-8,
    "fieldsplit_1_ksp_atol": 1e-8,
    "fieldsplit_1_ksp_max_it": 2000,

    "fieldsplit_1_aux_pc_type": "jacobi",
    # "fieldsplit_1_aux_ksp_ksp_type": "chebyshev",
    # "fieldsplit_1_aux_ksp_pc_type": "jacobi",
    # "fieldsplit_1_aux_ksp_ksp_max_it": 20,
    # # "fieldsplit_1_aux_ksp_ksp_convergence_test": "skip",
    # "fieldsplit_1_aux_ksp_esteig_ksp_type": "cg",
    # "fieldsplit_1_aux_ksp_esteig_pc_type": "jacobi",
    # "fieldsplit_1_aux_ksp_esteig_ksp_max_it": 1500,
    # "fieldsplit_1_aux_ksp_esteig_ksp_rtol": 1e-12,
    # # "fieldsplit_1_aux_ksp_esteig_ksp_atol": 1e-12,
    # "fieldsplit_1_aux_ksp_ksp_chebyshev_eigenvalues": "0.075, 2.55",
    # "fieldsplit_1_aux_ksp_ksp_converged_reason": None,
    # "fieldsplit_1_ksp_monitor_true_residual": None,
    # "fieldsplit_0_ksp_monitor_true_residual": None,
    # "ksp_view": None
}

parameters_changemaxits_schur_cheby_jacobi_bcgs_cheby_jacobi = {
    "ksp_monitor_true_residual": None,
    "ksp_type": "fgmres",
    "ksp_rtol": 1e-10,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",

    "fieldsplit_0_ksp_type": "chebyshev",
    "fieldsplit_0_esteig_ksp_type": "cg",
    "fieldsplit_0_esteig_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_max_it": 1500,
    "fieldsplit_0_esteig_ksp_rtol": 1e-12,
    # "fieldsplit_0_chebyshev_esteig": "0, 0.1, 0, 1.5",
    "fieldsplit_0_pc_type": "jacobi",
    "fieldsplit_0_ksp_rtol": 1e-12,
    "fieldsplit_0_ksp_max_it": 40, # 30 does not seem to be enough
    "fieldsplit_0_convergence_test": "skip", #make cheby stationary

    "fieldsplit_1_ksp_type": "bcgs",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_ksp_rtol": 1e-12,
    "fieldsplit_1_ksp_max_it": 10,

    "fieldsplit_1_aux_pc_type": "ksp",
    "fieldsplit_1_aux_ksp_ksp_type": "chebyshev",
    "fieldsplit_1_aux_ksp_pc_type": "jacobi",
    "fieldsplit_1_aux_ksp_ksp_max_it": 5,
    "fieldsplit_1_aux_ksp_ksp_convergence_test": "skip",
    "fieldsplit_1_aux_ksp_esteig_ksp_type": "cg",
    "fieldsplit_1_aux_ksp_esteig_pc_type": "jacobi",
    "fieldsplit_1_aux_ksp_esteig_ksp_max_it": 1500,
    "fieldsplit_1_aux_ksp_esteig_ksp_rtol": 1e-12,
    # "fieldsplit_1_aux_ksp_chebyshev_esteig": "0.5, 1.5",
    "ksp_converged_reason": None,
}

parameters_schur_cheby_jacobi_preonly_jacobi= {
    "ksp_monitor_true_residual": None,
    "ksp_type": "fgmres",
    "ksp_rtol": 1e-10,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",

    "fieldsplit_0_ksp_type": "chebyshev",
    "fieldsplit_0_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_type": "cg",
    "fieldsplit_0_esteig_pc_type": "jacobi",
    "fieldsplit_0_ksp_rtol": 1e-12,
    "fieldsplit_0_esteig_ksp_max_it": 2,

    "fieldsplit_1_ksp_type": "preonly",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_aux_pc_type": "jacobi",
    "fieldsplit_1_ksp_rtol": 1e-12,

    # "fieldsplit_0_esteig_ksp_converged_reason": None,
    # "fieldsplit_1_ksp_converged_reason": None,
    # "fieldsplit_0_ksp_converged_reason": None,
    # "ksp_converged_reason": None,

}

parameters_schur_cheby_jacobi_cheby_jacobi = {
    "ksp_monitor_true_residual": None,
    "ksp_type": "fgmres",
    "ksp_rtol": 1e-10,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",
    "fieldsplit_0_ksp_type": "chebyshev",
    "fieldsplit_0_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_type": "cg",
    "fieldsplit_0_esteig_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_max_it": 2,
    "fieldsplit_0_ksp_rtol": 1e-12,

    "fieldsplit_1_ksp_type": "chebyshev",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_aux_pc_type": "jacobi",
    "fieldsplit_1_ksp_chebyshev_esteig": "35.0,1.3",
    "fieldsplit_1_esteig_ksp_type": "cg",
    "fieldsplit_1_esteig_pc_type": "jacobi",
    "fieldsplit_1_esteig_ksp_max_it": 70,
    "fieldsplit_1_ksp_rtol": 1e-12,
    # "fieldsplit_1_ksp_it_max": 200

    # "fieldsplit_1_esteig_ksp_converged_reason": None,
    # "fieldsplit_1_ksp_converged_reason": None,
    # "fieldsplit_0_ksp_converged_reason": None,
    # "pc_fieldsplit_ksp_converged_reason": None,
    # "ksp_view": None
}

parameters_bcgs_schur_cheby_jacobi_cheby_jacobi = {
    "ksp_monitor_true_residual": None,
    "ksp_type": "bcgs",
    "ksp_rtol": 1e-10,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",
    "fieldsplit_0_ksp_type": "chebyshev",
    "fieldsplit_0_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_type": "cg",
    "fieldsplit_0_esteig_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_max_it": 2,
    "fieldsplit_0_ksp_rtol": 1e-12,

    "fieldsplit_1_ksp_type": "chebyshev",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_aux_pc_type": "jacobi",
    "fieldsplit_1_ksp_chebyshev_esteig": "35.0,1.3",
    "fieldsplit_1_esteig_ksp_type": "cg",
    "fieldsplit_1_esteig_pc_type": "jacobi",
    "fieldsplit_1_esteig_ksp_max_it": 70,
    "fieldsplit_1_ksp_rtol": 1e-12,
    # "fieldsplit_1_ksp_it_max": 200

    # "fieldsplit_1_esteig_ksp_converged_reason": None,
    # "fieldsplit_1_ksp_converged_reason": None,
    # "fieldsplit_0_ksp_converged_reason": None,
    # "pc_fieldsplit_ksp_converged_reason": None,
    # "ksp_view": None
}
parameters_preonly_schur_cheby_jacobi_cheby_jacobi = {
    "ksp_monitor_true_residual": None,
    "ksp_type": "preonly",
    "ksp_rtol": 1e-10,
    "pc_type": "fieldsplit",
    "pc_fieldsplit_type": "schur",
    "pc_fieldsplit_schur_fact_type": "full",
    "fieldsplit_0_ksp_type": "chebyshev",
    "fieldsplit_0_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_type": "cg",
    "fieldsplit_0_esteig_pc_type": "jacobi",
    "fieldsplit_0_esteig_ksp_max_it": 2,
    "fieldsplit_0_ksp_rtol": 1e-12,

    "fieldsplit_1_ksp_type": "chebyshev",
    "fieldsplit_1_pc_type": "python",
    "fieldsplit_1_pc_python_type": __name__+ ".DGLaplacian",
    "fieldsplit_1_aux_pc_type": "jacobi",
    "fieldsplit_1_ksp_chebyshev_esteig": "35.0,1.3",
    "fieldsplit_1_esteig_ksp_type": "cg",
    "fieldsplit_1_esteig_pc_type": "jacobi",
    "fieldsplit_1_esteig_ksp_max_it": 70,
    "fieldsplit_1_ksp_rtol": 1e-12,
    # "fieldsplit_1_ksp_it_max": 200

    # "fieldsplit_1_esteig_ksp_converged_reason": None,
    # "fieldsplit_1_ksp_converged_reason": None,
    # "fieldsplit_0_ksp_converged_reason": None,
    # "pc_fieldsplit_ksp_converged_reason": None,
    # "ksp_view": None
}



mg_param_amg = {'ksp_type': 'preonly', 'pc_type': 'gamg',
            'ksp_rtol': 1E-8,
            'pc_mg_cycles': 'v',
            'mg_levels': {'ksp_type': 'chebyshev',
                            'ksp_max_it': 2, 'pc_type': 'bjacobi', 'sub_pc_type': 'sor'},
            'mg_coarse': {'ksp_type':'chebyshev', 'ksp_max_it':2,
                        'pc_type':'sor'}}
mg_param_gmg = {'ksp_type': 'preonly',
                'pc_type': 'mg',
                'ksp_rtol': 1E-8,
                'pc_mg_levels':2,
                'pc_mg_cycles': 'v',
                'mg_levels': {'ksp_type': 'chebyshev',
                            'ksp_max_it': 2,
                            'pc_type': 'bjacobi',
                            'sub_pc_type': 'sor'},
                'mg_coarse': {'ksp_type':'chebyshev',
                              'ksp_max_it':2,
                              'pc_type':'sor'}}
                        
mg_jack = {"ksp_type": "preonly",
        "pc_type": "mg",
        "pc_mg_type": "full",
        "mg_levels_ksp_type": "chebyshev",
        "mg_levels_ksp_max_it": 3,
        "mg_levels_pc_type": "jacobi"}
mgb = {"snes_type": "ksponly",
            "ksp_type": "preonly",
            "pc_type": "mg",
            "pc_mg_type": "full",
            "mg_levels_ksp_type": "chebyshev",
            "mg_levels_ksp_max_it": 2,
            "mg_levels_pc_type": "fieldsplit",
            "mg_levels_pc_fieldsplit_type": "additive",
            "mg_levels_fieldsplit_pc_type": "jacobi",
            "mg_coarse_pc_type": "fieldsplit",
            "mg_coarse_pc_fieldsplit_type": "additive",
            "mg_coarse_fieldsplit_pc_type": "redundant",
            "mg_coarse_fieldsplit_redundant_pc_type": "lu",
            "mg_coarse_ksp_type": "preonly",
            "snes_convergence_test": "skip"} # does not work bc additive I think
p1pc = {"ksp_type": "cg",
        "pc_type": "python",
        "mat_type": "matfree",
        "pc_python_type": "firedrake.P1PC",
        "pmg_coarse_degree": 2,
        "pmg_mg_levels": {
            "ksp_type": "chebyshev",
            "ksp_max_it": 2,
            "pc_type": "jacobi"},
        "pmg_mg_coarse": {
            "ksp_type": "preonly",
            "pc_type": "lu",
            "pc_factor_mat_solver_type": "mumps"
        }}

gt_levels_fancy = {"ksp_type": "richardson",
                    "ksp_max_it": 1,
                    "pc_type": "fieldsplit",
                    "pc_fieldsplit_type": "schur",
                    "pc_fieldsplit_schur_fact_type": "upper",
                    "fieldsplit_0_ksp_type": "richardson",
                    "fieldsplit_0_ksp_convergence_test": "skip",
                    "fieldsplit_0_ksp_max_it": 2,
                    "fieldsplit_0_ksp_richardson_self_scale": None,
                    "fieldsplit_0_pc_type": "bjacobi",
                    "fieldsplit_0_sub_pc_type": "ilu",
                    "fieldsplit_1_ksp_type": "richardson",
                    "fieldsplit_1_ksp_convergence_test": "skip",
                    "fieldsplit_1_ksp_richardson_self_scale": None,
                    "fieldsplit_1_ksp_max_it": 3,
                    "fieldsplit_1_pc_type": "python",
                    "fieldsplit_1_pc_python_type": "__main__.Mass",
                    "fieldsplit_1_aux_pc_type": "bjacobi",
                    "fieldsplit_1_aux_sub_pc_type": "icc"}
gt_levels_demo =  {'ksp_type': 'richardson',
                    'ksp_max_it': 2,
                    'pc_type': 'bjacobi',}
p1pcpatch = {"ksp_type": "gmres",
            "ksp_converged_reason": None,
            "pc_type": "python",
            "pc_python_type": "firedrake.P1PC",
            "pmg_mg_levels_ksp_type": "chebyshev",
            "pmg_mg_levels_ksp_norm_type": "unpreconditioned",
            "pmg_mg_levels_ksp_monitor_true_residual": None,
            "pmg_mg_levels_pc_type": "python",
            "pmg_mg_levels_pc_python_type": "firedrake.PatchPC",
            "pmg_mg_levels_patch": {
                "pc_patch_sub_mat_type": "aij",
                "pc_patch_save_operators": True,
                "pc_patch_construct_dim": 0,
                "pc_patch_construct_type": "star",
                "sub_ksp_type": "preonly",
                "sub_pc_type": "lu",
            },
            "pmg_mg_coarse": {
                "mat_type": "aij",
                "ksp_type": "preonly",
                "pc_type": "python",
                "pc_python_type": "firedrake.AssembledPC",
                "assembled_pc_type": "cholesky",
            }} # not implemented on extruded meshes
lumatfree = {"ksp_type": "preonly",
            "pc_type": "python",
            "pc_python_type": "firedrake.AssembledPC",
            "assembled_pc_type": "lu"}


# Parameters used in the cases of my setups
# 1) HELPER DICTs

# MG params
mgmatfree_mtf ={"snes_type": "ksponly",
                "ksp_type": "preonly",
                "mat_type": "matfree",
                "pc_type": "mg",
                "pc_mg_type": "full",
                "mg_coarse_ksp_type": "preonly",
                "mg_coarse_pc_type": "python",
                "mg_coarse_pc_python_type": "firedrake.AssembledPC",
                "mg_coarse_assembled_pc_type": "lu",
                # "mg_coarse_assembled_pc_factor_mat_solver_type": "mumps",
                # "mg_coarse_assembled_pc_mat_mumps_icntl_14": 200,
                "mg_levels_ksp_type": "chebyshev",
                "mg_levels_ksp_max_it": 3,
                "mg_levels_pc_type": "none"}

mgmatfree_mtx = {"snes_type": "ksponly",
                "ksp_type": "preonly",
                 "pc_type": "mg",
                 "pc_mg_type": "full",
                    # "mg_coarse_ksp_type": "preonly",
                    # "mg_coarse_pc_type": "python",
                    # "mg_coarse_pc_python_type": "firedrake.AssembledPC",
                    # "mg_coarse_assembled_ksp_type": "cg",
                    # "mg_coarse_assembled_pc_type": "jacobi",
                    # "mg_coarse_assembled_ksp_rtol": 1.e-10,
                 "mg_levels_ksp_type": "chebyshev",
                 "mg_levels_ksp_max_it": 3,
                 "mg_levels_pc_type": "none"}

mgmatexp = {'ksp_type': 'preonly',
            'pc_type': 'mg',
            'pc_mg_type': 'full',
            'mg_levels': {'ksp_type': 'chebyshev',
                          'pc_type': 'jacobi',
                          'ksp_max_it': 3}}

# Params for solves on levels
cheby_jacobi = {"ksp_type": "chebyshev",
                          "ksp_max_it": 3,
                          "pc_type": "jacobi"}
cheby_none = {"ksp_type": "chebyshev",
                    "ksp_max_it": 3,
                    "pc_type": "none"}

# Params for GTMG
gt_params_matexp = {'mg_levels': cheby_jacobi,
                    'mg_coarse': mgmatexp}
gt_params_global_matfree = {"mg_coarse": mgmatfree_mtf,
                            "mg_levels": cheby_none,
                            'mat_type': 'matfree'}
gt_params_fully_matfree = {"mg_coarse": mgmatfree_mtx,
                           "mg_levels": cheby_none,
                           'mat_type': 'matfree'}

# 2) FULL PARAMS
# Matrix explicit, direct hybridization
hybridization_lu_params = {'mat_type': 'matfree',
                           'ksp_type': 'preonly',
                           'pc_type': 'python',
                           'pc_python_type': 'firedrake.HybridizationPC',
                           'hybridization': {'ksp_type': 'cg', 'ksp_rtol': 1.e-8},
                           'ksp_view': None}

# Hyridization, globally matfree with CG, used in Thomas' matrix-free hybridization test
hybridization_global_matfree_cg =  {'mat_type': 'matfree',
                                    'ksp_type': 'preonly',
                                    'pc_type': 'python',
                                    'pc_python_type': 'firedrake.HybridizationPC',
                                    'hybridization': {'ksp_type': 'cg',
                                                     'pc_type': 'none',
                                                     'ksp_rtol': 1.e-8,
                                                     'mat_type': 'matfree'}}

# These are the tests used for Jacks GTMG test in the Firedrake test suite
gtmg_matexpl_params =  {'mat_type': 'matfree',
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
gtmg_global_matfree_params={'snes_type': 'ksponly',
                            'mat_type': 'matfree',
                            'ksp_type': 'preonly',
                            'pc_type': 'python',
                            'pc_python_type': 'firedrake.HybridizationPC',
                            'hybridization': {'ksp_type': 'cg',
                                                'pc_type': 'python',
                                                'mat_type': 'matfree', #!
                                                'pc_python_type': 'firedrake.GTMGPC',
                                                'ksp_rtol': 1.e-8,
                                                'gt': gt_params_global_matfree,
                                                'ksp_view': None}}

# These are the tests used for Jacks GTMG test in the Firedrake test suite
# with globally matrix-free solves on the levels and a nesting of schur complements on the trace solve
gtmg_global_matfree_nested_schur_params =  {'snes_type': 'ksponly',
                                            'mat_type': 'matfree',
                                            'ksp_type': 'preonly',
                                            'pc_type': 'python',
                                            'pc_python_type': 'firedrake.HybridizationPC',
                                            'hybridization': {'ksp_type': 'cg',
                                                                'pc_type': 'python',
                                                                'mat_type': 'matfree', #!
                                                                # nested schur option, but not locally matfree!
                                                                'localsolve': {'ksp_type': 'preonly',
                                                                                # 'mat_type': 'matfree',
                                                                                'pc_type': 'fieldsplit',
                                                                                'pc_fieldsplit_type': 'schur'},
                                                                'ksp_rtol': 1.e-8,
                                                                'ksp_max_it': 20,
                                                                'pc_python_type': 'firedrake.GTMGPC',
                                                                'gt': gt_params_global_matfree,
                                                                'ksp_view': None}}

# Fully matrix-free GTMG
# We need nested schur for local matfree
gtmg_fully_matfree_params ={'snes_type': 'ksponly',
                            'mat_type': 'matfree',
                            'ksp_type': 'preonly',
                            'pc_type': 'python',
                            'pc_python_type': 'firedrake.HybridizationPC',
                            'hybridization': {'ksp_type': 'cg',
                                              'pc_type': 'python',
                                              'mat_type': 'matfree',
                                              'ksp_rtol': 1.e-8,
                                              'ksp_max_it': 20,
                                              'localsolve': {'ksp_type': 'preonly',
                                                             'mat_type': 'matfree',  #local-matfree!
                                                             'pc_type': 'fieldsplit',
                                                             'pc_fieldsplit_type': 'schur'},
                                              'pc_python_type': 'firedrake.GTMGPC',
                                              'gt': gt_params_fully_matfree,
                                              'ksp_view': None}}
