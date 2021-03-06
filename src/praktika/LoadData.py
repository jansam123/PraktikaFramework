import pandas as pd
from praktika import Data


class LoadData(object):

    def __init__(self, file_name, error=True, to_numpy=False, separator=";", decimal=",", file_type='.xlsx'):
        self.out = []
        self.load(file_name, file_type, separator, decimal)

        self.to_numpy()
        if not to_numpy:
            self.to_Data(error)

    def to_numpy(self):
        self.np = [self.df[col].dropna().to_numpy() for col in self.df]

    def to_Data(self, error):
        if not error:
            self.out = [Data(col) for col in self.np]
            return

        for col in self.np:
            err = col[0]

            if type(err) is str:
                self.out += [Data(col[1:], self.dif_err(col[0], col[1:]))]
            else:
                self.out += [Data(col[1:], err)]

    def load(self, fname, file_type, separator, decimal):
        fname = fname + file_type
        if file_type == '.csv':
            self.df = pd.read_csv(fname, sep=separator, decimal=decimal)
        elif file_type == '.xlsx' or file_type == '.xls':
            self.df = pd.read_excel(fname)

    def dif_err(self, string, values):
        string = string.replace(' ', '').replace(',', '.')
        string = string.split('+')
        relative = float([val for val in string if '%' in val]
                         [0].replace('%', ''))
        absolute = float([val for val in string if '%' not in val][0])

        return [abs(val)*relative*1e-2 + absolute for val in values]

    def __str__(self):
        out = ''
        for val in self.out:
            out += val.__str__() + ' '
        return out
