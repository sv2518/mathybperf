from firedrake import *


def RT_DQ_3D(p, mesh):
    RT = FiniteElement("RTCF", quadrilateral, p+1)
    DG_v = FiniteElement("DG", interval, p)
    DG_h = FiniteElement("DQ", quadrilateral, p)
    CG = FiniteElement("CG", interval, p+1)
    HDiv_ele = EnrichedElement(HDiv(TensorProductElement(RT, DG_v)),
                               HDiv(TensorProductElement(DG_h, CG)))
    U = FunctionSpace(mesh, HDiv_ele)
    V = FunctionSpace(mesh, "DQ", p)
    W = U * V

    return W, U, V
