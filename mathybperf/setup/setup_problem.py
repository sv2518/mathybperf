from .mesh import mesh_3D
from .form import mixed_poisson
from .space import RT_DQ_3D
from .solver import solve_with_params
from mathybperf.verification.error import check_error, check_var_problem, project_trace_solution
from mathybperf.verification.geometric import check_facetarea_and_cellvolume
from firedrake import *
import ufl

def problem(problem_bag, solver_bag, verification, new=True, project=False):
    reset = not problem_bag.mesh or new  # setup new problem
    if reset:
        problem_bag.mesh = mesh_3D(problem_bag, solver_bag.levels)
        solver_bag.mesh = problem_bag.mesh

    # calculate exact solution on the new mesh before we setup the forms because we do MMS
    exact_sol = solver_bag.exact_solution(problem_bag.scaling, problem_bag.exact_sol_type)

    if reset:
        problem_bag.space = RT_DQ_3D(problem_bag.order, problem_bag.mesh)
        problem_bag.var_problem, problem_bag.var_problem_repr, problem_bag.var_problem_info = mixed_poisson(problem_bag.space[0],
                                                                              problem_bag.add_to_quad_degree,
                                                                              exact_sol)
    
    # solve problem
    a, L, quadrature_degree = problem_bag.var_problem
    w, solver = solve_with_params(problem_bag, solver_bag)

    # compare iterative solution to reference solution
    w_t = solver.snes.ksp.pc.getPythonContext().trace_solution
    problem_bag.total_local_shape=solver.snes.ksp.pc.getPythonContext().schur_builder.total_local_shape
    w_t_exact = None
    w2 = None
    if project:
        w2 = Function(problem_bag.space[0])
        w2.sub(0).project(ufl.grad(exact_sol))
        w2.sub(1).project(exact_sol)
        w_t_exact = project_trace_solution(w_t.function_space(), exact_sol)

    # verification of error
    if verification:
        # check some geometric quantities
        if problem_bag.deformation == [0]:
            check_facetarea_and_cellvolume(problem_bag.space[2])

        # plug iterative solution in the variational problem
        check_var_problem(a, L, w)

        # double check that the reference solution is solving the variational problem
        check_var_problem(a, L, w2.sub(1))

        # compare iterative to reference solution
        check_error(w, w2)

    return quadrature_degree, (w, w2), (w_t, w_t_exact), solver_bag.mesh