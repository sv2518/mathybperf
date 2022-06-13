from mathybperf import *
import pandas as pd
from firedrake.petsc import PETSc
import json
from mathybperf.utils.solver_utils import SolverBag
from mathybperf.utils.setup_utils import fetch_setup
from firedrake.petsc import OptionsManager
import importlib
import sys
import traceback

######################################
##############   MAIN   ##############
######################################

args = fetch_setup()
PETSc.Sys.Print("Read args from shell script: ", str(args)+"\n")
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
try:
    quad_degree, (w, w2), (w_t, w_t_exact), mesh, solver = problem(problem_bag, solver_bag,
                                                                    verification=args.verification,
                                                                    project=args.projectexactsol)
except Exception as e:
    VERIFY_STATUS = traceback.format_exc()
    error = int(not VERIFY_STATUS == "success")
    PETSc.Sys.Print("\n\n\n-----FAILED WITH AN ERROR ----"
                    + "\n\n The error message is: " + str(e)
                    + "\n\nThe following setup was run last.\n"
                    + str(problem_bag) + "\nSolver parameters:\n"
                    + str(json.dumps(parameters, indent=4))
                    + "\n\nThe setup finished with the following status.\n\n"
                    + str(VERIFY_STATUS))
    sys.exit(error)
internal_timedata_cold = time_data.get_internal_timedata(mesh.comm)
tas_data.update(internal_timedata_cold)

# add further information
# setup information
tas_data.update(vars(args))
data_to_tex = {"Local tensor shape": str(problem_bag.total_local_shape)}

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

# get iterations
pc = solver.snes.ksp.pc.getPythonContext() if solver.snes.ksp.pc.getType() == "python" else None
its = {'outer_its': pc.trace_ksp.its} if pc and hasattr(pc, "trace_ksp") else {'outer_its': 0}

if not args.verification:
    # write out data to .csv
    datafile = pd.DataFrame(tas_data)
    datafile.to_csv(args.name+f"_order{args.p}_cells{args.c}.csv",
                    index=False, mode="w", header=True)

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
        frame = pd.DataFrame(data_to_tex, index=[0]).to_latex(index=False)
        convert_file.write(frame)

    # also remember which the iteration count
    paramsfilename = args.name + '_its.json'
    with open(paramsfilename, 'w') as convert_file:
        convert_file.write(json.dumps(its, indent=4))
