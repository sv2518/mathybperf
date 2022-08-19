from distutils.core import setup
import time
from firedrake import *
import os
from tempfile import gettempdir
import matplotlib.pyplot as plt
from firedrake.petsc import PETSc
PETSc.Sys.popErrorHandler()
import numpy as np
import ufl
from pyop2.configuration import configuration
import pandas as pd
from firedrake import tsfc_interface

# RAN WITH FIREDRAKE STATUS:
#
#
# ---------------------------------------------------------------------------
# |Package             |Branch                        |Revision  |Modified  |
# ---------------------------------------------------------------------------
# |COFFEE              |master                        |70c1e66   |False     |
# |FInAT               |master                        |8b08fe0   |False     |
# |PyOP2               |HEAD                          |e72f3167  |False     |
# |fiat                |master                        |5384beb   |False     |
# |firedrake           |sv/local-matfree-scpccg-rebased150522| 4afabfc3 |False      |
# |h5py                |firedrake                     |78531f08  |False     |
# |libspatialindex     |master                        |4768bf3   |True      |
# |libsupermesh        |master                        |69012e5   |False     |
# |loopy               |main170622                    |3988272b  |False     |
# |petsc               |firedrake                     |ba68173f42|False     |
# |pyadjoint           |master                        |0dcfe22   |False     |
# |tsfc                |sv/local-matfree-pr-rebased150522|8aff2c4   |False     |
# |ufl                 |master-150622                 |1dddf46e  |False     |
# ---------------------------------------------------------------------------


def clean():
    os.system('firedrake-clean')
    os.system('rm -r ' + gettempdir() + '/pyop2-cache-*')
    from pyop2.op2 import exit
    tsfc_interface.TSFCKernel._cache = {}
    exit()

def local_operator_plot_and_print_info(a, name, bcs=None, disable_warning=False):
    import numpy as np
    def petsctopy(petscmat):
        n, m = petscmat.getSize()
        aa = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                aa[i, j] = petscmat.getValues(i, j)
        return aa


    if not disable_warning:
        import warnings
        warnings.warn("I don't know if the information about the local matrices are accurate when there are BCs")
    if not a:
        return 

    from firedrake import assemble
    A = assemble(a, mat_type="aij", form_compiler_parameters={"slate_compiler":{"optimise": False, 
                                                              "replace_mul": False}}, bcs=bcs).M.handle
    PETSc.Sys.Print(name + " ---")
    A_np = petsctopy(A)
    PETSc.Sys.Print("condition number:", np.linalg.cond(A_np))
    PETSc.Sys.Print("positive semi definite?:", np.all(np.linalg.eigvals(A_np) >= 0))
    PETSc.Sys.Print("neg semi definite?:", np.all(np.linalg.eigvals(A_np) <= 0))
    PETSc.Sys.Print("eigenvalues bounded?:", np.all(np.linalg.eigvals(A_np)<= np.inf) and np.all(np.linalg.eigvals(A_np)>= -np.inf))
    PETSc.Sys.Print("symmetric?:", np.allclose(A_np, A_np.T, rtol=0.0001,  atol=1e-8))
    PETSc.Sys.Print("Hermitian?:", np.allclose(A_np, A_np.conj().T, rtol=0.0001))
    PETSc.Sys.Print("min, max values:", np.min(A_np), np.max(A_np))
    PETSc.Sys.Print("singular?:", np.allclose(np.linalg.slogdet(A_np)[0], 0, rtol=1e-12))

    def dd(A_np):
        n = len(A_np[0])
        diag = np.zeros(n)
        off_diag = np.zeros(n)
        for i in range(n):
            diag[i] = abs(A_np[i][i])
            for j in range(n):
                if i!=j:
                    off_diag[i] += abs(A_np[i][j])
        return np.all(diag>=off_diag)

    PETSc.Sys.Print("diagonal dominant?:", dd(A_np))
    PETSc.Sys.Print("\n")
    
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(A_np, cmap='RdBu', vmin=-1e-12, vmax=1e-12)
    plt.savefig("./plots/"+name)



