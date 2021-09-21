import qexpy as q
import numpy as np
import pandas as pd
import praktika.functions as fce
import praktika.latexTable as tab



class Table(object):

    def __init__(self, columns, index=0, ignore_error=[], inline_error=False, save=None, fname='data_to_table'):
        self.columns = columns
        self.col_names = []
        self.df = pd.DataFrame()

        if isinstance(index, pd.Series):
            self.index = index

        self.add_all_col(index, inline_error, ignore_error)
        self.set_index()

        if save is not None:
            self.save(save, fname)


    def add_all_col(self, index, inline_error, ignore_error):
        for col_id, col in enumerate(self.columns):
            apply_err = False if col_id in ignore_error else True
            col_name = self.add_col(col, apply_err, inline_error)
            if type(index) is int and col_id == index:
                self.index = col_name
        


    def add_col(self, col, apply_err=True, inline_err=False):
        values, errors = self.set_val_err(col)
        if errors is None or np.all(np.array(errors) == errors[0]):
            apply_err = False
        name = col.name

        col_name = r"${}$".format(name)
        if hasattr(col, 'un'):
            col_name += r" \\ $[{}]$".format(fce.unit_to_latex(col.un))
            
        if apply_err:
            err_col_name = r"$\sigma_{}$".format("{" + str(name) + "}")
            if hasattr(col, 'un'):
                err_col_name += r" \\ $[{}]$".format(fce.unit_to_latex(col.un))


        self.col_names += [col_name]
        if inline_err and apply_err:
            inline_values = []
            for val, err in zip(values, errors):
                inline_values += [r"${} \pm {}$".format(val, err).replace('.', ',')]

            self.df[col_name] = inline_values 
        elif apply_err:
            self.df[col_name] = values
            self.df[err_col_name] = errors
            self.col_names += [err_col_name]
        else:
            self.df[col_name] = values
        return col_name
        

    def set_val_err(self, col):
        values = []
        if np.any(col.errors == 0):
            for val in col.values:
                if val == 0:
                    values += [int(val)]
                else:
                    round_val = round(val, 0)
                    round_val = int(round_val)
                    values += [str(round_val).replace('.', ',')]
            return values, None

        errors = []
        for err, val in zip(col.errors, col.values):
            round_err = round(err, fce.first_sgn(err))
            round_val = round(val, fce.first_sgn(round_err))

            if round_err >= 1:
                round_err = int(round_err)
                round_val = int(round_val)

            errors += [str(round_err).replace('.', ',')]
            values += [str(round_val).replace('.', ',')]
        return values, errors

    def round_list(self, list, digit):
        values = []
        for val in list:
            round_val = round(val, digit)
            if digit > 1:
                round_val = int(round_val)
            values += [round_val]
        return values

    def set_index(self):
        self.df = self.df.set_index(self.index)

    def save(self, save_as, fname):
        if save_as == 'csv':
            self.df.to_csv(fname + '.csv', sep=";", decimal=",", index=True)

        elif save_as == 'tex':
            if isinstance(self.index, pd.Series): 
                tab.latexTable(self.df, fname, True, label=fname.split('/')[-1])
            else:
                tab.latexTable(self.df, fname, label=fname.split('/')[-1])

        elif save_as == 'latex':
            self.df.to_latex(fname + '.tex', escape=False, multirow=True, multicolumn=True)
        
