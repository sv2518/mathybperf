from firedrake import *
from firedrake.petsc import PETSc


def solve_with_params(problem_bag, solver_bag):
    penalty_value = problem_bag.penalty(problem_bag.order, problem_bag.deformation)
    a, L, quadrature_degree = problem_bag.var_problem
    W, _, _ = problem_bag.space

    w = Function(W)
    vpb = LinearVariationalProblem(a, L, w)
    appctx = {"deform": problem_bag.deformation,
              "value": penalty_value,
              "quadrature_degree": quadrature_degree,
              "get_coarse_operator": solver_bag.p1_callback,
              "get_coarse_space": solver_bag.get_p1_space,
              "coarse_space_bcs": solver_bag.get_p1_prb_bcs()}
    solver = LinearVariationalSolver(vpb,
                                     solver_parameters=solver_bag.perform_params,
                                     appctx=appctx)
    with PETSc.Log.Event("perfsolve"):
        solver.solve()
    return w, solver


def naive_solver(a, L, W, solver_bag):
    appctx = {"get_coarse_operator": solver_bag.p1_callback,
              "get_coarse_space": solver_bag.get_p1_space,
              "coarse_space_bcs": solver_bag.get_p1_prb_bcs()}

    z = Function(W)
    vpb = LinearVariationalProblem(a, L, z)
    solver = LinearVariationalSolver(vpb,
                                     solver_parameters=solver_bag.baseline_params,
                                     appctx=appctx)
    with PETSc.Log.Event("naivesolve"):
        solver.solve()

    return z, solver
