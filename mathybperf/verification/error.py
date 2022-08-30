from firedrake import *
import numpy as np
import matplotlib.pyplot as plt


def check_error(w, w2, threshold):
    """Checks the error of the solution w against the reference solution w2."""
    sigma, u = w.split()
    sigma2, u2 = w2.split()
    norm = errornorm(sigma, sigma2, norm_type="L2")
    assert norm < threshold or norm < 1e-5
    norm = errornorm(u, u2, norm_type="L2")
    assert norm < threshold or norm < 1e-5


def get_errors(w, w2):
    """Returns error of mixed function in various norms."""
    linf_err_u = max(abs(assemble(w.sub(0) - w2.sub(0)).dat.data))
    linf_err_p = max(abs(assemble(w.sub(1) - w2.sub(1)).dat.data))
    l2_err_u = errornorm(w.sub(0), w2.sub(0), "L2")
    l2_err_p = errornorm(w.sub(1), w2.sub(1), "L2")
    hdiv_err_u = errornorm(w.sub(0), w2.sub(0), "hdiv")
    h1_err_p = errornorm(w.sub(1), w2.sub(1), "H1")
    return {"LinfPres": linf_err_p,
            "LinfVelo": linf_err_u,
            "L2Pres": l2_err_p,
            "L2Velo": l2_err_u,
            "H1Pres": h1_err_p,
            "HDivVelo": hdiv_err_u}


def get_error(w, ref, area, filename):
    """Returns error of not function of the trace."""
    plt.figure()
    plt.plot(w.dat.data, label="trace sol")
    plt.plot(ref.dat.data, label="trace ref")
    plt.legend()
    plt.savefig(filename)
    l2_err_p = sqrt(assemble(area* ( w -  ref) * ( w -   ref) * ds_v
                            +area*  ( w -   ref) * ( w -   ref) * ds_t
                            +area* ( w -   ref) * ( w -   ref) * ds_b
                            +area* ( w('+') -   ref('+')) * ( w('+') -   ref('+')) * dS_h
                            +area* ( w('+') -   ref('+')) * ( w('+') -   ref('+')) * dS_v))
    return {"L2Trace": l2_err_p}


def check_var_problem(a, L, w, threshold):
    """Double-checks that the solution is solving the variational problem"""
    sol = assemble(action(a, w))
    rhs = assemble(L)
    norm = errornorm(sol.sub(0), rhs.sub(0), norm_type="L2")
    assert  norm < threshold or norm < 1e-5, "Velocity in solution does not solve the variational problem. The errornorm is "+str(norm)
    norm = errornorm(sol.sub(1), rhs.sub(1), norm_type="L2") 
    assert norm < threshold or norm < 1e-5, "Pressure in solution does not solve the variational problem. The errornorm is "+str(norm)


def project_trace_solution(T, exact_sol, degree):
    lmbda_t = TrialFunction(T)
    gamma_t = TestFunction(T)
    a_t = (lmbda_t * gamma_t * ds_t(degree=degree)
           + lmbda_t * gamma_t * ds_v(degree=degree)
           + lmbda_t * gamma_t * ds_b(degree=degree)
           + lmbda_t('+') * gamma_t('+') * dS_h(degree=degree)
           + lmbda_t('+') * gamma_t('+') * dS_v(degree=degree))
    l_t = (exact_sol * gamma_t * ds_t(degree=degree)
           + exact_sol * gamma_t * ds_v(degree=degree)
           + exact_sol * gamma_t * ds_b(degree=degree)
           + exact_sol('+') * gamma_t('+') * dS_h(degree=degree)
           + exact_sol('+') * gamma_t('+') * dS_v(degree=degree))

    w_t_exact = Function(T)
    vpb_t = LinearVariationalProblem(lhs(a_t-l_t), rhs(a_t-l_t), w_t_exact)
    params = {"ksp_type": "cg", "ksp_rtol": 1e-6, "ksp_rtol": 1e-9, "pc_type": "bjacobi", "sub_pc_type": "icc"}
    solver_t = LinearVariationalSolver(vpb_t, solver_parameters=params)
    solver_t.solve()
    return w_t_exact
