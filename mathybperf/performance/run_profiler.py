from mathybperf import *
import pandas as pd
from firedrake.petsc import PETSc
import json
from mathybperf.utils.solver_utils import SolverBag
import argparse
from firedrake.petsc import OptionsManager
import importlib

######################################
##############   MAIN   ##############
######################################

parameters["pyop2_options"]["lazy_evaluation"] = False

def fetch_info():
    """GENERAL SETUP
       Information are fetched from shell script run_profiler.sh 
    """

    parser = argparse.ArgumentParser(description='Fetch setup from shell script.')
    parser.add_argument('name', type=str,
                        help='an integer for the accumulator')
    parser.add_argument('parameters', type=str,
                        help='Parmeter set name to solve the variational problem.')
    parser.add_argument('p', type=int,
                        help="""Approximation degree of RT of the function space.
                              DG space will have one less.""")
    parser.add_argument('gtmg_levels', type=int,
                        help='Number of levels in GTMG.')
    parser.add_argument('quadrilateral', type=bool,
                        help='Quadrilateral cells?')
    parser.add_argument('scaling', type=float, default=[0],
                        help='By which factor to scale the cell.')
    parser.add_argument('deform', type=float, default=[0],
                        help='By which factor to deform the cell.')
    parser.add_argument('trafo', type=str, default="",
                        help='Should the deformation be affine, non-affine or none?')
    parser.add_argument('c', type=int,
                        help="""Number of cells per dimension.
                                This is essentially the mesh size parameter.""")
    parser.add_argument('exact_sol_type', type=str,
                        help="""Type of the exact solution.
                                Can be quadratic or exponential at the moment.""")
    parser.add_argument('--add_to_quad_degree', type=int, nargs="+", default=[0,0],
                        help='In- or decrease the quadrature degree by a tuple.')
    parser.add_argument('-log_view', type=str,
                        help="""Flamegraph?""")
    parser.add_argument('--clean', action="store_true", help='Clean firdrake caches?')
    parser.add_argument('--verification', action="store_true",  help='Should errors on results be checked?')

    return parser.parse_args()

args = fetch_info()
# Penalty is set the same for all runs
penalty = lambda p, d: (p+1)**3
warmup = "warm_up" if args.clean else "warmed_up"
args.add_to_quad_degree = tuple(args.add_to_quad_degree)
# Set parameters to the parameter set with the name specified in shell script
importlib.import_module("mathybperf.setup.parameters")
parameters = globals()[args.parameters]


# problem setup
tas_data = {}
solver_bag = SolverBag(perform_params, baseline_params, args.gtmg_levels)
problem_bag = ProblemBag(args.deform, args.scaling, args.trafo, args.quadrilateral,
                         args.p, args.add_to_quad_degree, penalty, args.c, args.exact_sol_type)
time_data = TimeData()

# If the -log_view flag is passed you don't need to call
# PETSc.Log.begin because it is done automatically.
if "log_view" not in OptionsManager.commandline_options:
    PETSc.Log.begin()
PETSc.Sys.Print("Approximation order: ", args.p, "\n")
PETSc.Sys.Print("Deformation: ", args.deform, "\n")
PETSc.Sys.Print("Cell scaling: ", args.scaling, "\n")
PETSc.Sys.Print("# of cells per dim: ", args.c, "\n")

# get internal time data of solvers
# warm up solver
with PETSc.Log.Stage("stage"):
    quad_degree, (w, w2), (w_t, w_t_exact), mesh = problem(problem_bag, solver_bag, verification=args.verification)
    internal_timedata_cold = time_data.get_internal_timedata(warmup, mesh.comm)
tas_data.update(internal_timedata_cold)

# add general times spend on different parts
external_timedata = time_data.get_external_timedata("update solve")
tas_data.update(external_timedata)

# add further information
# setup information
tas_data.update(vars(args))

# gather dofs
size_data = SizeData(w).get_split_data()
tas_data.update(size_data)

# gather errors
accuracy_data = get_errors(w, w2)
PETSc.Sys.Print("error u : ", accuracy_data["L2Velo"], "\n")
PETSc.Sys.Print("error p: ", accuracy_data["L2Pres"], "\n")
tas_data.update(accuracy_data)

# gather dofs for trace
size_data = SizeData(w_t).get_data()
tas_data.update(size_data)

# errors for trace
accuracy_data = get_error(w_t, w_t_exact)
PETSc.Sys.Print("error trace: ", accuracy_data["LinfTrace"], "\n")
tas_data.update(accuracy_data)

# write out data to .csv
datafile = pd.DataFrame(tas_data)
datafile.to_csv(args.name+f"_order{args.p}_cells{args.c}.csv",index=False,mode="w",header=True)

# also remember which parameter sets we used for the solver
paramsfilename = args.name + "_" + args.parameters + '_parameters.txt'
with open(paramsfilename, 'w') as convert_file:
     convert_file.write(json.dumps(perform_params))


