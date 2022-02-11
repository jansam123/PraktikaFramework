from dataclasses import dataclass
import qexpy as q
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import container
import seaborn as sns
import matplotlib.style as style
import praktika.functions as fce
from scipy.interpolate import make_interp_spline
import locale
from praktika.Data import Data
from typing import Protocol, Callable, Optional
import inspect

locale.setlocale(locale.LC_NUMERIC, "de_DE")

ggplot_colors = {'red': '#E24A33', 'blue': '#348ABD',
                 'magenta': '#988ED5', 'gray': '#777777', 'yellow': '#FBC15E', 'green': '#8EBA42', 'pink': '#FFB5B8'}


def listOfMeasurement_to_Data(x: list[q.Measurement]) -> Data:
    return Data([meas.value for meas in x],  [meas.error for meas in x])


def Data_to_listOfMeasurement(x: Data) -> list[q.Measurement]:
    return [q.Measurement(val, err) for val, err in zip(x.values, x.errors)]


class PlottingStyle(Protocol):
    """Base class for various plot styles"""

    def add_plot(self, ax) -> None:
        """Adds plot to given axis"""


@dataclass
class DataModel:
    model_function: Callable
    params: Data

    def __call__(self, x) -> Data:
        """Evaluate model function with given parameters"""
        evaulation = self.model_function(x, *self.list_params)
        return evaulation

    @property
    def list_params(self):
        """Return parameters as a list of q.Measurement"""
        return Data_to_listOfMeasurement(self.params)

    def __str__(self):
        args_name = inspect.getfullargspec(self.model_function)[0][1:]

        params_str = ''.join(f"{name} = {param}, " for name,
                             param in zip(args_name, self.params))
        return f"{self.model_function.__name__}(x, args= {params_str})"


@dataclass
class XYPlotData:
    x: Data
    y: Data

    def delete(self, *args):
        indecies = np.flip(np.sort(np.array(args)))
        for index in indecies:
            self.x = self.x.delete(index)
            self.y = self.y.delete(index)

    def __str__(self):
        return f"  X = {self.x}     Y = {self.y}"


@dataclass
class Fit:
    data: XYPlotData
    model: Callable
    guess: Optional[list[float]] = None
    exclude: Optional[list] = None

    def __post_init__(self):
        if self.exclude:
            self.data.delete(*self.exclude)

        self.model_fit_xydata()

    def __call__(self, *args):
        return self.result.__call__(*args)

    def model_fit_xydata(self):
        fit = q.fit(self.data.x, self.data.y, model=self.model,
                    parguess=self.guess)

        self.result = DataModel(
            self.model, listOfMeasurement_to_Data(fit.params))


if __name__ == '__main__':
    def lin(x, a, b):
        return a*x + b

    test = XYPlotData(Data([1, 2, 3], [0.1, 0.1, 0.1]),
                      Data([1, 1.9, 3.1], [0.1, 0.1, 0.1]))

    res_func = Fit(test, lin, guess=[1, 0])
    print(res_func(10))
