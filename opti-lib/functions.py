from itertools import product

import sys, os
sys.path.append(os.getcwd())

from mip import Model, xsum, BINARY, INTEGER, minimize

from utils import *


class ShaftPlanning:
    def __init__(self, n, d, sloc, dloc, fc, htc, vtc, level):
        self.total = n
        self.sloc = sloc
        self.dist = d
        self.dloc = dloc
        self.scost = fc
        self.level = level
        self.horizontal_transport = htc
        self.vertical_transport = vtc
        self.validate(n, d)

    def validate(self, n, d):
        ch = True
        if len(self.dloc) != d:
            ch = False
            raise ValueError("Number of districts not equals the list of locations given.")

        if len(self.sloc) != n:
            ch = False
            raise ValueError("Number of Shafts not equals the list of locations given")

        for i in self.dloc:
            if len(i) != 3 or i[2]>self.level:
                ch = False
                raise ValueError("{} is not a proper district location".format(i))

        for i in self.sloc:
            if len(i) != 2:
                ch = False
                raise ValueError("{} is not a proper shaft location".format(i))

        if self.scost == 0:
            raise ValueError("Shaft Construction Cost per level can't be Zero")

        if self.horizontal_transport == 0 or self.vertical_transport == 0:
            raise ValueError("Transportation cost must be greater than Zero")

    def predict(self):
        model = Model("Shaft Planning")
        # Decision Variables
        s = [model.add_var(var_type=INTEGER, lb=0, ub=self.level) for i in range(self.total)]
        y = [[model.add_var(var_type=BINARY) for j in range(self.total)] for i in range(self.dist)]
        # Model Objective
        fc = self.scost
        total_fixed_cost = xsum(s[i]*fc for i in range(self.total))

        total_transportation_cost = xsum(y[i][j] * (compute_distance(self.dloc[i], self.sloc[j]) * self.horizontal_transport +
                                                    self.vertical_transport * self.dloc[i][2])
                                         for i in range(self.dist) for j in range(self.total))
        model.objective = minimize(total_fixed_cost + total_transportation_cost)

        # Model Constraints

        for i in range(self.dist):
            model += xsum(y[i][j] for j in range(self.total)) == 1

        for j in range(self.total):
            for i in range(self.dist):
                model += y[i][j] <= s[j]/self.dloc[i][2]
