from firedrake import *
from firedrake.petsc import PETSc


def solve_with_params(problem_bag, solver_bag):
    penalty_value = problem_bag.penalty(problem_bag.order, problem_bag.deformation)
    a, L, quadrature_degree = problem_bag.var_problem
    W, _, _ = problem_bag.space

    local_matfree = False
    fcp = None
    approx_inner_schur=False
    if ("hybridization" in solver_bag.perform_params.keys() 
        and "localsolve" in solver_bag.perform_params["hybridization"].keys()):
        if (("mat_type" in solver_bag.perform_params["hybridization"]["localsolve"].keys()) and
            solver_bag.perform_params["hybridization"]["localsolve"]["mat_type"] == "matfree"):
            local_matfree = True
            fcp = {"slate_compiler": {"replace_mul": True}}
        if solver_bag.perform_params["hybridization"]["localsolve"]["approx"]:
            approx_inner_schur=True

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
        PETSc.Sys.pushErrorHandler("ignore")
        try:
            solver.solve()
            if solver.snes.ksp.getIterationNumber()!=1 and not approx_inner_schur:
                raise Exception("In the solver options you specified that you want the local solvers to be exact enough,\
                                but the outer solver turns out to need more than 1 iteration.\
                                So you might want to put the tolerances lower on the local solver to make it more accurate.")
        except Exception as e:
            raise e
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
