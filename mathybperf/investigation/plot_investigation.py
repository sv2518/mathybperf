from mathybperf import *

# Setup
folder = "./results/mixed_poisson/"
case = "/(p+1)**3/"
test = "cgjacobi"

for defo in ["scaling", "deformations"]:
    types = ["scaling"] if defo == "scaling" else ["affine", "nonaffine"]
    for type in types:
        name = folder + type + case + test

        # Read the data
        df_deformation = pd.read_csv(name+"_per_deformation.csv")
        df_order = pd.read_csv(name+"_per_order.csv")

        # Plot the data
        plotter = ResultPlotter()

        plotter.plot_knds(name, df_order.iloc[0][1:], df_order.iloc[1][1:],
                          df_deformation.iloc[8][1:],
                          df_deformation.iloc[1][1:],
                          df_deformation.iloc[2][1:],
                          df_deformation.iloc[3][1:],
                          df_order.iloc[3][0],
                          df_order.iloc[2][1:],
                          xlabel=defo,
                          type=type)

        # name, orders, dofs, defo, results, knds, params, quad_degree_list, its_type, xlabel
        outer_its = df_deformation.iloc[4][1:]
        mixed_kond = df_deformation.iloc[1][1:]
        ylabel = "outer"
        plotter.plot_per_order(name, df_order.iloc[0][1:], df_order.iloc[1][1:],
                               df_deformation.iloc[8][1:], outer_its,
                               mixed_kond, df_order.iloc[3][0],
                               df_order.iloc[2][1:],
                               its_type=f"{ylabel}_{type}_{defo}",
                               xlabel=defo, ylabel=ylabel)
        total_its = df_deformation.iloc[5][1:]
        ylabel = "total"
        plotter.plot_per_order(name, df_order.iloc[0][1:], df_order.iloc[1][1:],
                               df_deformation.iloc[8][1:], total_its,
                               mixed_kond, df_order.iloc[3][0],
                               df_order.iloc[2][1:],
                               its_type=f"{ylabel}_{type}_{defo}",
                               xlabel=defo, ylabel=ylabel)
        fsp0_its = df_deformation.iloc[6][1:]
        fsp0_kond = df_deformation.iloc[2][1:]
        ylabel = "fsp0"
        plotter.plot_per_order(name, df_order.iloc[0][1:], df_order.iloc[1][1:],
                               df_deformation.iloc[8][1:], fsp0_its,
                               fsp0_kond, df_order.iloc[3][0],
                               df_order.iloc[2][1:],
                               its_type=f"{ylabel}_{type}_{defo}",
                               xlabel=defo, ylabel=ylabel)
        fsp1_its = df_deformation.iloc[7][1:]
        fsp1_kond = df_deformation.iloc[3][1:]
        ylabel = "fsp1"
        plotter.plot_per_order(name, df_order.iloc[0][1:], df_order.iloc[1][1:],
                               df_deformation.iloc[8][1:], fsp1_its,
                               fsp1_kond, df_order.iloc[3][0],
                               df_order.iloc[2][1:],
                               its_type=f"{ylabel}_{type}_{defo}",
                               xlabel=defo, ylabel=ylabel)
