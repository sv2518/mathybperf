from mathybperf import *

# Setup
folder = "./results/mixed_poisson/"
type = "affine"  # or "nonaffine/" or "nodeform/"
case = "/(p+1)**3/"
test = "cgjacobi"
defo = "deformations"  # or "scalings"
name = folder + type + case + test

# Read the data
df_deformation = pd.read_csv(name+"_per_deformation.csv")
df_order = pd.read_csv(name+"_per_order.csv")

# Plot the data
plotter = ResultPlotter()
outer_its = df_deformation.iloc[2][1:]
plotter.plot_per_order(name, df_order.iloc[0][1:], df_order.iloc[1][1:],
                       df_deformation.iloc[4][1:], outer_its,
                       df_deformation.iloc[1][1:], df_order.iloc[3][0],
                       df_order.iloc[2][1:],
                       its_type=f"outer_{type}_{defo}", xlabel=defo)
total_its = df_deformation.iloc[3][1:]
plotter.plot_per_order(name, df_order.iloc[0][1:], df_order.iloc[1][1:],
                       df_deformation.iloc[4][1:], total_its,
                       df_deformation.iloc[1][1:], df_order.iloc[3][0],
                       df_order.iloc[2][1:],
                       its_type=f"total_{type}_{defo}", xlabel=defo)
