import argparse


def fetch_setup():
    """GENERAL SETUP
       Information are fetched from shell script run_profiler.sh
    """

    parser = argparse.ArgumentParser(description='Fetch setup from shell script.')
    parser.add_argument('name', type=str,
                        help='an integer for the accumulator')
    parser.add_argument('parameters', type=str,
                        help='Parmeter set name to solve the variational problem.')
    parser.add_argument('p', type=int,
                        help="""Approximation degree of RT of the function space.
                              DG space will have one less.""")
    parser.add_argument('gtmg_levels', type=int,
                        help='Number of levels in GTMG.')
    parser.add_argument('quadrilateral', type=bool,
                        help='Quadrilateral cells?')
    parser.add_argument('scaling', type=float, default=[0],
                        help='By which factor to scale the cell.')
    parser.add_argument('deform', type=float, default=[0],
                        help='By which factor to deform the cell.')
    parser.add_argument('trafo', type=str, default="",
                        help='Should the deformation be affine, non-affine or none?')
    parser.add_argument('c', type=int,
                        help="""Number of cells per dimension.
                                This is essentially the mesh size parameter.""")
    parser.add_argument('exact_sol_type', type=str,
                        help="""Type of the exact solution.
                                Can be quadratic or exponential at the moment.""")
    parser.add_argument('--add_to_quad_degree', type=int, nargs="+", default=[0, 0],
                        help='In- or decrease the quadrature degree by a tuple.')
    parser.add_argument('--projectexactsol', action="store_true",
                        help='Should the exact solution on the trace be projected so that we know the error?')
    parser.add_argument('-log_view', type=str,
                        help="""Flamegraph?""")
    parser.add_argument('--clean', action="store_true", help='Clean firdrake caches?')
    parser.add_argument('--verification', action="store_true", help='Should errors on results be checked?')

    return parser.parse_args()
