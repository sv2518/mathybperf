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