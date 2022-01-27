import pandas as pd


def write_investigation_data(data, name, deformations):
    data_file = pd.DataFrame(data)
    data_file.columns = ["deformation from 1.0 in percentage : %d" % (d*100) for d in deformations]
    data_file.index = ["dofs", "eigs", "kond", "outer_its", "total_its"]
    data_file = data_file.transpose()
    data_file.to_csv(name, mode="w")
