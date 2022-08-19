from operator import index
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import seaborn as sns
import re
from math import sqrt

# choose what to plot
complexities = False
solve_dominance = True

sns.set_palette("deep")
current_palette = sns.color_palette()
tips = ['o', 'v', 's', 'P', '*', "D", "X", 2]
plt.rcParams.update({'font.size': 18})


orders = range(6)
scalings = [1.0]
deformations = [0]  # 0.5*d for d in range(0,21)
add_to_quad_degree = (0, 0)
cells_per_dim = 2

folder = "mixed_poisson/pplus1pow3/"
case = "case0/trafo_none/"
params = "hybridization_global_matfree_cg"
type = "_warmed_up"
name = folder + case

# read-in all dat
dof_data = []
timeoverall_list = []
p_list = []

cg_its = np.zeros(len(orders))
files = ["results/" + name + f"order_{o}/cells_2/" + params + type + f"_its.json"
         for o in orders]
iteration_numbers = np.zeros(len(orders))
for i, file in enumerate(files):
    try:
        with open(file, 'r') as txt_file:
            its = int(str(txt_file.read()).strip('{').strip('}').split(":")[-1])
    except FileNotFoundError:
        its = 1
    iteration_numbers[i] = its

# gather data from all files
files = ["flames/" + name + f"order_{o}/cells_2/" + params + type + f"_flame.txt"
         for o in orders]
time_data = np.zeros(len(orders))
time_data_ls_nits = np.zeros(len(orders))
time_data_gs_nits = np.zeros(len(orders))
time_data_nits  = np.zeros((len(orders), 2))
for i, file in enumerate(files):
    print(file)
    with open(file, 'r') as txt_file:
        text = str(txt_file.read())
    text = text.split("\n")
    finds_getrf = [match for match in text if "SCSolve" in match
                   and "solve_getrf " in match]
    finds_scsolve = [match for match in text if "wrap_slate_loopy_knl_3" in match]
    if finds_getrf and finds_scsolve:
        time_data[i] = (sum(int(f.split()[-1]) for f in finds_getrf) /
                        (sum(int(f.split()[-1]) for f in finds_scsolve)))
        time_data_ls_nits[i] = (sum(int(f.split()[-1]) for f in finds_getrf)
                                / iteration_numbers[i])/1e6
        time_data_gs_nits[i] = (sum(int(f.split()[-1]) for f in finds_scsolve)
                                / iteration_numbers[i])/1e6
        time_data_nits[i] = [time_data_ls_nits[i], time_data_gs_nits[i]]
    else:
        time_data[i] = 0
        time_data_ls_nits[i] = 0
        time_data_gs_nits[i] = 0
        time_data_nits[i] = 0

if solve_dominance:
    script_dir = os.path.dirname(__file__)
    df = pd.DataFrame(time_data_nits, columns=["Local solve time",
                                               "Trace solve time"])
    ax = df.plot.bar(rot=0, figsize=(8,6))
    ax.set_xlabel("Polynomial degree (outer CG iterations)")
    ax.set_ylabel('Average time [s] per CG iteration')
    ax.set_xticklabels([f"{i} ({int(j)})" for i, j
                        in zip(range(6), iteration_numbers)])
    plt.savefig(script_dir+"/plots/bottleneck/avg_time_per_cg.png")

    df2 = pd.DataFrame(time_data_ls_nits/time_data_gs_nits*100)
    ax = df2.plot.bar(rot=0, figsize=(8,6), legend=False)
    ax.set_xlabel("Polynomial degree (outer CG iterations)")
    ax.set_xticklabels([f"{i} ({int(j)})" for i, j
                        in zip(range(6), iteration_numbers)])
    ax.set_ylabel('Ratio [%] of local to global solve time')
    plt.savefig(script_dir+"/plots/bottleneck/local_vs_global_solve.png")

