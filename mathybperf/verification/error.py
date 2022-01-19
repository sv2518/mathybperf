from firedrake import *
import numpy as np


def check_error(w, w2):
    """Checks the error of the solution w against the reference solution w2."""
    sigma, u = w.split()
    sigma2, u2 = w2.split()
    norm = errornorm(sigma, sigma2, norm_type="L2")
    assert np.allclose(sigma.dat.data, sigma2.dat.data, rtol=1.e-6), norm
    norm = errornorm(u, u2, norm_type="L2")
    assert np.allclose(u.dat.data, u2.dat.data, rtol=1.e-6), norm

def get_errors(w, w2):
    """Returns error in various norms."""
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

def get_error(w, w2):
    import matplotlib.pyplot as plt
    linf_err_p = max(abs(assemble(w - w2).dat.data))
    l2_err_p = np.sqrt(np.sum(np.abs(d1 - d2) for d1, d2 in zip(w.dat.data, w2.dat.data)))
    return {"LinfTrace": linf_err_p,
            "L2Trace": l2_err_p}


def check_var_problem(a, L, w):
    """Double-checks that the solution is solving the variational problem"""
    A = Tensor(a)
    B = AssembledVector(w)
    dat1 = assemble(A*B).dat.data
    dat2 = assemble(L).dat.data
    assert np.allclose(dat1[0], dat2[0], rtol=1.e-6), "Velocity in solution does not solve the variational problem."
    assert np.allclose(dat1[1], dat2[1], rtol=1.e-6), "Pressure in solution does not solve the variational problem."


def project_trace_solution(T, exact_sol, degree):
    lmbda_t = TrialFunction(T)
    gamma_t = TestFunction(T)
    a_t = (lmbda_t * gamma_t * ds_t(degree=degree) +
            lmbda_t * gamma_t * ds_v(degree=degree) +
            lmbda_t * gamma_t * ds_b(degree=degree) +
            lmbda_t('+') * gamma_t('+') * dS_h(degree=degree) +
            lmbda_t('+') * gamma_t('+') * dS_v(degree=degree))
    l_t = (exact_sol * gamma_t * ds_t(degree=degree) +
            exact_sol * gamma_t * ds_v(degree=degree) +
            exact_sol * gamma_t * ds_b(degree=degree) +
            exact_sol('+') * gamma_t('+') * dS_h(degree=degree) +
            exact_sol('+') * gamma_t('+') * dS_v(degree=degree))

    w_t_exact = Function(T)
    vpb_t = LinearVariationalProblem(lhs(a_t-l_t), rhs(a_t-l_t), w_t_exact)
    solver_t = LinearVariationalSolver(vpb_t, solver_parameters={'ksp_rtol': 1.e-6})
    solver_t.solve()
    return w_t_exact