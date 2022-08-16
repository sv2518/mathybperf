import pandas as pd


def write_investigation_data(data, name, rows=None, columns=None):
    data_file = pd.DataFrame(data)
    if columns:
        data_file.columns = columns
    data_file.to_csv(name, mode="w", index=rows)
