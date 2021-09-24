import qexpy as q
import numpy as np
import pandas as pd
import re


def first_sqn(x):
    return -int(np.floor(np.log10(abs(x))))

first_sgn = np.vectorize(first_sqn)
  

def unit_to_latex(string, plt=None):
    if plt is None:
        return re.sub(r"([a-zA-Z]+)", r'\\text{\1}', string)
    else:
        return re.sub(r"([a-zA-Z]+)", r'\\mathrm{\1}', string)




