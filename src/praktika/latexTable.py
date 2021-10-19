from dataclasses import field, dataclass
from enum import auto
from typing import Optional
from pandas import DataFrame, Series


@dataclass
class LatexTable:
    df: DataFrame
    index:  Optional[Series] = None
    label: str = ''
    caption: str = ''

    def __call__(self, file_name: str) -> None:
        self.heading(tab_label=self.label, caption=self.caption)
        self.index_row()
        if self.index:
            self.multirow()
        else:
            self.row()
        self.ending()
        self.save(file_name)

    def row(self):
        for idx, idx_val in enumerate(self.df.index):
            row_string = f'{idx_val}  &'
            for col_num, _ in enumerate(self.df.keys()):
                row_string += f'  {self.df.iloc[idx,col_num]}  &'
            self.output_string += [row_string[:-1] + r'\\']

    def multirow(self):
        old_idx = None
        old_multirow_num = 0
        new_multirow_num = 0
        for idx, idx_val in enumerate(self.df.index):
            multi_bool = False
            if idx_val == old_idx:
                row = r'  &'
                new_multirow_num += 1
            else:
                old_idx = idx_val
                row = r'\multirow{...}{*}{' + f'{idx_val}' + r'} &'
                new_multirow_num = 1

            if new_multirow_num <= old_multirow_num:
                multi_bool = True
                self.output_string[-old_multirow_num] = self.output_string[-old_multirow_num].replace(
                    '...', f'{old_multirow_num}')
            multirow_num = new_multirow_num

            if multi_bool and idx != len(self.df.index):
                self.output_string[-1] = self.output_string[-1] + r' \hline'
            old_multirow_num = multirow_num

            for col_num, _ in enumerate(self.df.keys()):
                row += f'  {self.df.iloc[idx,col_num]}  &'
            self.output_string += [row[:-1] + r'\\']
        self.output_string[-old_multirow_num] = self.output_string[-old_multirow_num].replace(
            '...', f'{old_multirow_num}')

    def save(self, fname):
        outfile = open(fname + '.tex', 'w')
        for val in self.output_string:
            outfile.write(val + '\n')
        outfile.close()

    def index_row(self):
        col_names = r'\begin{tabular}[c]{@{}c@{}} ' + \
            self.df.index.name + r' \end{tabular}  &'
        for col in self.df.keys():
            col_names += r'  \begin{tabular}[c]{@{}c@{}} ' + \
                col + r' \end{tabular}  &'
        col_names = col_names[:-1]
        col_names += r'\\'
        self.output_string += [col_names]
        self.output_string += [r'\midrule']

    def col_setup(self):
        col_setup = '{'
        for _ in range(len(self.df.keys()) + 1):
            col_setup += 'c'
        col_setup += '}'
        return col_setup

    def heading(self,  position='!htb', caption='', tab_label=''):
        self.output_string = []
        self.output_string += [r'\begin{table}[' + position + ']']
        self.output_string += [r'\centering']
        self.output_string += [r'\caption{' + caption + '}']
        self.output_string += [r'\label{tab:' + tab_label + '}']
        self.output_string += [r'\begin{tabular}' + self.col_setup()]
        self.output_string += [r'\toprule']

    def ending(self):
        self.output_string += [r'\bottomrule',
                               r'\end{tabular}', r'\end{table}']
