from firedrake import *
import numpy as np


def check_error(w, w2):
    sigma, u = w.split()
    sigma2, u2 = w2.split()
    norm = errornorm(sigma, sigma2, norm_type="L2")
    assert np.allclose(sigma.dat.data, sigma2.dat.data, atol=1.e-2), norm
    norm = errornorm(u, u2, norm_type="L2")
    assert np.allclose(u.dat.data, u2.dat.data, atol=1.e-2), norm

def get_errors(w, w2):
    linf_err_u = max(abs(assemble(w.sub(0) - w2.sub(0)).dat.data))
    linf_err_p = max(abs(assemble(w.sub(1) - w2.sub(1)).dat.data))
    l2_err_u = errornorm(w.sub(0), w2.sub(0), "L2")
    l2_err_p = errornorm(w.sub(1), w2.sub(1), "L2")
    hdiv_err_u = errornorm(w.sub(0), w2.sub(0), "hdiv")
    h1_err_p = errornorm(w.sub(1), w2.sub(1), "H1")
    return ((linf_err_u, linf_err_p),
            (l2_err_u, l2_err_p),
            (hdiv_err_u, h1_err_p))
