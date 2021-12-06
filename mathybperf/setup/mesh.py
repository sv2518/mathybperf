from firedrake import *


def mesh_3D(cells_per_dim, s, deform, affine, quadrilateral):
    n = cells_per_dim
    mesh = SquareMesh(n, n, s, quadrilateral=quadrilateral)
    mesh = ExtrudedMesh(mesh, n)
    coords = mesh.coordinates.dat.data

    if not affine:
        mesh.coordinates.dat.data[2][1] += deform * mesh.coordinates.dat.data[2][1]
        mesh.coordinates.dat.data[4][1] += deform * 0.25 * mesh.coordinates.dat.data[4][1]
    else:
        for i in range(coords.shape[0]):
            if coords[i][2] > 0:
                mesh.coordinates.dat.data[i][2] *= deform

    return mesh
