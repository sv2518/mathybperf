from firedrake import *


def mesh_3D(bag, hierarchy_nlevels=None):
    n = bag.cells_per_dim
    s = bag.scaling
    base = SquareMesh(n, n, s, quadrilateral=bag.quadrilateral)
    if hierarchy_nlevels:
        basemh = MeshHierarchy(base, hierarchy_nlevels)
        mh = ExtrudedMeshHierarchy(basemh, s, base_layer=n)
        mesh = mh[-1]
    else:
        mesh = ExtrudedMesh(base, n)
    coords = mesh.coordinates.dat.data

    c = [1, 0.75]
    if not bag.affine_trafo and bag.deformation:
        for i in range(coords.shape[0]):
            if coords[i][2] > 0:
                mesh.coordinates.dat.data[i][2] *= bag.deformation * c[i]
    elif bag.affine_trafo and bag.deformation:
        for i in range(coords.shape[0]):
            if coords[i][2] > 0:
                mesh.coordinates.dat.data[i][2] *= bag.deformation

    return mesh
