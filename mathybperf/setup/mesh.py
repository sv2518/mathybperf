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

    if not bag.affine_trafo and bag.deformation:
        mesh.coordinates.dat.data[2][1] += bag.deformation * mesh.coordinates.dat.data[2][1]
        mesh.coordinates.dat.data[4][1] += bag.deformation * 0.25 * mesh.coordinates.dat.data[4][1]
    elif bag.affine_trafo and bag.deformation:
        for i in range(coords.shape[0]):
            if coords[i][2] > 0:
                mesh.coordinates.dat.data[i][2] *= bag.deformation

    return mesh