def DGLaplacian3D(u, v, value):
    W = u.function_space()
    n = FacetNormal(W.mesh())
    alpha = Constant(value/2)
    gamma = Constant(value)
    h = CellVolume(W.mesh())/FacetArea(W.mesh())
    h_avg = (h('+') + h('-'))/2

    a_dg = (dot(grad(v), grad(u))*dx
            - dot(grad(v), (u)*n)*ds_v
            - dot(v*n, grad(u))*ds_v
            + gamma/h*dot(v, u)*ds_v
            - dot(grad(v), (u)*n)*ds_t
            - dot(v*n, grad(u))*ds_t
            + gamma/h*dot(v, u)*ds_t
            - dot(grad(v), (u)*n)*ds_b
            - dot(v*n, grad(u))*ds_b
            + gamma/h*dot(v, u)*ds_b
            - inner(jump(u, n), avg(grad(v)))*dS_v
            - inner(avg(grad(u)), jump(v, n), )*dS_v
            + alpha/h_avg * inner(jump(u, n), jump(v, n))*dS_v
            - inner(jump(u, n), avg(grad(v)))*dS_h
            - inner(avg(grad(u)), jump(v, n), )*dS_h
            + alpha/h_avg * inner(jump(u, n), jump(v, n))*dS_h)

    bcs = []
    return (a_dg, bcs)


def setup_problem(extruded, N, p, quadri):

    # setup function spaces
    mesh = SquareMesh(N, N, N, quadrilateral=quadri)
    rt = "RTCF" if quadri else "RT"
    if extruded:
        # extrude the mesh to 3D
        mesh = ExtrudedMesh(mesh, N, layer_height=1)

        # Break the RT space in 2 steps because
        # the equvialent to DRT is not defined on this mesh
        # not that this is more involved in 3D because
        # there is no utility space in Firedrake for it
        # 1) construct RT on tensor product element first
        RT = FiniteElement(rt, quadrilateral, p+1)
        DG_v = FiniteElement("DG", interval, p)
        DG_h = FiniteElement("DQ", quadrilateral, p)
        CG = FiniteElement("CG", interval, p+1)
        HDiv_ele = EnrichedElement(HDiv(TensorProductElement(RT, DG_v)),
                                   HDiv(TensorProductElement(DG_h, CG)))
        U = FunctionSpace(mesh, HDiv_ele)
    else:
        # 1) construct RT on tensor product element first
        U = FunctionSpace(mesh, rt, p+1)

    # 2) then break the space
    broken_elements = ufl.MixedElement([ufl.BrokenElement(Vi.ufl_element())
                                        for Vi in U])
    U_d = FunctionSpace(mesh, broken_elements)
    V = FunctionSpace(mesh, "DQ", p)
    T = FunctionSpace(mesh, "DGT", p)
    W = U_d * V * T

    # setup the variational form
    n = FacetNormal(mesh)
    sigma, u, lambdar = TrialFunctions(W)
    tau, v, gammar = TestFunctions(W)

    a = (inner(sigma, tau)*dx + inner(u, div(tau))*dx
         + inner(div(sigma), v)*dx)

    if extruded:
        a += (inner(lambdar('+'), jump(tau, n=n))*dS_h
              + inner(lambdar('+'), jump(tau, n=n))*dS_v
              - inner(jump(sigma, n=n), gammar('+'))*dS_h
              - inner(jump(sigma, n=n), gammar('+'))*dS_v)
        bcs = [DirichletBC(T, Constant(0.0), s)
               for s in ["on_boundary", "top", "bottom"]]
    else:
        a += (inner(lambdar('+'), jump(tau, n=n))*dS
              - inner(jump(sigma, n=n), gammar('+'))*dS)
        bcs = [DirichletBC(T, Constant(0.0), "on_boundary")]

    return a, bcs


