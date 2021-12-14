from firedrake import *
import numpy as np


def check_error(w, w2):
    """Checks the error of the solution w against the reference solution w2."""
    sigma, u = w.split()
    sigma2, u2 = w2.split()
    norm = errornorm(sigma, sigma2, norm_type="L2")
    assert np.allclose(sigma.dat.data, sigma2.dat.data, rtol=1.e-2), norm
    norm = errornorm(u, u2, norm_type="L2")
    assert np.allclose(u.dat.data, u2.dat.data, atol=1.e-2), norm

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

