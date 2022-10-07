

from operator import index
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import seaborn as sns
import itertools
import re

from mathybperf.setup.setup_problem import problem
sns.set_palette("deep")
current_palette = sns.color_palette()
tips = ['o', 'v', 's', 'P', '*', "D", "X", 2, 1]
markers = itertools.cycle(tips)
plt.rcParams.update({'font.size': 20})


def tas_spectrum(plot_dir, orders, error_list, dof_group_list, timeoverall_list, sol, overlay=False, labels=[], per_order=True, case_counter=None):

    ####################################################################
    ############# MESH CONVERGENCE #####################################
    ####################################################################
    markers = itertools.cycle(tips)

    doa = [-np.log10(error) for error in error_list]  # digits of accuracy
    dos = [np.log10(dof) for dof in dof_group_list]  # digits of size

    fig4 = plt.figure(4, figsize=(5.33, 4))
    axis4 = fig4.gca()
    axis4.set_ylabel('DoA')
    axis4.set_xlabel('DoS')

    if per_order:
        for i, order in enumerate(orders):
            axis4.plot(dos[i], doa[i], label="p=%d" % order if not labels else "", marker=tips[case_counter] if case_counter else next(markers))
    else:
        axis4.plot([d[0] for d in dos], [d[0] for d in doa], marker=tips[case_counter] if case_counter else next(markers))

    axis4.legend() if not labels else axis4.legend(labels, ncol=2, frameon=True, loc="center", bbox_to_anchor=(0.5, 1.3))
    plt.tight_layout()
    axis4.grid(True)
    plt.rcParams.update({'font.size': 20})
    if not overlay:
        fig4.savefig(plot_dir+'tasMesh_'+sol+'.pdf')
    ####################################################################
    #############    STATIC SCALING  ###################################
    ####################################################################
    markers = itertools.cycle(tips)

    # static scaling
    fig5 = plt.figure(5, figsize=(5.33, 4))
    axis5 = fig5.gca()
    axis5.set_ylabel('DoF/s')
    axis5.set_xlabel('Time [s]')

    # gather static scaling information
    # unknowns per second
    dofpersecond = []
    if per_order:
        for i, order in enumerate(orders):
            dofpersecond.append([x/y for x, y in zip(dof_group_list[i], timeoverall_list[i])])  # needs to be adapted if we wrap a time stepper around
            axis5.loglog(timeoverall_list[i], dofpersecond[i], label="p=%d" % order if not labels else "", marker=tips[i])
    else:
        for i, order in enumerate(orders):
            dofpersecond.append([x/y for x, y in zip(dof_group_list[i], timeoverall_list[i])])  # needs to be adapted if we wrap a time stepper around
        axis5.loglog([t[0] for t in timeoverall_list], [d[0] for d in dofpersecond], label="p=%d" % order if not labels else "", marker=tips[case_counter] if case_counter else next(markers))

    plt.tight_layout()
    axis5.grid(True)
    if not overlay:
        fig5.savefig(plot_dir+'tasStatic_'+sol+'.pdf')

    ####################################################################
    ############# ACCURACY #############################################
    ####################################################################

    fig6 = plt.figure(6, figsize=(5.33, 4))
    axis6 = fig6.gca()
    axis6.set_ylabel('DoE')
    axis6.set_xlabel('Time [s]')

    doe = []
    for i, order in enumerate(orders):
        efficacy = [x*y for x, y in zip(error_list[i], timeoverall_list[i])]
        doe.append(-np.log10(efficacy))  # digits of efficacy

    if per_order:
        for i, order in enumerate(orders):
            axis6.semilogx((timeoverall_list[i]), doe[i], label="p=%d" % order if not labels else "", marker=tips[i])
    else:
        axis6.semilogx(([t[0] for t in timeoverall_list]), [d[0] for d in doe], label="p=%d" % order if not labels else "", marker=tips[case_counter] if case_counter else next(markers))

    plt.tight_layout()
    axis6.grid(True)
    if not overlay:
        fig6.savefig(plot_dir+'tasEfficacy_'+sol+'.pdf')

    ####################################################################
    ############# TRUE STATIC SCALING ##################################
    ####################################################################

    fig8 = plt.figure(8, figsize=(5.33, 4))
    axis8 = fig8.gca()
    axis8.set_ylabel('True DoF/s')
    axis8.set_xlabel('Time [s]')

    scaling = []
    truedofpersecond = []
    for i, order in enumerate(orders):
        scaling.append([x/y for x, y in zip(doa[i], dos[i])])
        truedofpersecond.append([x*y for x, y in zip(scaling[i], dofpersecond[i])])

    if per_order:
        for i, order in enumerate(orders):
            axis8.loglog(timeoverall_list[i], truedofpersecond[i], label="p=%d" % order if not labels else "", marker=tips[i])
    else:
        axis8.loglog([t[0] for t in timeoverall_list], [t[0] for t in truedofpersecond], label="p=%d" % order if not labels else "", marker=tips[case_counter] if case_counter else next(markers))

    plt.tight_layout()
    axis8.grid(True)
    if not overlay:
        fig8.savefig(plot_dir+'tasTrueStatic_'+sol+'.pdf')


