from firedrake import *
import numpy as np


def one(fs):
    one = Function(fs, name="one")
    ones = one.split()
    for fi in ones:
        fs_i = fi.function_space()
        if fs_i.rank == 1:
            fi.interpolate(Constant((1.0,) * fs_i.value_size))
        elif fs_i.rank == 2:
            fi.interpolate(Constant([[1.0 for i in range(fs_i.mesh().geometric_dimension())]
                                     for j in range(fs_i.rank)]))
        else:
            fi.interpolate(Constant(1.0))
    return one


def check_facetarea_and_cellvolume(U):
    Vt = FunctionSpace(U.mesh(), 'DGT', 0)
    u = TrialFunction(Vt)
    v = TestFunction(Vt)

    top = Function(Vt)
    proj_form = u*v*ds_t == FacetArea(U.mesh())*v*ds_t
    solve(proj_form, top, solver_parameters={"ksp_type": "cg", "pc_type": "jacobi"})

    vert1 = Function(Vt)
    proj_form = u*v*ds_v(1) == FacetArea(U.mesh())*v*ds_v(1)
    solve(proj_form, vert1, solver_parameters={"ksp_type": "cg", "pc_type": "jacobi"})
    vert2 = Function(Vt)
    proj_form = u*v*ds_v(2) == FacetArea(U.mesh())*v*ds_v(2)
    solve(proj_form, vert2, solver_parameters={"ksp_type": "cg", "pc_type": "jacobi"})
    vert3 = Function(Vt)
    proj_form = u*v*ds_v(3) == FacetArea(U.mesh())*v*ds_v(3)
    solve(proj_form, vert3, solver_parameters={"ksp_type": "cg", "pc_type": "jacobi"})
    vert4 = Function(Vt)
    proj_form = u*v*ds_v(4) == FacetArea(U.mesh())*v*ds_v(4)
    solve(proj_form, vert4, solver_parameters={"ksp_type": "cg", "pc_type": "jacobi"})

    bot = Function(Vt)
    proj_form = u*v*ds_b == FacetArea(U.mesh())*v*ds_b
    solve(proj_form, bot, solver_parameters={"ksp_type": "cg", "pc_type": "jacobi"})

    assert (np.isclose(project(CellVolume(U.mesh()), U).dat.data[0], assemble(one(U)*dx), rtol=1.e-4))
    assert (np.isclose(top.dat.data.max(), assemble(one(U)*ds_t), rtol=1.e-4))
    assert (np.isclose(vert1.dat.data.max(), assemble(one(U)*ds_v(1)), rtol=1.e-4))
    assert (np.isclose(vert2.dat.data.max(), assemble(one(U)*ds_v(2)), rtol=1.e-4))
    assert (np.isclose(vert3.dat.data.max(), assemble(one(U)*ds_v(3)), rtol=1.e-4))
    assert (np.isclose(vert4.dat.data.max(), assemble(one(U)*ds_v(4)), rtol=1.e-4)), str(vert4.dat.data)+"!="+str(assemble(one(U)*ds_v(4)))
    assert (np.isclose(bot.dat.data.max(), assemble(one(U)*ds_b), rtol=1.e-4)), str(bot.dat.data)+"!="+str(assemble(one(U)*ds_b))
