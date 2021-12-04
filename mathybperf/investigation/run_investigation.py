from firedrake import *
from firedrake.slate.static_condensation import hybridization
import numpy as np
from mathybperf import *

def run_test(deformations, orders, scalings, itmaxs, penalty, affine_trafo, add_to_quad_degree, number):
    dofs = np.zeros(len(orders))
    konditionnumberlist = []
    eigenvaluelist = []
    outeritslist = []
    totalitslist = []
    dofslist = []
    results_outer_its = np.zeros([len(itmaxs), len(orders), len(scalings)])
    results_total_its = np.zeros([len(itmaxs), len(orders), len(scalings)])

    for h, deform in enumerate(deformations):
        konditionnumbers = []
        eigenvals = []
        totalits = []
        outerits = []
        quaddegreelist = []
        for i, p in enumerate(orders):
            for j, s in enumerate(scalings):
                for k, itmax in enumerate(itmaxs):

                    # preconditioner penalty
                    penalty_value = penalty(p, deform)

                    # problem setup
                    mesh = mesh_3D(s, deform, affine_trafo, True)
                    W, U, V = RT_DQ_3D(p, mesh)
                    a, L, quadrature_degree = mixed_poisson(W, mesh, add_to_quad_degree)

                    # just some checks
                    if not deformations:
                        check_facetarea_and_cellvolume(U)

                    # some analysis
                    analytics_mixed = Analytics(a)
                    _, wmin, wmax = analytics_mixed.eigenvalues()
                    eigenvals.append((wmin, wmax))
                    konditionnumbers.append(analytics_mixed.condition_number())
                    print("Mixed poisson spd?", analytics_mixed.spd())
                    print("Mixed poisson singular?", analytics_mixed.singular())
                    print("Mixed poisson condition number", analytics_mixed.condition_number)

                    AB = Tensor(a).blocks
                    S = AB[1, 1] - AB[1, 0] * AB[0, 0].inv * AB[0, 1]
                    analytics_schur = Analytics(S)
                    print("Schur spd?", analytics_schur.spd())
                    print("Schur singular?", analytics_schur.singular())
                    print("Schur condition number", analytics_schur.condition_number)

                    analytics_vmass = Analytics(A[0, 0])
                    print("Velocity mass spd?", analytics_vmass.spd())
                    print("Velocity mass singular?", analytics_vmass.singular())
                    print("Velocity mass condition number", analytics_vmass.condition_number)

                    try:
                        w, solver = solve_with_params(a, L, W, params, deform, penalty_value, quadrature_degree)
                        outer_its = solver.snes.ksp.its
                        pcs = solver.snes.ksp.pc.getFieldSplitSubKSP()
                        fsp0_its =  pcs[0].its
                        fsp1_its =  pcs[1].its
                        results_total_its[k][i][j] = outer_its*(fsp0_its+fsp1_its*fsp0_its)
                        results_outer_its[k][i][j] = outer_its

                        velo, pres = w.split()
                        f1 = File("visualisation/poisson_mixed_velocity_"+str(p)+".pvd")
                        f1.write(velo)
                        f2 = File("visualisation/poisson_mixed_pressure_"+str(p)+".pvd", project_output=True)
                        f2.write(pres)

                    except Exception as e:
                        # check that aborted bc of divergence
                        if solver.snes.diverged or solver.snes.ksp.diverged or pcs[0].diverged or pcs[1].diverged:
                            results_total_its[k][i][j] = -1
                            results_outer_its[k][i][j] = -1
                        else:
                            results_total_its[k][i][j] = -2
                            results_outer_its[k][i][j] = -2

                    # in case chebyshev is preconditioner,
                    # multiply the fieldsplit solver itations by chebyshev iterations
                    try:
                        fsp0_cheby_its = params["fieldsplit_0_aux_ksp_ksp_max_it"]
                        fsp0_its *= fsp0_cheby_its
                    except:
                        pass
                    try:
                        fsp1_cheby_its = params["fieldsplit_1_aux_ksp_ksp_max_it"]
                        fsp1_its *= fsp1_cheby_its
                    except:
                        pass

                    # verification of error
                    w2 = naive_solver(a, L, W, p)
                    check_error(w, w2)

            outerits.append(results_outer_its[0][i][0])
            totalits.append(results_total_its[0][i][0])
            dofs[i] = solver.snes.vec_sol.local_size
            quaddegreelist.append(quadrature_degree)

        konditionnumberlist.append(konditionnumbers)
        eigenvaluelist.append(eigenvals)
        outeritslist.append(outerits)
        totalitslist.append(totalits)

    dofslist = [dofs] * len(deformations)

    # write data to csv file
    write_investigation_data([dofslist, eigenvaluelist, konditionnumberlist, outeritslist, totalitslist],
                             name+".csv",
                             deformations)

    #  Plots
    plotter = ResultPlotter()
    # plotter.plot_its_vs_scaling_fororder(name, orders, dofs, scalings, results_total_its, params, its_type="total")
    # # plotter.plot_its_vs_scaling_fororder(name, orders, dofs, scalings, results_outer_its, params, its_type="outer")
    plotter.plot_deformation_vs_its_fororder(name, orders, dofs, deformations, totalitslist, konditionnumberlist, params, quaddegreelist, its_type="total")



##### !!!!
# setup test
params = parameters_changemaxits_schur_cg_jacobi_cg_jacobi
penalty = lambda p, d: (p+1)**3
test = "(p+1)**3"
degree = range(6)
scalings = list([1.0])
itmaxs = [4]
deformations = [] #0.5*d for d in range(0,21)
affine_trafo = True

# setup plotting output
folder = "results/mixed_poisson/"
type = "affine/" if deformations and affine_trafo else "nonaffine/" if deformations else "nodeform/"
##### !!!!
for c, add_to_quad_degree in enumerate([(i, i) for i in range(1)]):
    case = test # + "_addtodeg" + str(add_to_quad_degree)
    name =  folder + type + case
    try:
        os.makedirs(name)
    except FileExistsError:
        pass
    run_test(deformations, degree, scalings, itmaxs, penalty, affine_trafo, add_to_quad_degree, c)