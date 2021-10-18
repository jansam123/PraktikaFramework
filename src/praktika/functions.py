import qexpy as q
import numpy as np
import pandas as pd
import re


def first_sqn(x):
    return -int(np.floor(np.log10(abs(x))))


first_sgn = np.vectorize(first_sqn)


def unit_to_latex(string, plt=None):
    if plt is None:
        text_style = 'text'
    else:
        text_style = 'mathrm'

    out = re.sub(r"([a-zA-Z]+)", r'\\'+text_style+r'{\1}', string)

    out = re.sub(r"\\\\"+text_style +
                 r"{([^}]*)}", r'\ \1', out).replace(' ', '')
    return out
