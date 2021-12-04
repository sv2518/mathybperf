from firedrake import *


def est_degree_calculation(form):
    from ufl.algorithms import estimate_total_polynomial_degree
    from tsfc.ufl_utils import compute_form_data

    # preprocess to lower compund operators
    fd = compute_form_data(form*dx, do_estimate_degrees=True)
    itg_data, = fd.integral_data
    integral, = itg_data.integrals
    integrand = integral.integrand()

    # then estimate degree for the preprocessed form
    return estimate_total_polynomial_degree(integrand)
