import qexpy as q
import numpy as np


class Data(q.MeasurementArray):

    def set_un(self, unit):
        self.un = unit

    def add_Data(self, MeasurementArrays):
        data = self.values
        err = self.errors
        for measArr in MeasurementArrays:
            data = np.append(data, measArr.values)
            err = np.append(err, measArr.errors)
        return Data(data, err)

    def avg(self):
        sum_of_squares = sum([error**2 for error in self.errors])
        return q.Measurement(self.mean().value, np.sqrt(sum_of_squares) / len(self.errors))
