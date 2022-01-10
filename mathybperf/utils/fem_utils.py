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


class ProblemBag(object):
    
    def __init__(self, deformation, scaling, affine_trafo, quadrilateral,
                 order, add_to_quad_degree, penalty, cells_per_dim,
                 exact_sol_type):
        self.deformation = deformation
        self.scaling = scaling
        self.affine_trafo = affine_trafo
        self.quadrilateral = quadrilateral
        self.order = order
        self.add_to_quad_degree = add_to_quad_degree
        self.penalty = penalty
        self.cells_per_dim = cells_per_dim
        self.exact_sol_type = exact_sol_type
        self.mesh = None
        self.space = None
        self.var_problem = None