def convergence_rates(error_list, dof_list, orders, type):
    rows_conv_rate = []
    for i, order in enumerate(orders):
        one_error_list = error_list[i]
        one_dof_list = dof_group_list[i]
        conv_rate = []
        conv_rate.append("p=%d" % (i+1))
        names = [0]
        for i, error in enumerate(one_error_list):
            if i < len(one_error_list)-1:
                conv_rate.append(np.log10(one_error_list[i]/one_error_list[i+1])/np.log10(np.sqrt(one_dof_list[i+1])/np.sqrt(one_dof_list[i])))
            else:
                conv_rate.append('-')
            names.append(one_dof_list[i])
        rows_conv_rate.append(conv_rate)

    datafile = pd.DataFrame(rows_conv_rate, columns=names).sort_index(axis=1)
    result = "convergence/"+case+"/timedata_taylorgreen_convergence"+type+".csv"
    if not os.path.exists(os.path.dirname("convergence/"+case+"/")):
        os.makedirs(os.path.dirname("convergence/"+case+"/"))
    datafile.to_csv(result, index=False, mode="w", header=True)

    return datafile


def convergence_rates_tolatex(velo_rows_conv_rate, pres_rows_conv_rate, veloerror_list, preserror_list):
    table = r"""
    \begin{table}
    \begin{center}
    \resizebox{0.57\textwidth}{!}{%
    \begin{tabular}{| l | c | c | c | c | c |}
    \hline
    \multicolumn{6}{|c|}{SPCS-IP method ($t_{max} =1\times e-9$)} \\
    \hline
    \multirow{2}{*}{$k$} &
    \multirow{2}{*}{DoF}&
    \multicolumn{2}{|c|}{
    $\norm{\boldsymbol{u}-\boldsymbol{u}_h}_{\boldsymbol{L}^2(\Omega)} \leq \mathcal{O}(d^{k+1})$} &
    \multicolumn{2}{|c|}{$\norm{p-p_h}_{L^2(\Omega)}\leq \mathcal{O}(d^{k+2})$} &
    \cline{3-6}
    & & $L^2$-error & rate & $L^2$-error & rate \\
    """

    lformat = r"""& {dof: d} & {veloerror:.3e} & {velorate} & {preserr:.3e} & {presrate}\\
    """

    dofs_list = velo_rows_conv_rate.columns.tolist()[1:]

    for j, order in enumerate(velo_rows_conv_rate[0]):
        table += r"""
        \hline
        \hspace{0.1cm}%s\hspace{0.1cm}    
        """ % order

        s = "\\\\"
        for i, dofs in enumerate(dofs_list):
            table += r"""
            &%s
            """ % str(dofs)

            try:

                table += r"""
                &%.3e
                """ % float(veloerror_list[j][i])

                table += r"""
                &%.2f
                """ % float(velo_rows_conv_rate.iloc[j, i+1])

                table += r"""
                &%.3e
                """ % float(preserror_list[j][i])

                table += r"""
                &%.2f\\
                """ % float(pres_rows_conv_rate.iloc[j, i+1])

            except ValueError:

                table += r"""
                &%s
                """ % (velo_rows_conv_rate.iloc[j, i+1])

                table += r"""
                &%.3e
                """ % float(preserror_list[j][i])

                table += r"""
                &%s\\
                """ % (pres_rows_conv_rate.iloc[j, i+1])

        table += r"""\hline"""

    table += r"""\end{tabular}}
    \end{center}
    \caption{Error and convergence rates for velocity and pressure}
    \label{tab:conv}
    \end{table}"""
    print(table)


