from .mesh import mesh_3D
from .form import mixed_poisson
from .space import RT_DQ_3D
from .solver import solve_with_params, naive_solver
from mathybperf.verification.error import check_error
from firedrake import Function
from ufl import grad

def problem(problem_bag, solver_bag, verification, new=True):
    # setup poblem
    penalty_value = problem_bag.penalty(problem_bag.order, problem_bag.deformation)
    problem_bag.mesh = (mesh_3D(problem_bag.cells_per_dim, problem_bag.scaling,
                        problem_bag.deformation, problem_bag.affine_trafo,
                        problem_bag.quadrilateral, solver_bag.levels) if not problem_bag.mesh or new else problem_bag.mesh)
    solver_bag.mesh = problem_bag.mesh
    W, U, V = RT_DQ_3D(problem_bag.order, solver_bag.mesh) if not problem_bag.space or new else problem_bag.space
    problem_bag.space =  W, U, V 
    a, L, quadrature_degree = (mixed_poisson(W, problem_bag.add_to_quad_degree,
                                             solver_bag.exact_solution(problem_bag.scaling))
                               if not problem_bag.var_problem or new else problem_bag.var_problem)
    problem_bag.var_problem = a, L, quadrature_degree
    w, solver = solve_with_params(a, L, W, solver_bag, problem_bag.deformation,
                                  penalty_value, quadrature_degree)

    # verification of error
    if verification:
        # check some geometric quantities
        if problem_bag.deformation == [0]:
            check_facetarea_and_cellvolume(problem_bag.space[2])

        # plug iterative solution in the variational problem
        check_var_problem(a, L, w)
    
        # compare iterative solution to reference solution
        w2 = Function(problem_bag.space[0])
        w2.sub(0).project(ufl.grad(exact_sol))
        w2.sub(1).project(exact_sol)

        # get error for trace solution too
        w_t = solver.snes.ksp.pc.getPythonContext().trace_solution
        w_t_exact = project_trace_solution(w_t.function_space(), exact_sol)

        # double check that the reference solution is solving the variational problem
        check_var_problem(a, L, w2.sub(1))

        # compare iterative to reference solution
        check_error(w, w2)
    else: 
        w2 = None
    return  a, solver, quadrature_degree, (w, w2), solver_bag.mesh