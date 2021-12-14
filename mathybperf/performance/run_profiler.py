from firedrake import Citations
from firedrake.preconditioners import base
from mathybperf import *
import numpy as np
import pandas as pd
from firedrake.petsc import PETSc
import json
import os

# Citations.print_at_exit()

class SolverBag(object):

    def __init__(self, perform_params, baseline_params, gtmg_levels):
        self.perform_params = perform_params
        self.baseline_params = baseline_params
        self.levels = gtmg_levels
        self.mesh = None

    def get_p1_space(self):
        return FunctionSpace(self.mesh, "CG", 1)

    def get_p1_prb_bcs(self):
        return [DirichletBC(self.get_p1_space(), Constant(0.0), "on_boundary"),
                DirichletBC(self.get_p1_space(), Constant(0.0), "top"),
                DirichletBC(self.get_p1_space(), Constant(0.0), "bottom")]

    def p1_callback(self):
        P1 = self.get_p1_space()
        p = TrialFunction(P1)
        q = TestFunction(P1)
        return inner(grad(p), grad(q))*dx

    def exact_solution(self, L):
        x = SpatialCoordinate(self.mesh)
        return x[0]*(L-x[0])*x[1]*(L-x[1])*x[2]*(L-x[2]) * exp(L-x[0]+1)

######################################
##############   MAIN   ##############
######################################

parameters["pyop2_options"]["lazy_evaluation"] = False


#########    GENERAL SETUP   ####
gt_params_nested = {"mg_coarse": mg_jack,
                    "mg_levels": gt_levels_cheby}

# setup test
perform_params = {'mat_type': 'matfree',
                  'ksp_type': 'preonly',
                  'pc_type': 'python',
                  'pc_python_type': 'firedrake.HybridizationPC',
                  'hybridization': {'ksp_type': 'cg',
                                    'pc_type': 'python',
                                    'ksp_rtol': 1e-8,
                                    'mat_type': 'matfree',
                                    'pc_python_type': 'firedrake.GTMGPC',
                                    'gt': gt_params_nested}}
baseline_params = {"ksp_type": "gmres",
                    'pc_type': 'ilu',
                    "ksp_gmres_restart": 100,
                    'ksp_rtol': 1.e-12}

gtmg_levels = 2
solver_bag = SolverBag(perform_params, baseline_params, gtmg_levels)

penalty = lambda p, d: (p+1)**3
orders = range(6)
scalings = [1.0]
itmaxs = [4]  # script is not working for varyin itmaxs rn
deformations = [0] # 0.5*d for d in range(0,21)
affine_trafo = False
add_to_quad_degree = (0, 0)
cells_per_dim = range(1, 5)
quadrilateral = True

# setup output
folder = "mathybperf/performance/results/mixed_poisson/"
type = "affine/" if deformations and affine_trafo else "nonaffine/" if deformations else "nodeform/"
case = "(p+1)**3/"
test = "cgjacobi"
name =  folder + type + case
try:
    os.makedirs(name)
except FileExistsError:
    pass
name += test

# remember which parameter sets we used for the solver
with open(name + 'performance_parameters.txt', 'w') as convert_file:
     convert_file.write(json.dumps(perform_params))

# turn off threading
os.system('export OMP_NUM_THREADS=1')

PETSc.Log.begin()
time_data = TimeData()
tas_data_orders = []
assert len(deformations) == 1 or len(scalings) == 1, "Can only loop over either, scalings or deformations"
for deform in deformations:
    for s in scalings:
        for p in orders:
            tas_data_cells = {}
            for c in cells_per_dim:
                tas_data = {}
                # problem setup
                problem_bag = ProblemBag(deform, s, affine_trafo, quadrilateral,
                                        p, add_to_quad_degree, penalty, c)

                PETSc.Sys.Print("Approximation order:", p)
                PETSc.Sys.Print("\nDeformation: ", deform)
                PETSc.Sys.Print("\nCell scaling: ", s)
                PETSc.Sys.Print("\n# of cells per dim: ", c)

                # get internal time data of solvers
                # warm up solver
                with PETSc.Log.Stage("warmup"):
                    _, _, _, (w, w2), mesh = problem(problem_bag, solver_bag, verification=True)
                    internal_timedata_cold = time_data.get_internal_timedata("warmup", "cold", mesh.comm)
                    temp_internal_timedata_cold = time_data.get_internal_timedata("warmup", "warm", mesh.comm)#temp needed for subtraction 
                tas_data.update(internal_timedata_cold)

                # get timings for solving without assembly
                with PETSc.Log.Stage("update solve"):
                    _, _, _, (_, _), mesh = problem(problem_bag, solver_bag, verification=True, new=False)
                    temp_internal_timedata_warm = time_data.get_internal_timedata("update solve", "warm", mesh.comm)
                internal_timedata_warm={key: temp_internal_timedata_warm[key]
                                        for key in temp_internal_timedata_warm.keys()}
                tas_data.update(internal_timedata_warm)

                # add general times spend on different parts
                external_timedata = time_data.get_external_timedata("update solve")
                tas_data.update(external_timedata)

                # add further information
                # setup information
                tas_data.update({"order": p,
                                "deform": deform,
                                "scalings": s
                })

                # gather dofs
                u_w, p_w = w.split()
                u_dofs = u_w.dof_dset.layout_vec.getSize() 
                p_dofs = p_w.dof_dset.layout_vec.getSize()
                size_data={
                    "velo dofs": u_dofs,
                    "pres dofs": p_dofs,
                    "sum dofs": u_dofs+p_dofs
                }
                tas_data.update(size_data)

                # gather errrors
                errors = get_errors(w, w2)
                accuracy_data={"LinfPres": errors[0][1],
                            "LinfVelo": errors[0][0],
                            "L2Pres": errors[1][1],
                            "L2Velo": errors[1][0],
                            "H1Pres": errors[2][1],
                            "HDivVelo": errors[2][0],  
                }
                PETSc.Sys.Print("\n error u : ", errors[1][0])
                PETSc.Sys.Print("\n error p: ", errors[1][1])
                tas_data.update(accuracy_data)

                # write out data to .csv
                datafile = pd.DataFrame(tas_data, index=[0])   
                datafile.to_csv(name+f"_order{p}_cells{c}.csv",index=False,mode="w",header=True)