def gather_data(base_dir, folder, folder_flames, case, ctype, params, cells_per_dim, orders):
    # gather data from all files
    # gather all filenames
    files = [[f"{base_dir}{folder}{case}/{ctype}order_{o}/cells_{c}/{params}_warmed_up_order{o}_cells{c}.csv" for c in cells_per_dim] for o in orders]
    files_flames = [[f"{base_dir}{folder_flames}{case}/{ctype}order_{o}/cells_{c}/{params}_warmed_up_flame.svg" for c in cells_per_dim] for o in orders]

    for i, order in enumerate(orders):
        cell_data = pd.concat(pd.read_csv(cell_files, nrows=1) for cell_files in files[i])

        # order data by dof number and append to group by order list
        # dof_data.append(cell_data.groupby(["trace dofs (part of velo dofs)"], as_index=False))
        dof_data.append(cell_data.groupby(["sum dofs"], as_index=False))

        # gather all dofs
        # dof_group_list.append([d[1] for d in cell_data["trace dofs (part of velo dofs)"].items()])#use sum dofs instead
        dof_group_list.append([d[1] for d in cell_data["sum dofs"].items()])  # use sum dofs instead

        # gather all times, decide here which times to use!
        # timeoverall_list.append([e[1] for e in cell_data["HybridTraceSolve"].items()])
        times = []
        for file in files_flames[i]:
            with open(file, 'r') as txt_file:
                text = str(txt_file.read())
                finds = re.findall(re.compile("SNESSolve \(.* us"), text)
                time = int((finds[0]).split('(')[1][:-3].replace(',', ''))/1000000 if finds else 0
            times.append(time)
        timeoverall_list.append(times)

        # gather all errors
        veloerror_list.append([e[1] for e in cell_data["L2Velo"].items()])
        preserror_list.append([e[1] for e in cell_data["L2Pres"].items()])
    print(timeoverall_list)
    return veloerror_list, preserror_list, dof_group_list, timeoverall_list


################ !!!!!!!!!!!!!!!! SETUP !!!!!!!!!!!!!! ####################
affine_trafo = "none"
base_dir = "./"
folder = "results/mixed_poisson/pplus1pow3/"
folder_flames = "flames/mixed_poisson/pplus1pow3/"
ctype = "trafo_" + affine_trafo + "/"


################ Plot TAS for each case seperately and increase size by refining the mesh ####################
case_list = ['case0',
             'case1',
             'case2',
             'case3',
             'case4e',
             'case6',
             'case8']  # case name by experiment
params_list = ['hybridization_cg_params',
               'hybridization_global_matfree_cg',
               'gtmg_global_matfree_params_matexpmg_assembledjacobi_fgmres',
               'gtmg_matexpl_params',
               'gtmg_fully_matfree_params_matexpmg_fgmres_assembledjacobi',
               'gtmg_fully_matfree_params_fs0_cg_jacobi_fs1_cg_laplacian_jacobi_fgmres',
               'native_dg']
order_labels = {'c3', 'c2', 'c1', 'c6', 'c8', 'c4', 'c5', 'c7', 'c9'}


for params, case in zip(params_list, case_list):
    print("Plotting " + case)
    orders = list(range(5)) if not case in ['case5', 'case6', 'case8'] else list(range(4))
    cells_per_dim = range(1, 5)

    # read-in all data
    dof_data = []
    dof_group_list = []  # per order per cell per dim dofs
    timeoverall_list = []
    veloerror_list = []
    preserror_list = []
    p_list = []
    veloerror_list, preserror_list, dof_group_list, timeoverall_list = gather_data(base_dir, folder, folder_flames, case, ctype, params, cells_per_dim, orders)

    # make folder for this case
    plot_dir = f"{base_dir}plots/tas/{case}/"
    if not os.path.exists(os.path.dirname(plot_dir)):
        os.makedirs(os.path.dirname(plot_dir))

    # plot tas spectrum for velocity
    tas_spectrum(plot_dir, orders, veloerror_list, dof_group_list, timeoverall_list, "velo")

    plt.close(4)
    plt.close(5)
    plt.close(6)
    plt.close(8)

    # plot tas spectrum for pressure
    tas_spectrum(plot_dir, orders, preserror_list, dof_group_list, timeoverall_list, "pres")

    plt.close(4)
    plt.close(5)
    plt.close(6)
    plt.close(8)


################ Plot TAS for each case together and increase size by refining the mesh ####################

for c, (params, case) in enumerate(zip(params_list, case_list)):
    print("Plotting " + case)
    orders = [3]
    cells_per_dim = range(1, 5)
    overlay = False if c == len(params_list)-1 else True

    # read-in all data
    dof_data = []
    dof_group_list = []  # per order per cell per dim dofs
    timeoverall_list = []
    veloerror_list = []
    preserror_list = []
    p_list = []
    veloerror_list, preserror_list, dof_group_list, timeoverall_list = gather_data(base_dir, folder, folder_flames, case, ctype, params, cells_per_dim, orders)

    # make folder for this case
    plot_dir = f"{base_dir}plots/tas/allcases/permeshsize/"
    if not os.path.exists(os.path.dirname(plot_dir)):
        os.makedirs(os.path.dirname(plot_dir))

    # plot tas spectrum for velocity
    tas_spectrum(plot_dir, orders, veloerror_list, dof_group_list, timeoverall_list, "velo", overlay=overlay, labels=order_labels)

