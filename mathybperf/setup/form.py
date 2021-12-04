from firedrake import *
from mathybperf.utils.fem_utils import est_degree_calculation


def mixed_poisson(W, mesh, add_to_quad_degree):
    sigma, u = TrialFunctions(W)
    tau, v = TestFunctions(W)
    V, U = W.split()
    f = Function(U)
    x, y, z = SpatialCoordinate(mesh)
    expr = (1+12*pi*pi)*cos(100*pi*x)*cos(100*pi*y)*cos(100*pi*z)
    f.interpolate(expr)

    form = (dot(sigma, tau) + div(tau)*u + div(sigma)*v)

    # estimate the quadrature degree
    # and give user the freedom to increase the estimated degree
    est = enumerate(est_degree_calculation(form))
    quadrature_degree = tuple([d+add_to_quad_degree[c] for c, d in est])

    a = form*dx(degree=quadrature_degree)
    L = -f*v*dx(degree=quadrature_degree)
    return a, L, quadrature_degree
