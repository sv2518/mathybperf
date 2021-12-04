from firedrake import *


class DGLaplacian(AuxiliaryOperatorPC):

    def form(self, pc, u, v):

        ctx = self.get_appctx(pc)
        d = ctx["deform"]
        value = ctx["value"]
        q = ctx["quadrature_degree"]

        def gamma(p, h, d, value):
            # Note approximation defree and deformation of the mesh
            # are currently not used in the DG penalty parameter
            return Constant(value)/h

        W = u.function_space()
        n = FacetNormal(W.mesh())

        p = W._ufl_element._sub_elements[0]._degree
        h = CellVolume(W.mesh())/FacetArea(W.mesh())

        a_dg = -(dot(grad(v), grad(u)) * dx(degree=q)
                 - dot(grad(v), u * n) * ds_v(degree=q)
                 - dot(v * n, grad(u)) * ds_v(degree=q)
                 + gamma(p, h, d, value) * dot(v, u) * ds_v(degree=q)
                 - dot(grad(v), u * n) * ds_t(degree=q)
                 - dot(v * n, grad(u)) * ds_t(degree=q)
                 + gamma(p, h, d, value) * dot(v, u) * ds_t(degree=q)
                 - dot(grad(v), u * n) * ds_b(degree=q)
                 - dot(v * n, grad(u)) * ds_b(degree=q)
                 + gamma(p, h, d, value) * dot(v, u) * ds_b(degree=q))

        bcs = []
        return (a_dg, bcs)
