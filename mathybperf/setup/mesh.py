from firedrake import *


def mesh_3D(s, deform, affine, quadrilateral):
    mesh = SquareMesh(1, 1, s, quadrilateral=quadrilateral)
    mesh = ExtrudedMesh(mesh, 1)
    coords = mesh.coordinates.dat.data

    if not affine:
        mesh.coordinates.dat.data[2][1] += deform * mesh.coordinates.dat.data[2][1]
        mesh.coordinates.dat.data[4][1] += deform * 0.25 * mesh.coordinates.dat.data[4][1]
    else:
        for i in range(coords.shape[0]):
            if coords[i][2] > 0:
                mesh.coordinates.dat.data[i][2] *= deform

    return mesh
