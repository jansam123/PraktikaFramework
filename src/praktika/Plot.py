import qexpy as q
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import container
import seaborn as sns
import matplotlib.style as style
import praktika.functions as fce
from scipy.interpolate import make_interp_spline

import locale
locale.setlocale(locale.LC_NUMERIC, "de_DE")


class Plot(object):

    def __init__(self, xdata, ydata, xlabel=None, ylabel=None, ax=None, fig=None, fname=None, 
                 fmt='o', label=None, color=None, exclude=None, grid=False, model=None, guess=None, model_fmt='-', show_dispersion=True, 
                 no_errbar=False, no_points=False, degree=None, spline=False, graph_save_path = 'LaTeX/graphs/'): 
        self.xdata = xdata
        self.ydata = ydata
        self.set_visual()
        self.set_axis(ax, fig)
        self.no_points = no_points
        self.leg_label = label
        self.degree = degree
        self.graph_save_path = graph_save_path


        self.ax.grid(grid)

        if no_errbar:
            points = self.ax.plot(self.xdata.values, self.ydata.values, fmt=fmt, label=label, ms=8, color=color)
            self.color = points[-1][-1].get_color()
        elif no_points:
            self.color = None
        else:
            points = self.ax.errorbar(self.xdata.values, self.ydata.values, yerr=self.ydata.errors, fmt=fmt, label=label, capsize=4, ms=8, color=color)
            self.color = points[-1][-1].get_color()

        if None not in [model, guess]:
            self.fit(model, guess, exclude)
            self.plot_fit(model, fmt=model_fmt, show_dispersion=show_dispersion)

        if spline:
            if exclude is not None:
                x = xdata.delete(exclude).values
                y = ydata.delete(exclude).values
            else:
                x = xdata.values
                y = ydata.values
                
            X_Y_Spline = make_interp_spline(x, y)
            X_ = np.linspace(x.min(), x.max(), 500)
            Y_ = X_Y_Spline(X_)
            self.ax.plot(X_, Y_, color=self.color)

        self.label(xlabel, 'x')
        self.label(ylabel, 'y')        
        if label is not None:
            self.legend()
        self.save(fname)
                            

    def set_axis(self, ax, fig):
        if ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.ax = ax
            self.fig = fig


    def label(self, label, axis):
        label_attr = getattr(self.ax, f'set_{axis}label')
        if label is not None:
            label_attr(label)
        elif getattr(self.ax, f'{axis}axis').get_label().get_text() == '':
            data = getattr(self, f'{axis}data')
            if hasattr(data, 'un') and hasattr(data, 'name'):
                name = data.name
                unit = fce.unit_to_latex(data.un, plt=True)
                label_attr(f'${name} \ [{unit}]$')
                
            elif hasattr(data, 'name'):
                label_attr(f'${data.name} \ [1]$')


    def legend(self, facecolor='white'):
        handles, labels = self.ax.get_legend_handles_labels()
        handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
        self.ax.legend(handles, labels, facecolor=facecolor)


    def fit(self, model, guess, exclude=None):
        if exclude is not None:
            fit = q.fit(self.xdata.delete(exclude), self.ydata.delete(exclude), model, parguess=guess, degree=self.degree)    
        else:
            fit = q.fit(self.xdata, self.ydata, model, parguess=guess, degree=self.degree)

        self.params = [exp_val.value for exp_val in fit.params]
        self.params_err = [exp_val.error for exp_val in fit.params]
        self.regress_coeff = fit.params
    
    def plot_fit(self, model, npoints=None, fmt='-', show_dispersion=True):
        if npoints is None:
            npoints=20*len(self.xdata.values)
        x_fit = np.linspace(self.xdata.values.min(), self.xdata.values.max(), npoints)
        model_vals = model(x_fit, *self.params)
        if self.no_points:
            label = self.leg_label
        else:
            label = None
        self.ax.plot(x_fit, model_vals, fmt, zorder=10, color=self.color, label=label)
        if show_dispersion:
            model_valsPlus = model(x_fit, *[param + err for param, err in zip(self.params,self.params_err)])
            model_valsMinus = model(x_fit,*[param - err for param, err in zip(self.params,self.params_err)])
            self.ax.fill_between(x_fit, model_valsMinus, model_valsPlus, color=self.color, alpha=0.35)


    def save(self, fname):
        if fname is not None:
            self.fig.savefig(self.graph_save_path+fname + '.png')


    def get_fig(self):
        return self.ax, self.fig


    def set_visual(self, sns_context='paper', mt_style='ggplot'):
        plt.rcParams['axes.formatter.use_locale'] = True
        sns.set_context(sns_context)
        style.use(mt_style)
        plt.rcParams.update({
            "font.family": "monospace",
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 11,
            "text.color": "black",
            'axes.labelcolor': "black",
            'xtick.color': 'black',
            'ytick.color': 'black',
            "axes.facecolor"    : "#c7ddff",   
            "figure.facecolor"  : "#f2f2f2",  
            "figure.edgecolor"  : "#ffffff",   
            "axes.formatter.use_locale" : True
            })


