from firedrake import *
import numpy as np
from mathybperf import *
from mathybperf.utils.solver_utils import SolverBag
import os


def run_test(deformations, orders, penalty, affine_trafo, add_to_quad_degree, params, name, type):
    dofs = np.zeros(len(orders))
    konditionnumberlist_mixed = []
    konditionnumberlist_A00 = []
    konditionnumberlist_Schur = []
    eigenvaluelist = []
    outeritslist = []
    totalitslist = []
    fsp0itslist = []
    fsp1itslist = []

    for deform in deformations:
        konditionnumbers_mixed = []
        konditionnumbers_Schur = []
        konditionnumbers_A00 = []
        results_outer_its = []
        results_total_its = []
        results_fsp0_its = []
        results_fsp1_its = []
        eigenvals = []
        quaddegreelist = []
        s = deform if type == "scaling" else 1
        deform = 1 if type == "scaling" else deform
        for i, p in enumerate(orders):
            try:
                # Problem setup and solve
                problem_bag = ProblemBag(deform, s, affine_trafo, True,
                                         p, add_to_quad_degree, penalty, 1, "quadratic")
                solver_bag = SolverBag(params, None, None)
                _, _, _, _, solver = problem(problem_bag,
                                             solver_bag,
                                             verification=True,
                                             project=False)
                a, L, quadrature_degree = problem_bag.var_problem

                # Some analytics
                analytics_mixed = Analytics(a)
                _, wmin, wmax = analytics_mixed.eigenvalues()
                eigenvals.append((wmin, wmax))
                konditionnumbers_mixed.append(analytics_mixed.condition_number())
                # print("Mixed poisson spd?", analytics_mixed.spd())
                # print("Mixed poisson singular?", analytics_mixed.singular())

                AB = Tensor(a).blocks
                S = AB[1, 1] - AB[1, 0] * AB[0, 0].inv * AB[0, 1]
                analytics_schur = Analytics(S)
                konditionnumbers_Schur.append(analytics_schur.condition_number())
                # print("Schur spd?", analytics_schur.spd())
                # print("Schur singular?", analytics_schur.singular())

                analytics_vmass = Analytics(AB[0, 0])
                konditionnumbers_A00.append(analytics_vmass.condition_number())
                # print("Velocity mass spd?", analytics_vmass.spd())
                # print("Velocity mass singular?", analytics_vmass.singular())

                # Iteration counts
                outer_its = solver.snes.ksp.its
                pcs = solver.snes.ksp.pc.getFieldSplitSubKSP()
                fsp0_its = pcs[0].its
                fsp1_its = pcs[1].its
                results_total_its.append(outer_its*(fsp1_its+fsp1_its*fsp0_its))
                results_outer_its.append(outer_its)
                results_fsp0_its.append(fsp0_its)
                results_fsp1_its.append(fsp1_its)

                # Visualisation of solutions on the deformed cells
                # velo, pres = w.split()
                # f1 = File("mathybperf/investigation/visualisation/poisson_mixed_velocity_"+str(p)+".pvd")
                # f1.write(velo)
                # f2 = File("mathybperf/investigation/visualisation/poisson_mixed_pressure_"+str(p)+".pvd", project_output=True)
                # f2.write(pres)

            except Exception as e:
                # check that aborted bc of divergence
                if solver.snes.diverged or solver.snes.ksp.diverged or pcs[0].diverged or pcs[1].diverged:
                    results_total_its.append(-1)
                    results_outer_its.append(-1)
                    results_fsp0_its.append(-1)
                    results_fsp1_its.append(-1)
                else:
                    results_total_its.append(-2)
                    results_outer_its.append(-2)
                    results_fsp0_its.append(-2)
                    results_fsp1_its.append(-2)

            dofs[i] = solver.snes.vec_sol.local_size
            quaddegreelist.append(list(int(q) for q in quadrature_degree))

        outeritslist.append(results_outer_its)
        totalitslist.append(results_total_its)
        fsp0itslist.append(results_fsp0_its)
        fsp1itslist.append(results_fsp1_its)
        konditionnumberlist_mixed.append(konditionnumbers_mixed)
        konditionnumberlist_Schur.append(konditionnumbers_Schur)
        konditionnumberlist_A00.append(konditionnumbers_A00)
        eigenvaluelist.append(eigenvals)

    # write data to csv file
    data_per_defo = [eigenvaluelist, konditionnumberlist_mixed,
                     konditionnumberlist_A00, konditionnumberlist_Schur,
                     outeritslist, totalitslist,
                     fsp0itslist, fsp1itslist,
                     deformations]
    names_per_defo = ["eigs",
                      "kond_mixed", "kond_A00", "kond_Schur",
                      "outer_its", "total_its",
                      "deformations"]
    write_investigation_data(data_per_defo,
                             name+"_per_deformation.csv",
                             names_per_defo,
                             ["deformation from 1.0 in percentage : %d"
                              % (d*100) for d in deformations])

    data_per_order = [orders, dofs, quaddegreelist, [params]*len(orders)]
    names_per_order = ["orders", "dofs", "quad_degree", "params"]
    write_investigation_data(data_per_order,
                             name+"_per_order.csv",
                             names_per_order)


# !!!!


params = {"mat_type": "matfree",
          "snes_type": "ksponly",
          "ksp_type": "fgmres",
          "ksp_rtol": 1.0e-6,
          "ksp_atol": 1.0e-6,
          "pc_type": "fieldsplit",
          "pc_fieldsplit_type": "schur",
          "pc_fieldsplit_schur_fact_type": "full",
          "fieldsplit_0_ksp_type": "cg",
          "fieldsplit_0_pc_type": "jacobi",
          "fieldsplit_0_ksp_rtol": 1e-10,
          "fieldsplit_0_ksp_atol": 1e-10,
          "fieldsplit_0_ksp_max_it": 2000,
          "fieldsplit_0_ksp_monitor": None,
          "fieldsplit_1_ksp_type": "cg",
          "fieldsplit_1_pc_type": "python",
          "fieldsplit_1_pc_python_type": DGLaplacian.__module__ + ".DGLaplacian",  # defined in utils/auxiliary
          "fieldsplit_1_ksp_rtol": 1e-8,
          "fieldsplit_1_ksp_atol": 1e-8,
          "fieldsplit_1_ksp_max_it": 2000,
          "fieldsplit_1_aux_pc_type": "jacobi",
          "fieldsplit_1_ksp_monitor": None,
          "ksp_monitor": None,
          }


for type in ["scaling"]:
    penalty = lambda p, d: (p+1)**3
    case = "/(p+1)**3/"
    test = "cgjacobi"
    degree = range(6)
    deformations = ([0.2*d for d in range(1, 26)]
                    if type in ["nonaffine_defo", "affine_defo"] else
                    [0.1*d for d in range(1, 26)])
    affine_trafo = False if type == "nonaffine_defo" else True

    # setup plotting output
    folder = "./results/mixed_poisson/"
    type = ("nonaffine" if type == "nonaffine_defo" else
            "affine" if type == "affine_defo" else
            "scaling" if type == "scaling" else
            "none")

    # !!!!
    for c, add_to_quad_degree in enumerate([(i, i) for i in range(1)]):
        case = case  # + "_addtodeg" + str(add_to_quad_degree)
        name = folder + type + case
        try:
            os.makedirs(name)
        except FileExistsError:
            pass
        name += test
        run_test(deformations, degree, penalty, affine_trafo, add_to_quad_degree, params, name, type)
