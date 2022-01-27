from firedrake import *
import pandas as pd


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
        self.var_problem_repr = ""
        self.var_problem_info = {}
        self.total_local_shape = None

    def __str__(self):
        return ((f"\nPROBLEM SETUP:\n"
                 f"Approximation order: {self.order}\n"
                 f"Cells per dimension: {self.cells_per_dim}\n"
                 f"Deformation: {self.deformation}\n"
                 f"Cell scaling: {self.scaling}\n"
                 f"Cell deformation transformation: {self.affine_trafo}\n"
                 f"Quadrilateral cells?: {self.quadrilateral}\n"
                 f"Change to quadrature degree: {self.add_to_quad_degree}\n"
                 f"Type of the exact solution (and rhs): {self.exact_sol_type}\n")
                + self.var_problem_repr)

    def latex(self):
        data = {"Approximation order": f"{self.order}",
                "Cells per dimension": f"{self.cells_per_dim}",
                "Deformation": f"{self.deformation}",
                "Cell scaling": f"{self.scaling}",
                "Cell deformation transformation": f"{self.affine_trafo}",
                "Quadrilateral cells?": f"{self.quadrilateral}",
                "Change to quadrature degree": f"{self.add_to_quad_degree}",
                "Type of the exact solution (and rhs)": f"{self.exact_sol_type}"}
        data.update(self.var_problem_info)
        data["Domain"] = data["Domain"].replace("_", "\_")
        pd.set_option('display.max_colwidth', None)
        data["Lhs"] = data["Lhs"].replace("[v_0[0], v_0[1], v_0[2]]", "v_0")
        data["Lhs"] = data["Lhs"].replace("[v_1[0], v_1[1], v_1[2]]", "v_1")
        data["Lhs"] = data["Lhs"].replace("div", "\Delta")
        data["Lhs"] = data["Lhs"].replace("grad", "\nabla")
        data["Lhs"] = data["Lhs"].replace("*", "\cdot")
        data["Lhs"] = data["Lhs"].replace(".", "\cdot")
        data["Lhs"] = "$"+data["Lhs"]+"$"
        data["Rhs"] = data["Rhs"].replace("+ -1 *", "-")
        data["Rhs"] = data["Rhs"].replace("div", "\Delta")
        data["Rhs"] = data["Rhs"].replace("grad", "\nabla")
        data["Lhs"] = data["Lhs"].replace("*", "\cdot")
        data["Lhs"] = data["Lhs"].replace(".", "\cdot")
        data["Rhs"] = "$"+data["Rhs"]+"$"
        return pd.DataFrame(data, index=[0]).T.to_latex(header=None, escape=False)
