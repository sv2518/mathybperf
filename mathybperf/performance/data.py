
from firedrake.petsc import PETSc
from mpi4py import MPI


class TimeData(object):
    #get internal solver specific times
    #state can be cold or warm
    def get_internal_timedata(self, stage, comm):
        internal_timedata={}

        # get the time data of the solver which would be used for an update in a PECE scheme
        PETSc.Log.Stage(stage).push()
        snes = PETSc.Log.Event("SNESSolve").getPerfInfo()["time"]
        ksp = PETSc.Log.Event("KSPSolve").getPerfInfo()["time"]
        pcsetup = PETSc.Log.Event("PCSetUp").getPerfInfo()["time"]
        pcapply = PETSc.Log.Event("PCApply").getPerfInfo()["time"]#solving time
        jac_eval = PETSc.Log.Event("SNESJacobianEval").getPerfInfo()["time"]
        residual = PETSc.Log.Event("SNESFunctionEval").getPerfInfo()["time"]
        elim = PETSc.Log.Event("SCForwardElim").getPerfInfo()["time"]#elimination time (averagin and assembly ofrhs)
        trace = PETSc.Log.Event("SCSolve").getPerfInfo()["time"]#trace solve time
        full_recon = PETSc.Log.Event("SCBackSub").getPerfInfo()["time"]#backsub time
        hybridassembly= PETSc.Log.Event("HybridOperatorAssembly").getPerfInfo()["time"]#assembly time (inside init)    
        hybridinit = PETSc.Log.Event("HybridInit").getPerfInfo()["time"]
        hybridupdate = PETSc.Log.Event("HybridUpdate").getPerfInfo()["time"]  # assembly
        overall = PETSc.Log.Event("perfsolve").getPerfInfo()["time"]
        PETSc.Log.Stage(stage).pop()

        internal_timedata.update({
                #Scalable Nonlinear Equations Solvers
                "snes_time_upd": comm.allreduce(snes, op=MPI.SUM) / comm.size,
                #scalable linear equations solvers
                "ksp_time_upd": comm.allreduce(ksp, op=MPI.SUM) / comm.size,
                "pc_setup_time_upd": comm.allreduce(pcsetup, op=MPI.SUM) / comm.size,
                "pc_apply_time_upd": comm.allreduce(pcapply, op=MPI.SUM) / comm.size,
                "jac_eval_time_upd":comm.allreduce(jac_eval, op=MPI.SUM) / comm.size,
                "res_eval_time_upd": comm.allreduce(residual, op=MPI.SUM) / comm.size,
                "HybridInit": comm.allreduce(hybridinit, op=MPI.SUM) / comm.size,
                "HybridAssembly": comm.allreduce(hybridassembly, op=MPI.SUM) / comm.size,
                "HybridUpdate": comm.allreduce(hybridupdate, op=MPI.SUM) / comm.size,
                "HybridRhs": comm.allreduce(elim, op=MPI.SUM) / comm.size,
                "HybridRecover": comm.allreduce(full_recon, op=MPI.SUM) / comm.size,
                "HybridTraceSolve": comm.allreduce(trace, op=MPI.SUM) / comm.size,
                "HybridTotal": hybridinit+hybridupdate+elim+full_recon+trace  ,  
                "overall": comm.allreduce(overall, op=MPI.SUM)/comm.size    
                })
        
        return internal_timedata

    # general time spend on different parts of the whole run
    def get_external_timedata(self, stage): 
        #gather all time information
        time_data={
                # stage: PETSc.Log.Event("warm up").getPerfInfo()["time"]
                # "taylorgreen": PETSc.Log.Event("taylorgreen").getPerfInfo()["time"],
                # "configuration": PETSc.Log.Event("configuration").getPerfInfo()["time"],
                # "spcs": PETSc.Log.Event("spcs").getPerfInfo()["time"],
                # "spcs configuration": PETSc.Log.Event("spcs configuration").getPerfInfo()["time"],
                # "initial values": PETSc.Log.Event("initial values").getPerfInfo()["time"],
                # "build forms": PETSc.Log.Event("build forms").getPerfInfo()["time"],
                # "build problems and solvers": PETSc.Log.Event("build problems and solvers").getPerfInfo()["time"],
                # "build update solver": PETSc.Log.Event("update").getPerfInfo()["time"],
                # "update solve": PETSc.Log.Event("update solve").getPerfInfo()["time"],
                # "postprocessing": PETSc.Log.Event("postprocessing").getPerfInfo()["time"],
        }
        return time_data


class SizeData(object):
    def __init__(self, solution):
        self.solution = solution
        self.split_solution = solution.split()

    def get_split_data(self):
        u_dofs, p_dofs = (sol.dof_dset.layout_vec.getSize()
                          for sol in self.split_solution)
        return {"velo dofs": u_dofs,
                "pres dofs": p_dofs,
                "sum dofs": u_dofs + p_dofs}
    
    def get_data(self):
        dofs = self.solution.dof_dset.layout_vec.getSize()
        return {"trace dofs": dofs}
