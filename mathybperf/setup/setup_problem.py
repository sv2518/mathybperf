from .mesh import mesh_3D
from .form import mixed_poisson
from .space import RT_DQ_3D
from .solver import solve_with_params, naive_solver
from mathybperf.verification.error import check_error


def problem(problem_bag, solver_bag, verification, new=True):
    # setup poblem
    penalty_value = problem_bag.penalty(problem_bag.order, problem_bag.deformation)
    problem_bag.mesh = (mesh_3D(problem_bag.cells_per_dim, problem_bag.scaling,
                        problem_bag.deformation, problem_bag.affine_trafo,
                        problem_bag.quadrilateral) if not problem_bag.mesh or new else problem_bag.mesh)
    W, U, V = RT_DQ_3D(problem_bag.order, problem_bag.mesh) if not problem_bag.space or new else problem_bag.space
    problem_bag.space =  W, U, V 
    a, L, quadrature_degree = (mixed_poisson(W, problem_bag.mesh, problem_bag.add_to_quad_degree)
                               if not problem_bag.var_problem or new else problem_bag.var_problem)
    problem_bag.var_problem = a, L, quadrature_degree

    # solve problem
    solver_bag.mesh = problem_bag.mesh
    w, solver = solve_with_params(a, L, W, solver_bag, problem_bag.deformation,
                                  penalty_value, quadrature_degree)

    # verification of error
    if verification:
        # if problem_bag.deformation == 0:
        #     check_facetarea_and_cellvolume(U)
        w2 = naive_solver(a, L, W, solver_bag)
        check_error(w, w2)
    return  a, solver, quadrature_degree, (w, w2), solver_bag.mesh