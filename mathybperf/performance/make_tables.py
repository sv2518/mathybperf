import os
import json
import glob
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# collect json in all directories in home
home = '/Users/sv2518/firedrakeexamples/mathybperf/mathybperf/performance/results/mixed_poisson/pplus1pow3/'
flames = '/Users/sv2518/firedrakeexamples/mathybperf/mathybperf/performance/flames/mixed_poisson/pplus1pow3/'
trafo = 'trafo_none/'
cases = os.listdir(home)
plot_cases = ['case1','case2', 'case2d', 'case2i', 'case2j', 'case3', 'case4']
time_data = {}
its_data = {}
rows = []
for case in cases:
    case_path = home+case
    if os.path.isdir(case_path) and case in plot_cases:
        orders = os.listdir(case_path+'/'+trafo)
        time_data_inner = {}
        its_data_inner = {}
        time_data_per_param = {}
        its_data_per_param = {}
        index_names = []
        for order in orders:
            order_path = case_path+'/'+trafo+order+'/'
            if os.path.isdir(order_path):
                index_names += [order]
                cells = os.listdir(order_path)
                for cell in cells:
                    cell_path = order_path+cell+'/'
                    files = glob.glob(cell_path+'*.json')
                    for file in files:
                        a = file.split("_warm")[0]
                        param = fr"{a}".split("/")[-1]
                        if not param in its_data_per_param.keys():
                            its_data_per_param.update({param: {}})
                        with open(file) as json_file:
                            its = json.load(json_file)['outer_its']
                            if its:
                                its_data_per_param[param][order] = its

                    cell_path = flames+case+'/'+trafo+order+'/'+cell+'/'
                    files = glob.glob(cell_path+'*.svg')
                    for file in files:
                        if 'warmed_up' in file:
                            a = file.split("_warm")[0]
                            param = fr"{a}".split("/")[-1]
                            if not param in time_data_per_param.keys():
                                time_data_per_param.update({param: {}})
                            with open(file, 'r') as txt_file:
                                text = str(txt_file.read())
                            finds = re.findall(re.compile("all \(.* us"), text)
                            if finds:
                                time = (finds[0]).split('(')[1][:-3].replace(',', '')
                            else:
                                time = 0
                            if time:
                                time_data_per_param[param][order] = int(time) / 1000000
        if not rows or len(index_names)>len(rows):
            rows = index_names
        for (key_t, value_t) in time_data_per_param.items():
            time_data[case+"_"+key_t] = time_data_per_param[key_t]
        for (key_i, value_i) in its_data_per_param.items():
            its_data[case+"_"+key_i] = its_data_per_param[key_i]
print("Times", time_data)
print("Its", its_data)

# save latex tables
table_filename = home + 'table_time.tex'
with open(table_filename, 'w') as convert_file:
    frame = pd.DataFrame(time_data, index=rows).to_latex(index=True, index_names=rows)
    convert_file.write(frame)
    fig = plt.figure(figsize=(20, 7))
    sns.heatmap(pd.DataFrame(time_data, index=rows).sort_index().transpose().sort_index(), linewidth=1, square=True,
                cbar_kws={"orientation": "vertical"}, cmap="Reds", robust=True, annot=True, fmt="4.0f")
    plt.show()
table_filename = home + 'table_its.tex'
with open(table_filename, 'w') as convert_file:
    frame = pd.DataFrame(its_data, index=rows).to_latex(index=True, index_names=rows)
    convert_file.write(frame)
    fig = plt.figure(figsize=(20, 7))
    sns.heatmap(pd.DataFrame(its_data, index=rows).sort_index().transpose().sort_index(), linewidth=1, square=True,
                cbar_kws={"orientation": "vertical"}, cmap="Blues", robust=True, annot=True)
    plt.show()

