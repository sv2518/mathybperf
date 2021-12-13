from firedrake import *
from firedrake.petsc import PETSc

def solve_with_params(a, L, W, solver_bag, deform, penalty_value, quadrature_degree):
    w = Function(W)
    vpb = LinearVariationalProblem(a, L, w)
    appctx={"deform": deform,
            "value": penalty_value,
            "quadrature_degree": quadrature_degree}
    appctx.update({"get_coarse_operator": solver_bag.p1_callback,
                   "get_coarse_space": solver_bag.get_p1_space,
                   "coarse_space_bcs": solver_bag.get_p1_prb_bcs()})
    solver = LinearVariationalSolver(vpb,
                                     solver_parameters=solver_bag.perform_params,
                                     appctx=appctx)
    with PETSc.Log.Event("perfsolve"):
        solver.solve()
    
    sigma_dc, u_dc = TrialFunctions(W)
    tau_dc, v_dc = TestFunctions(W)
    _, U_dc = W.split()
    f_dc = Function(U_dc)
    x = SpatialCoordinate(solver_bag.mesh)
    w_dc = Function(W).assign(w)
    assert w_dc != w, "Make sure we don't modify w"
    f_dc.interpolate(-2*(x[0]-1)*x[0] - 2*(x[1]-1)*x[1]- 2*(x[2]-1)*x[2])
    w_dc.sub(1).project(x[0]*(1-x[0])*x[1]*(1-x[1])*x[2]*(1-x[2]))
    A=Tensor((dot(sigma_dc, tau_dc) + div(tau_dc)*u_dc + div(sigma_dc)*v_dc)*dx)
    B=AssembledVector(w_dc)
    dat1 = assemble(A*B).dat.data[1]
    dat2 = assemble(-f_dc*v_dc*dx).dat.data[1]
    assert np.allclose(dat1, dat2), "Analytical solution is not correct"
    
    sigma_dc, u_dc = TrialFunctions(W)
    tau_dc, v_dc = TestFunctions(W)
    _, U_dc = W.split()
    f_dc = Function(U_dc)
    x = SpatialCoordinate(solver_bag.mesh)
    f_dc.interpolate(-2*(x[0]-1)*x[0] - 2*(x[1]-1)*x[1]- 2*(x[2]-1)*x[2])
    w_dc.sub(1).project(x[0]*(1-x[0])*x[1]*(1-x[1])*x[2]*(1-x[2]))
    A=Tensor((dot(sigma_dc, tau_dc) + div(tau_dc)*u_dc + div(sigma_dc)*v_dc)*dx)
    B=AssembledVector(w)
    dat1 = assemble(A*B).dat.data[1]
    dat2 = assemble(-f_dc*v_dc*dx).dat.data[1]
    assert np.allclose(dat1, dat2), "Iterative solution is not correct"

    assert np.allclose(w_dc.dat.data[0], w.dat.data[0], rtol=1.e-4)
    assert np.allclose(w_dc.dat.data[1], w.dat.data[1], rtol=1.e-4)

    return w, solver

def naive_solver(a, L, W, solver_bag):
    appctx = {"get_coarse_operator": solver_bag.p1_callback,
              "get_coarse_space": solver_bag.get_p1_space,
              "coarse_space_bcs": solver_bag.get_p1_prb_bcs()}

    w = Function(W)
    vpb = LinearVariationalProblem(a, L, w)
    solver = LinearVariationalSolver(vpb,
                                     solver_parameters=solver_bag.baseline_params,
                                     appctx=appctx)
    with PETSc.Log.Event("naivesolve"):
        solver.solve()

    return w
