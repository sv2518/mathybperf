from mathybperf import *
import pandas as pd
from firedrake.petsc import PETSc
import json
from mathybperf.utils.solver_utils import SolverBag
from mathybperf.utils.setup_utils import fetch_setup
from firedrake.petsc import OptionsManager
import importlib
import sys, traceback, os
import gc

gc.collect()

######################################
##############   MAIN   ##############
######################################

parameters["pyop2_options"]["lazy_evaluation"] = False

args = fetch_setup()
# Penalty is set the same for all runs
penalty = lambda p, d: (p+1)**3
warmup = "warm_up" if args.clean else "warmed_up"
PETSc.Sys.Print("Running: ", warmup+"\n")
args.add_to_quad_degree = tuple(args.add_to_quad_degree)
# Set parameters to the parameter set with the name specified in shell script
importlib.import_module("mathybperf.setup.parameters")
parameters = globals()[args.parameters]
PETSc.Sys.Print("with params: ", args.parameters+"\n")


# problem setup
tas_data = {}
solver_bag = SolverBag(parameters, None, args.gtmg_levels)
problem_bag = ProblemBag(args.deform, args.scaling, args.trafo, args.quadrilateral,
                         args.p, args.add_to_quad_degree, penalty, args.c, args.exact_sol_type)
time_data = TimeData()

# If the -log_view flag is passed you don't need to call
# PETSc.Log.begin because it is done automatically.
if "log_view" not in OptionsManager.commandline_options:
    PETSc.Log.begin()

# get internal time data of solvers
petsc_stage_name = "stage"
with PETSc.Log.Stage(petsc_stage_name):
    try:
        quad_degree, (w, w2), (w_t, w_t_exact), mesh = problem(problem_bag, solver_bag,
                                                               verification=args.verification,
                                                               project=args.projectexactsol)
        VERIFY_STATUS = "success"
    except Exception as e:
        VERIFY_STATUS = traceback.format_exc()
        error = int(not VERIFY_STATUS=="success")
        pid = os.get_pid()
        err_filename = args.name[:args.name.rfind("trafo")] + str(pid) + '_verification.err'
        with open(err_filename, 'w') as convert_file:
            output =("The following setup was run last.\n"
                        + str(problem_bag) + "\nSolver parameters:\n"
                        + str(json.dumps(parameters, indent=4))
                        +"\n\nThe setup finished with the following status.\n\n"
                        +str(VERIFY_STATUS))
            convert_file.write(output)
            PETSc.Sys.Print("failed with \n", str(e))
            gc.collect()
        sys.exit(error)
    internal_timedata_cold = time_data.get_internal_timedata(warmup, mesh.comm)
tas_data.update(internal_timedata_cold)

# add general times spend on different parts
external_timedata = time_data.get_external_timedata(petsc_stage_name)
tas_data.update(external_timedata)

# add further information
# setup information
tas_data.update(vars(args))
data_to_tex={"Local tensor shape": str(problem_bag.total_local_shape)}

# gather dofs
size_data = SizeData(w).get_split_data()
data_to_tex.update(size_data)
tas_data.update(size_data)

# gather errors
if args.projectexactsol:
    accuracy_data = get_errors(w, w2)
    tas_data.update(accuracy_data)
    data_to_tex.update(accuracy_data)

# gather dofs for trace
size_data = SizeData(w_t).get_data()
tas_data.update(size_data)
data_to_tex.update(size_data)

# errors for trace
if args.projectexactsol:
    accuracy_data = get_error(w_t, w_t_exact)
    tas_data.update(accuracy_data)
    data_to_tex.update(accuracy_data)

if not args.verification:
    PETSc.Sys.Print("Writing some files...")
    # write out data to .csv
    datafile = pd.DataFrame(tas_data)
    datafile.to_csv(args.name+f"_order{args.p}_cells{args.c}.csv",index=False,mode="w",header=True)

    # also remember which parameter sets we used for the solver
    paramsfilename = args.name + '_parameters.txt'
    with open(paramsfilename, 'w') as convert_file:
        convert_file.write(json.dumps(parameters, indent=4))

    # also save latex table for setup data separate
    setup_filename = args.name + '_setup.tex'
    with open(setup_filename, 'w') as convert_file:
        convert_file.write(problem_bag.latex())

    # also save latex table for size data separate
    size_table_filename = args.name + '_extradata.tex'
    with open(size_table_filename, 'w') as convert_file:
        convert_file.write(pd.DataFrame(data_to_tex, index=[0]).to_latex(index=False))