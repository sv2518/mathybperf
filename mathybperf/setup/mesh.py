from firedrake import *


def mesh_3D(cells_per_dim, s, deform, affine, quadrilateral, hierarchy_nlevels=None):
    n = cells_per_dim
    base = SquareMesh(n, n, s, quadrilateral=quadrilateral)
    if hierarchy_nlevels:
        basemh = MeshHierarchy(base, hierarchy_nlevels)
        mh = ExtrudedMeshHierarchy(basemh, s, base_layer=n)
        mesh = mh[-1]
    else:
        mesh = ExtrudedMesh(base, n)
    coords = mesh.coordinates.dat.data

    if not affine and deform:
        mesh.coordinates.dat.data[2][1] += deform * mesh.coordinates.dat.data[2][1]
        mesh.coordinates.dat.data[4][1] += deform * 0.25 * mesh.coordinates.dat.data[4][1]
    elif affine and deform:
        for i in range(coords.shape[0]):
            if coords[i][2] > 0:
                mesh.coordinates.dat.data[i][2] *= deform

    return mesh
