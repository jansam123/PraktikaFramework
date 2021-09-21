import qexpy as q
import numpy as np
import pandas as pd
import re



def get_data(name, col=[], errors=[], NaN=False, numpy=False, sep=";", decimal=",", file_type='.csv'):
    name = str(name) + file_type
    if file_type == '.csv':
        data = pd.read_csv(name, sep=sep, decimal=decimal)
    elif file_type == '.xlsx' or file_type == '.xls':
        data = pd.read_excel(name)

    if NaN:
        for i in data.columns:
            index = data[i].index[data[i].apply(np.isnan)]
            data = data.drop(index)

    if len(col) > 1:
        if numpy:
            out = [data[c].to_numpy() for c in col]
        else:
            out = [q.MeasurementArray(data[c].to_numpy(), errors[j]) for j, c in enumerate(col)]
    else:
        if numpy:
            out = data[col[0]].to_numpy()
        else:
            out = q.MeasurementArray(data[col[0]].to_numpy(), errors[0])

    return out


def first_sqn(x):
    return -int(np.floor(np.log10(abs(x))))

first_sgn = np.vectorize(first_sqn)
  

def unit_to_latex(string, plt=None):
    if plt is None:
        return re.sub(r"([a-zA-Z]+)", r'\\text{\1}', string)
    else:
        return re.sub(r"([a-zA-Z]+)", r'\\mathrm{\1}', string)




