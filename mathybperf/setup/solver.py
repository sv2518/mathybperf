from firedrake import *


def solve_with_params(a, L, W, parameters, deform, penalty_value, quadrature_degree):
    w = Function(W)
    vpb = LinearVariationalProblem(a, L, w)
    solver = LinearVariationalSolver(vpb,
                                     solver_parameters=parameters,
                                     appctx={"deform": deform,
                                             "value": penalty_value,
                                             "quadrature_degree": quadrature_degree})
    solver.solve()
    return w, solver


def naive_solver(a, L, W):
    parameters = {"ksp_type": "gmres",
                  "ksp_gmres_restart": 100,
                  "ksp_rtol": 1e-8,
                  "pc_type": "ilu"}

    A = assemble(a)
    solver = LinearSolver(A, solver_parameters=parameters)

    w = Function(W)
    b = assemble(L)
    solver.solve(w, b)

    return w