def show_numerics(extruded, N, p, quadri, penalty):
    """Actions the static condensaiton operator of
    an H-RT-DG discretised Poisson problem onto a coefficient.
    """

    a, bcs = setup_problem(extruded, N, p, quadri)

    # Now using Slate expressions only
    _A = Tensor(a)
    A = _A.blocks

    # split mixed matrix in blocks
    A00, A01, A10, A11 = A[0, 0], A[0, 1], A[1, 0], A[1, 1]
    KT0, KT1 = A[0, 2], A[1, 2]
    K0, K1 = A[2, 0], A[2, 1]
    J = A[2, 2]

    # tolerances
    atol = 1e-70
    rtol = 1e-12

    # construct inverses on A00 and inner Schur complement
    prec_A = DiagonalTensor(A00).inverse(rtol*1e-2, atol)
    A00_inv = A00.inverse(rtol*1e-2, atol)
    prec_A00_inv = (prec_A * A00).inverse(rtol*1e-2, atol) * prec_A

    inner_S = (A10 * A00_inv * A01 - A11)
    inner_S_inv = inner_S.inverse(rtol, atol)
    test, trial = A11.arguments()

    b, _ = DGLaplacian3D(test, trial, penalty(p))
    prec_inner_S = (A10 * prec_A00_inv * A01 - A11)
    prec_S = DiagonalTensor(Tensor(b)).inverse(rtol, atol)

    # build outer Schur complement
    # K * block1
    K_Ainv_block1 = [K0, (-K0 * A00_inv * A01 + K1)]
    # K * block1 * block2
    K_Ainv_block2 = [K_Ainv_block1[0] * A00_inv,
                     K_Ainv_block1[1] * -inner_S_inv]
    # K * block1 * block2 * block3
    K_Ainv_block3 = [(K_Ainv_block2[0] - K_Ainv_block2[1] * A10 * A00_inv),
                     K_Ainv_block2[1]]
    # K * block1 * block2 * block3 * K.T
    outer_S = J - (K_Ainv_block3[0] * KT0 + K_Ainv_block3[1] * KT1)

    if N > 1:
        PETSc.Sys.Print("\n ------ Show global numerics ------\n")
        local_operator_plot_and_print_info(_A, "Hybridised mixed Poisson A", disable_warning=True)
        PETSc.Sys.Print("Takeaway: hybridised Poisson operator is indefinite\n")
        local_operator_plot_and_print_info(outer_S, "outer Schur complement", bcs, disable_warning=True)
        PETSc.Sys.Print("Takeaway: outer Schur complement is spd\n")
        local_operator_plot_and_print_info(A[0:2, 0:2], "A_01,01", disable_warning=True)
        PETSc.Sys.Print("Takeaway: A_01,01 block is spd\n")
    else:
        PETSc.Sys.Print("\n ------ Show local numerics ------\n")
        local_operator_plot_and_print_info(A00, "velocity mass", disable_warning=True)
        PETSc.Sys.Print("Takeaway: velocity mass matrix block (without traces) is spd\n")
        local_operator_plot_and_print_info(A11, "pressure mass", disable_warning=True)
        PETSc.Sys.Print("Takeaway: pressure mass block (without traces) is singular (it's a zero block)\n")
        local_operator_plot_and_print_info(J, "trace mass", disable_warning=True)
        PETSc.Sys.Print("Takeaway: trace mass block (without traces) is singular (it's a zero block)\n")
        local_operator_plot_and_print_info(A00_inv, "inverse of velocity mass", disable_warning=True)
        PETSc.Sys.Print("Takeaway: inverse of velocity mass matrix does not seem to be dense\n")
        local_operator_plot_and_print_info(prec_A*A00, "preconditioned velocity mass", disable_warning=True)
        PETSc.Sys.Print("Takeaway: preconditioner of the velocity mass matrix lowers the precondition number\n")
        local_operator_plot_and_print_info(inner_S, "inner Schur commplement", disable_warning=True)
        PETSc.Sys.Print("Takeaway: inner Schur complement is spd\n")
        if extruded:
            local_operator_plot_and_print_info(prec_S*prec_inner_S, "preconditioned inner S", disable_warning=True)
            PETSc.Sys.Print("""Takeaway: preconditioner of the inner schur complement lowers
                  the precondition number not by much and only for high order\n""")


#############
plt.style.use("seaborn-darkgrid")
plt.rcParams.update({'font.size': 24})

extruded_to_3D = True
N_list = [3, 1]  # local vs global numerics
p_list = [2]
quadri_list = [True]
penalty = lambda p: (p+1)**3

for quadri in quadri_list:
    for N in N_list:
        for p in p_list:
            show_numerics(extruded_to_3D, N, p, quadri, penalty)
