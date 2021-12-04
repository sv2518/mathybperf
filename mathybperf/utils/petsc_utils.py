import numpy as np
from firedrake.petsc import PETSc
PETSc.Sys.popErrorHandler()


def petsc_to_py(petscmat):
    n, m = petscmat.getSize()
    aa = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            aa[i, j] = petscmat.getValues(i, j)
    return aa