plt.close(4)
plt.close(5)
plt.close(6)
plt.close(8)

for c, (params, case) in enumerate(zip(params_list, case_list)):
    print("Plotting " + case)
    orders = [3]
    cells_per_dim = range(1, 5)
    overlay = False if c == len(params_list)-1 else True

    # read-in all data
    dof_data = []
    dof_group_list = []  # per order per cell per dim dofs
    timeoverall_list = []
    veloerror_list = []
    preserror_list = []
    p_list = []
    veloerror_list, preserror_list, dof_group_list, timeoverall_list = gather_data(base_dir, folder, folder_flames, case, ctype, params, cells_per_dim, orders)

    # make folder for this case
    plot_dir = f"{base_dir}plots/tas/allcases/permeshsize/"
    if not os.path.exists(os.path.dirname(plot_dir)):
        os.makedirs(os.path.dirname(plot_dir))

    # plot tas spectrum for velocity
    tas_spectrum(plot_dir, orders, preserror_list, dof_group_list, timeoverall_list, "pres", overlay=overlay, labels=order_labels)

plt.close(4)
plt.close(5)
plt.close(6)
plt.close(8)


################ Plot TAS for each case together and increase size by refining the degree ####################

case_list = ['case2',
             'case3',
             'case4e',
             'case6',
             ]
params_list = ['gtmg_global_matfree_params_matexpmg_assembledjacobi_fgmres',
               'gtmg_matexpl_params',
               'gtmg_fully_matfree_params_matexpmg_fgmres_assembledjacobi',
               'gtmg_fully_matfree_params_fs0_cg_jacobi_fs1_cg_laplacian_jacobi_fgmres',
               ]

order_labels = ['case5', 'case3', 'case6', 'case7', 'case1']  # rename cases according to the thesis

for c, (params, case) in enumerate(zip(params_list, case_list)):
    print("Plotting " + case)
    orders = list(range(5)) if not case in ['case5', 'case6', 'case8'] else list(range(4))
    cells_per_dim = range(4, 5)
    overlay = False if c == len(params_list)-1 else True

    # read-in all data
    dof_data = []
    dof_group_list = []  # per order per cell per dim dofs
    timeoverall_list = []
    veloerror_list = []
    preserror_list = []
    p_list = []
    veloerror_list, preserror_list, dof_group_list, timeoverall_list = gather_data(base_dir, folder, folder_flames, case, ctype, params, cells_per_dim, orders)

    # make folder for this case
    plot_dir = f"{base_dir}plots/tas/allcases/perdegree/"
    if not os.path.exists(os.path.dirname(plot_dir)):
        os.makedirs(os.path.dirname(plot_dir))

    # plot tas spectrum for velocity
    tas_spectrum(plot_dir, orders, veloerror_list, dof_group_list, timeoverall_list, "velo", overlay=overlay, labels=order_labels, per_order=False, case_counter=c)

plt.close(4)
plt.close(5)
plt.close(6)
plt.close(8)

for c, (params, case) in enumerate(zip(params_list, case_list)):
    print("Plotting " + case)
    orders = list(range(0, 5)) if not case in ['case5', 'case6', 'case8'] else list(range(4))
    cells_per_dim = range(4, 5)
    overlay = False if c == len(params_list)-1 else True

    # read-in all data
    dof_data = []
    dof_group_list = []  # per order per cell per dim dofs
    timeoverall_list = []
    veloerror_list = []
    preserror_list = []
    p_list = []
    veloerror_list, preserror_list, dof_group_list, timeoverall_list = gather_data(base_dir, folder, folder_flames, case, ctype, params, cells_per_dim, orders)

    # make folder for this case
    plot_dir = f"{base_dir}plots/tas/allcases/perdegree/"
    if not os.path.exists(os.path.dirname(plot_dir)):
        os.makedirs(os.path.dirname(plot_dir))

    # plot tas spectrum for velocity
    tas_spectrum(plot_dir, orders, preserror_list, dof_group_list, timeoverall_list, "pres", overlay=overlay, labels=order_labels, per_order=False, case_counter=c)
