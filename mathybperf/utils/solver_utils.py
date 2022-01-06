from firedrake import *

class SolverBag(object):

    def __init__(self, perform_params, baseline_params, gtmg_levels):
        self.perform_params = perform_params
        self.baseline_params = baseline_params
        self.levels = gtmg_levels
        self.mesh = None

    def get_p1_space(self):
        return FunctionSpace(self.mesh, "CG", 1)

    def get_p1_prb_bcs(self):
        return [DirichletBC(self.get_p1_space(), zero(), "on_boundary"),
                DirichletBC(self.get_p1_space(), zero(), "top"),
                DirichletBC(self.get_p1_space(), zero(), "bottom")]

    def p1_callback(self):
        P1 = self.get_p1_space()
        p = TrialFunction(P1)
        q = TestFunction(P1)
        return inner(grad(p), grad(q))*dx

    def exact_solution(self, L):
        x = SpatialCoordinate(self.mesh)
        return x[0]*(L-x[0])*x[1]*(L-x[1])*x[2]*(L-x[2]) * exp(L-x[0]+1)