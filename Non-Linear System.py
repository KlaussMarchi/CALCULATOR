import numpy as np
from scipy.optimize import fsolve

def solveSystem(variables):
    (x, y, z, w) = variables
    eq1 = x - y - 9.8
    eq2 = x - 3*z - (3 * 9.8)
    eq3 = 2*x - 2*w - (2*9.8)
    eq4 = w + (0.5)*(y + z)

    return [eq1, eq2, eq3, eq4]

So = np.array([1,1,1,1])        # INICIAL ESTIMATIVE
S = fsolve(solveSystem, So)     # FINAL RESULTS
print('FINAL RESULTS: ', S)