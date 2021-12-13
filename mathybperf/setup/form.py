from firedrake import *
from mathybperf.utils.fem_utils import est_degree_calculation


def mixed_poisson(W, mesh, add_to_quad_degree, uexact):
    sigma, u = TrialFunctions(W)
    tau, v = TestFunctions(W)

    form = (dot(sigma, tau) + div(tau)*u + div(sigma)*v)

    # estimate the quadrature degree
    # and give user the freedom to increase the estimated degree
    est = enumerate(est_degree_calculation(form))
    quadrature_degree = tuple([d+add_to_quad_degree[c] for c, d in est])

    # build rhs from exact solution
    f = -div(grad(uexact))

    a = form*dx(degree=quadrature_degree)
    L = -f*v*dx(degree=quadrature_degree)
    return a, L, quadrature_degree
