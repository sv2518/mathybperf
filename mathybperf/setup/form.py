from firedrake import *
from mathybperf.utils.fem_utils import est_degree_calculation


def mixed_poisson(W, add_to_quad_degree, exact):
    sigma, u = TrialFunctions(W)
    tau, v = TestFunctions(W)

    form = (dot(sigma, tau) + div(tau)*u + div(sigma)*v)

    # estimate the quadrature degree
    # and give user the freedom to increase/decrease the estimated degree
    est = enumerate(est_degree_calculation(form))
    quadrature_degree = tuple([d+add_to_quad_degree[c] for c, d in est])

    # Method of manufactured solution: build rhs from exact solution
    f = -div(grad(exact))

    a = form*dx(degree=quadrature_degree)
    L = -f*v*dx(degree=quadrature_degree)
    repr = (
            f"\nVARIATIONAL PROBLEM\n"
            f"Trial functions: {sigma} and {u}\n"
            f"Test functions: {tau} and {v}\n"
            f"Lhs: {a}\n"
            f"Rhs: {L}\n"
            f"Quadrature degree: {quadrature_degree}\n"
           )
    return (a, L, quadrature_degree), repr