if complexities:
    # plot complexities for local Slate kernel of the Schur complement in the trace solve
    sizes = np.array([7, 44, 135, 304, 575, 972])

    local_assembly = np.array([(p+1)**(2*3+1) for p in orders])
    local_assembly_matfree = np.array([(p+1)**(3+1) for p in orders]) 

    local_solves = np.array([2/3*n**3 for n in sizes])
    local_solves_matfree = np.array([p**(3+1) for n, p in zip(sizes, orders)])

    local_linear_algebra = np.array([2*n*(2*n-1) for n in sizes])  # 2 matvecs
    local_linear_algebra_matfree = np.array([2*p**(3+1) for n, p in zip(sizes, orders)]) # 2 matvecs

    slate_kernel_nosolve = local_linear_algebra+local_assembly
    slate_kernel = local_linear_algebra+local_solves+local_assembly
    slate_kernel_matfree = local_linear_algebra_matfree+local_solves_matfree+local_assembly_matfree

    measured_flops = np.zeros(len(orders))
    measured_flops_nosolve = np.zeros(len(orders))
    files = ["results/" + name + f"order_{o}/cells_2/" + params + type + f"_slate_flops.txt" for o in orders]
    print(files)
    for i, file in enumerate(files):
        try:
            with open(file, 'r') as txt_file:
                data = str(txt_file.read()).split()
                idx = data.index("wrap_slate_loopy_knl_3:")
                count = int(data[idx+1])
        except FileNotFoundError:
            count = 1
        measured_flops_nosolve[i] = count
        measured_flops[i] = count

    plt.figure(figsize=(10, 7))
    plt.semilogy(orders[:-1],  slate_kernel_matfree[:-1], 's--',
                color=current_palette[3],  label="matfree theoretical including solve")
    plt.semilogy(orders[:-1],  slate_kernel_nosolve[:-1], 'o--',
                color=current_palette[1],  label="theoretical excluding solve")
    plt.semilogy(orders[:-1], measured_flops_nosolve[:-1], 'o-',
                color=current_palette[1],  label="practical excluding solve")
    plt.semilogy(orders[:-1], measured_flops_nosolve[:-1]+local_solves[:-1], 'D-',
                color=current_palette[0],  label="practical including solve")
    plt.semilogy(orders[:-1],  slate_kernel[:-1], 'D--',
                color=current_palette[0], label="theoretical FLOPS including solve")
    plt.xticks(orders[:-1])
    plt.ylabel('FLOPS')
    plt.xlabel("Polynomial degree")
    plt.grid()
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 7))
    ptothe3 = [(p+1)**3 for p in orders]
    plt.semilogy(orders[:-1],  ptothe3[:-1]/slate_kernel_matfree[:-1], 's--',
                color=current_palette[3],  label="matfree theoretical including solve")
    plt.semilogy(orders[:-1],  ptothe3[:-1]/slate_kernel_nosolve[:-1], 'o--',
                color=current_palette[1],  label="theoretical excluding solve")
    plt.semilogy(orders[:-1], ptothe3[:-1]/measured_flops_nosolve[:-1], 'o-',
                color=current_palette[1],  label="practical excluding solve")
    plt.semilogy(orders[:-1], ptothe3[:-1]/(measured_flops_nosolve[:-1]+local_solves[:-1]), 'D-',
                color=current_palette[0],  label="practical including solve")
    plt.semilogy(orders[:-1],  ptothe3[:-1]/slate_kernel[:-1], 'D--',
                color=current_palette[0], label="theoretical FLOPS including solve")
    plt.xticks(orders[:-1])
    plt.ylabel('FLOPS/s')
    plt.xlabel("Polynomial degree")
    plt.grid()
    plt.legend()
    plt.show()

    # plot distribution of different bits
    plt.figure(figsize=(10, 7))
    print(slate_kernel)
    plt.semilogy(orders, local_assembly, '>-', label="assembly")
    plt.semilogy(orders, local_solves, 'o-', label="solve")
    plt.semilogy(orders, local_linear_algebra, 's-', label="simple linear algebra")
    plt.semilogy(orders, slate_kernel, 'x--', color='black', label="Slate kernel")
    plt.ylabel('FLOPS')
    plt.xlabel("Polynomial degree")
    plt.grid()
    plt.legend()
    plt.show()

    # plot complexity of global kernel
    number_elements = (2**3)**3
    global_matvec = np.array([number_elements * s for s in slate_kernel])
    cg = np.array([gmv*its for its, gmv
                in zip(iteration_numbers, global_matvec)])

    plt.figure(figsize=(10, 7))
    plt.semilogy(orders, iteration_numbers, 'D-', label="iterations")
    plt.semilogy(orders, global_matvec, 's-', label="MatVec (Slate)")
    plt.semilogy(orders, cg, 'x--', color='black', label="CG kernel")
    plt.ylabel('FLOPS')
    plt.xlabel("Polynomial degree")
    plt.grid()
    plt.legend()
    plt.show()
