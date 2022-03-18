
from firedrake.petsc import PETSc
from mpi4py import MPI


class TimeData(object):

    def get_time(self, key):
        return PETSc.Log.Event(key).getPerfInfo()["time"]

    def reduce(self, time, comm):
        return comm.allreduce(time, op=MPI.SUM) / comm.size

    # get internal solver specific times
    # state can be cold or warm
    def get_internal_timedata(self, comm):
        internal_timedata = {}

        snes = self.get_time("SNESSolve")
        ksp = self.get_time("KSPSolve")
        pcsetup = self.get_time("PCSetUp")
        pcapply = self.get_time("PCApply")
        jac_eval = self.get_time("SNESJacobianEval")
        residual = self.get_time("SNESFunctionEval")
        # elimination time (averaging and assembly of rhs)
        elim = self.get_time("SCForwardElim")
        # trace solve time
        trace = self.get_time("SCSolve")
        # backsub time
        full_recon = self.get_time("SCBackSub")
        # assembly time (inside init)
        hybridassembly = self.get_time("HybridOperatorAssembly")
        hybridinit = self.get_time("HybridInit")
        hybridupdate = self.get_time("HybridUpdate")  # assembly
        overall = self.get_time("perfsolve")

        internal_timedata.update({"snes_time_upd": self.reduce(snes, comm),
                                  "ksp_time_upd": self.reduce(ksp, comm),
                                  "pc_setup_time_upd": self.reduce(pcsetup, comm),
                                  "pc_apply_time_upd": self.reduce(pcapply, comm),
                                  "jac_eval_time_upd": self.reduce(jac_eval, comm),
                                  "res_eval_time_upd": self.reduce(residual, comm),
                                  "HybridInit": self.reduce(hybridinit, comm),
                                  "HybridAssembly": self.reduce(hybridassembly, comm),
                                  "HybridUpdate": self.reduce(hybridupdate, comm),
                                  "HybridRhs": self.reduce(elim, comm),
                                  "HybridRecover": self.reduce(full_recon, comm),
                                  "HybridTraceSolve": self.reduce(trace, comm),
                                  "HybridTotal": hybridinit+hybridupdate+elim+full_recon+trace,
                                  "overall": self.reduce(overall, comm)})

        return internal_timedata


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
        return {"trace dofs (part of velo dofs)": dofs}
