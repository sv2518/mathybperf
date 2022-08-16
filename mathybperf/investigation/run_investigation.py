from firedrake import *
import numpy as np
from mathybperf import *
from mathybperf.utils.solver_utils import SolverBag
import os

# TODO
# 1) fix counting of iterations
# 2) fix condition number plots


def run_test(deformations, orders, penalty, affine_trafo, add_to_quad_degree, params, name, type):
    dofs = np.zeros(len(orders))
    konditionnumberlist = []
    eigenvaluelist = []
    outeritslist = []
    totalitslist = []
    results_outer_its = np.zeros([len(orders)])
    results_total_its = np.zeros([len(orders)])

    for deform in deformations:
        konditionnumbers = []
        eigenvals = []
        totalits = []
        outerits = []
        quaddegreelist = []
        for i, p in enumerate(orders):
            try:
                # Problem setup and solve
                s = deform if type == "scalings" else 1
                deform = 1 if type == "scalings" else deform
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
                konditionnumbers.append(analytics_mixed.condition_number())
                # print("Mixed poisson spd?", analytics_mixed.spd())
                # print("Mixed poisson singular?", analytics_mixed.singular())
                print("Mixed poisson condition number", analytics_mixed.condition_number())

                # AB = Tensor(a).blocks
                # S = AB[1, 1] - AB[1, 0] * AB[0, 0].inv * AB[0, 1]
                # analytics_schur = Analytics(S)
                # print("Schur spd?", analytics_schur.spd())
                # print("Schur singular?", analytics_schur.singular())
                # print("Schur condition number", analytics_schur.condition_number())

                # analytics_vmass = Analytics(AB[0, 0])
                # print("Velocity mass spd?", analytics_vmass.spd())
                # print("Velocity mass singular?", analytics_vmass.singular())
                # print("Velocity mass condition number", analytics_vmass.condition_number())

                # Iteration counts
                outer_its = solver.snes.ksp.its
                pcs = solver.snes.ksp.pc.getFieldSplitSubKSP()
                fsp0_its = pcs[0].its
                fsp1_its = pcs[1].its
                results_total_its[i] = outer_its*(fsp1_its+fsp1_its*fsp0_its)
                results_outer_its[i] = outer_its

                # velo, pres = w.split()
                # f1 = File("mathybperf/investigation/visualisation/poisson_mixed_velocity_"+str(p)+".pvd")
                # f1.write(velo)
                # f2 = File("mathybperf/investigation/visualisation/poisson_mixed_pressure_"+str(p)+".pvd", project_output=True)
                # f2.write(pres)

            except Exception as e:
                # check that aborted bc of divergence
                if solver.snes.diverged or solver.snes.ksp.diverged or pcs[0].diverged or pcs[1].diverged:
                    results_total_its[i] = -1
                    results_outer_its[i] = -1
                else:
                    results_total_its[i] = -2
                    results_outer_its[i] = -2

            outerits.append(results_outer_its[i])
            totalits.append(results_total_its[i])
            dofs[i] = solver.snes.vec_sol.local_size
            quaddegreelist.append(list(int(q) for q in quadrature_degree))

        outeritslist.append(outerits)
        totalitslist.append(totalits)
        konditionnumberlist.append(konditionnumbers)
        eigenvaluelist.append(eigenvals)

    # write data to csv file
    write_investigation_data([eigenvaluelist, konditionnumberlist,
                              outeritslist, totalitslist, deformations],
                             name+"_per_deformation.csv",
                             ["eigs", "kond", "outer_its", "total_its",
                              "deformations"],
                             ["deformation from 1.0 in percentage : %d" % (d*100) for d in deformations])
    write_investigation_data([orders, dofs, quaddegreelist, [params]*len(orders)],
                             name+"_per_order.csv",
                             ["orders", "dofs", "quad_degree", "params"])


# !!!!
class DGLaplacian(AuxiliaryOperatorPC):
    def form(self, pc, u, v):
        ctx = self.get_appctx(pc)
        d = ctx["deform"]
        value = ctx["value"]
        q = ctx["quadrature_degree"]

        def gamma(p, h, d, value):
            return Constant(value)/(h*h)

        W = u.function_space()
        n = FacetNormal(W.mesh())

        p = W._ufl_element._sub_elements[0]._degree
        h = CellVolume(W.mesh())/FacetArea(W.mesh())

        a_dg = -(dot(grad(v), grad(u))*dx(degree=q)
                 - dot(grad(v), (u)*n)*ds_v(degree=q)
                 - dot(v*n, grad(u))*ds_v(degree=q)
                 + gamma(p, h, d, value)*dot(v, u)*ds_v(degree=q)
                 - dot(grad(v), (u)*n)*ds_t(degree=q)
                 - dot(v*n, grad(u))*ds_t(degree=q)
                 + gamma(p, h, d, value)*dot(v, u)*ds_t(degree=q)
                 - dot(grad(v), (u)*n)*ds_b(degree=q)
                 - dot(v*n, grad(u))*ds_b(degree=q)
                 + gamma(p, h, d, value)*dot(v, u)*ds_b(degree=q))

        bcs = []
        return (a_dg, bcs)


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
          "fieldsplit_1_pc_python_type": __name__ + ".DGLaplacian",
          "fieldsplit_1_ksp_rtol": 1e-8,
          "fieldsplit_1_ksp_atol": 1e-8,
          "fieldsplit_1_ksp_max_it": 2000,
          "fieldsplit_1_aux_pc_type": "jacobi",
          "fieldsplit_1_ksp_monitor": None,
          "ksp_monitor": None,
          "ksp_norm_type": "unpreconditioned",
          }


for type in ["nonaffine_defo"]:  # , "affine_defo", "scaling", "no_defo"]:
    penalty = lambda p, d: (p+1)**3
    case = "/(p+1)**3/"
    test = "cgjacobi"
    degree = range(6)
    deformations = ([0.2*d for d in range(1, 26)]
                    if type in ["nonaffine_defo", "affine_defo", "scaling"] else
                    [1])
    affine_trafo = False if type == "nonaffine_defo" else True

    # setup plotting output
    folder = "./results/mixed_poisson/"
    type = ("nonaffine" if type == "nonaffine_defo" else
            "affine" if type == "affine_defo" else
            "scaling" if type == "scaling" else
            "nodeform")

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
