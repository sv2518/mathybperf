import os
import json
import glob
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_palette("deep")
current_palette = sns.color_palette()
plt.rcParams.update({'font.size': 16})

# collect json in all directories in home
home = './results/mixed_poisson/pplus1pow3/'
flames = './flames/mixed_poisson/pplus1pow3/'
trafo = 'trafo_none/'
cases = os.listdir(home)
plot_cases = ['case3', 'case0', 'case8', 'case4e', 'case6', 'case1', 'case2']
map_cases_experiments_to_thesis = {'case3': 'case3', 'case0': 'case2', 'case8': 'case1', 'case4e': 'case6',
                                   'case6': 'case7', 'case1': 'case4', 'case2': 'case5', 'case5': 'case7', 'case11': 'case9',
                                   'case12': 'case10'
                                   }
cellslist = [['cells_2'], ['cells_4']]
for cells in cellslist:
    time_data = {}
    its_data_outer = {}
    its_data_trace = {}
    dof_data = {}
    rows = []
    for case in cases:
        case_path = home+case
        if os.path.isdir(case_path) and case in plot_cases:
            orders = os.listdir(case_path+'/'+trafo)
            time_data_per_param = {}
            its_data_per_param_outer = {}
            its_data_per_param_trace = {}
            dof_data_per_param = {}
            index_names = []
            for order in orders:
                order_path = case_path+'/'+trafo+order+'/'
                if os.path.isdir(order_path):
                    if order:
                        index_names += [order[-1]]
                    for cell in cells:
                        cell_path = order_path+cell+'/'
                        files = glob.glob(cell_path+'*.json')
                        for file in files:
                            a = file.split("_warm")[0]
                            param = fr"{a}".split("/")[-1]
                            if param not in its_data_per_param_trace.keys():
                                its_data_per_param_trace.update({param: {}})
                            if param not in its_data_per_param_outer.keys():
                                its_data_per_param_outer.update({param: {}})

                            with open(file) as json_file:
                                its_outer = json.load(json_file)['outer_its']
                                if its_outer:
                                    its_data_per_param_outer[param][order[-1]] = its_outer

                            with open(file) as json_file:
                                its_trace = json.load(json_file)['trace_its']
                                if its_trace:
                                    its_data_per_param_trace[param][order[-1]] = its_trace

                        files = glob.glob(cell_path+'*extradata.tex')
                        for file in files:
                            a = file.split("_warm")
                            param = fr"{a}".split("/")[-1]
                            if param not in dof_data_per_param.keys():
                                dof_data_per_param.update({param: {}})

                            with open(file) as texfile:
                                data = int(texfile.readlines()[4].split("&")[3])
                                if data:
                                    dof_data_per_param[param][order[-1]] = data

                        cell_path = flames+case+'/'+trafo+order+'/'+cell+'/'
                        files = glob.glob(cell_path+'*.svg')
                        for file in files:
                            if 'warmed_up' in file:
                                a = file.split("_warm")[0]
                                param = fr"{a}".split("/")[-1]
                                if param not in time_data_per_param.keys():
                                    time_data_per_param.update({param: {}})
                                with open(file, 'r') as txt_file:
                                    text = str(txt_file.read())
                                finds = re.findall(re.compile("SNESSolve \(.* us"), text)
                                if finds:
                                    time = np.log(int((finds[0]).split('(')[1][:-3].replace(',', ''))/1000000)
                                else:
                                    time = 0
                                if time:
                                    time_data_per_param[param][order[-1]] = time

            rows = index_names
            for (key_t, value_t) in time_data_per_param.items():
                time_data[map_cases_experiments_to_thesis[case]] = time_data_per_param[key_t]
            for (key_i, value_i) in its_data_per_param_outer.items():
                its_data_outer[map_cases_experiments_to_thesis[case]] = its_data_per_param_outer[key_i]
            for (key_i, value_i) in its_data_per_param_trace.items():
                its_data_trace[map_cases_experiments_to_thesis[case]] = its_data_per_param_trace[key_i]
            for (key_i, value_i) in dof_data_per_param.items():
                dof_data[map_cases_experiments_to_thesis[case]] = dof_data_per_param[key_i]

    dofs = sorted(dof_data[map_cases_experiments_to_thesis['case3']].items())
    xlables = [f"p={k}\nDOFS={v}" for k, v in dofs]
    print(xlables)

    # save latex tables
    table_filename = home + 'table_time.tex'
    with open(table_filename, 'w') as convert_file:
        frame = pd.DataFrame(time_data).to_latex(index=True, index_names=rows)
        convert_file.write(frame)
        fig = plt.subplots(figsize=(12, 6))
        im = sns.heatmap(pd.DataFrame({k: {k2: np.exp(v2) for k2, v2 in v.items()} for k, v in time_data.items()}, index=rows).sort_index(0).sort_index(1), linewidth=2, square=True,
                         annot=True, fmt="5.1f", cbar=False, cmap="Reds", vmax=7500, annot_kws={"size": 14})

        im = sns.heatmap(pd.DataFrame(time_data, index=rows).sort_index(0).sort_index(1), linewidth=2, square=True,
                         cbar_kws={"orientation": "vertical", "extend": "max", 'label': 'log(runtime in seconds)'}, cmap="Reds", annot=False,
                         annot_kws={"size": 14}, fmt="5.1f", robust=True, vmax=9.5)

        im.set_xlim([0, 6])
        im.set_yticklabels(xlables)

        im2 = im.twiny()
        im2.set_aspect('equal')
        im2.set_ylim((0, 5))
        im2.set_xlim([1, 6])
        im2.axvline(color='black', linewidth=4, x=4)  # xy1=(3, 6.5), xy2=(3, -0.5))
        im2.axvline(color='black', linewidth=4, x=6)  # xy1=(5, 6.5), xy2=(5, -0.5))
        im2.set_xticks([2.5, 5, 7])
        im2.tick_params(axis=u'both', which=u'both', length=0)
        im2.set_xticklabels(['Group1', 'Group 2', 'Group 3'])

        im.spines['left'].set_position(('data', 0))
        sns.despine(left=True, bottom=True, ax=im2)
        labels = im2.get_xticklabels()
        for label in labels:
            label.set_fontweight('bold')

        cmap = plt.cm.get_cmap("Reds")
        cmap.set_bad("gray")
        plt.tight_layout()
        plt.savefig(f'./plots/table_time_{cells[0]}.pdf')

    table_filename = home + 'table_its_outer.tex'
    with open(table_filename, 'w') as convert_file:
        frame = pd.DataFrame(its_data_outer, index=rows).to_latex(index=True, index_names=rows)
        convert_file.write(frame)
        fig = plt.figure(figsize=(12, 6))
        im = sns.heatmap(pd.DataFrame(its_data_outer, index=rows).sort_index(0).sort_index(1), linewidth=2, square=True,
                         cbar_kws={"orientation": "vertical", 'label': 'trace solver iterations'}, cmap="Blues", annot=True, fmt='g', vmax=30, annot_kws={"size": 14})
        im.set_xlim([0, 6])
        im.set_yticklabels(xlables)

        im2 = im.twiny()
        im2.set_aspect('equal')
        im2.set_ylim((0, 5))
        im2.set_xlim([1, 6])
        im2.axvline(color='black', linewidth=4, x=4)  # xy1=(3, 6.5), xy2=(3, -0.5))
        im2.axvline(color='black', linewidth=4, x=6)  # xy1=(5, 6.5), xy2=(5, -0.5))
        im2.set_xticks([2.5, 5, 7])
        im2.tick_params(axis=u'both', which=u'both', length=0)
        im2.set_xticklabels(['Group1', 'Group 2', 'Group 3'])

        im.spines['left'].set_position(('data', 0))
        sns.despine(left=True, bottom=True, ax=im2)
        labels = im2.get_xticklabels()
        for label in labels:
            label.set_fontweight('bold')

        cmap = plt.cm.get_cmap("Blues")
        cmap.set_bad("gray")
        plt.tight_layout()
        plt.savefig(f'./plots/table_its_{cells[0]}_outer.pdf')

    table_filename = home + 'table_its_trace.tex'
    with open(table_filename, 'w') as convert_file:
        frame = pd.DataFrame(its_data_trace, index=rows).to_latex(index=True, index_names=rows)
        convert_file.write(frame)
        fig = plt.figure(figsize=(12, 6))
        im = sns.heatmap(pd.DataFrame(its_data_trace, index=rows).sort_index(0).sort_index(1), linewidth=2, square=True,
                         cbar_kws={"orientation": "vertical", 'label': 'trace solver iterations'}, cmap="Blues", annot=True, fmt='g', vmax=390, annot_kws={"size": 14})
        im.set_xlim([0, 6])
        im.set_yticklabels(xlables)

        im2 = im.twiny()
        im2.set_aspect('equal')
        im2.set_ylim((0, 5))
        im2.set_xlim([1, 6])
        im2.axvline(color='black', linewidth=4, x=4)  # xy1=(3, 6.5), xy2=(3, -0.5))
        im2.axvline(color='black', linewidth=4, x=6)  # xy1=(5, 6.5), xy2=(5, -0.5))
        im2.set_xticks([2.5, 5, 7])
        im2.tick_params(axis=u'both', which=u'both', length=0)
        im2.set_xticklabels(['Group1', 'Group 2', 'Group 3'])

        im.spines['left'].set_position(('data', 0))
        sns.despine(left=True, bottom=True, ax=im2)
        labels = im2.get_xticklabels()
        for label in labels:
            label.set_fontweight('bold')
        plt.tight_layout()
        plt.savefig(f'./plots/table_its_{cells[0]}_trace.pdf')
