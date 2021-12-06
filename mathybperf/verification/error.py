from firedrake import *
import numpy as np


def check_error(w, w2):
    sigma, u = w.split()
    sigma2, u2 = w2.split()
    norm = errornorm(sigma, sigma2, norm_type="L2")
    assert np.allclose(sigma.dat.data, sigma2.dat.data, atol=1.e-2), norm
    norm = errornorm(u, u2, norm_type="L2")
    assert np.allclose(u.dat.data, u2.dat.data, atol=1.e-2), norm
