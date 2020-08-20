# Graphs minimum ratio (gftbom+gftsom)/gftfb (rounded down to nearest multiple of y) for various support sizes
# Support of buyer/seller assumed to both be 0, 1, 2, 3, ... n

from scipy import optimize
import sys
sys.path.append('../')
from functions import linear_program_functions as lp
import matplotlib.pyplot as plt
import math

# Ratio is rounded down to the nearest multiple of precision
precision = 0.01

# Upper_bound is the large support size that the program will compute, lower_bound is the smallest support size computed
lower_bound = 2
upper_bound = 20

# Method is the method used to solve the linear program
method = 'interior-point'

# If bounds = (a,b), then all densities will be between a and b
bounds = (0, None)

# Alpha is the starting value of alpha (which will be decreased as the support size increases)
alpha = 1.5





# Iterates through support size = 2 to support size = upper_bound
for n in range(lower_bound, upper_bound+1):
    while True:
        # Gathers coefficients/constraints for linear program
        (coefficient_to_minimize, constraints, bound_on_constraints) = lp.minimum_ratio_checker_extreme_case(n=n,
                                                                                                             alpha=alpha)
        # Solves the linear program
        result = optimize.linprog(c=coefficient_to_minimize, A_ub=constraints, b_ub=bound_on_constraints, method=method,
                                  bounds=bounds)

        # If minimum value of linear program is not unbounded, then value of alpha is recorded, so that alpha
        # is the minimum ratio of (gftbom+gftsom)/gftfb rounded down to the nearest multiple of y
        # If minimum value of linear program is unbounded, then alpha is decreased and the linear program is run again
        if result["success"] == True:
            plt.scatter(n, alpha, color="blue")
            print(n)
            break
        alpha = alpha - precision

plt.xlabel("Support size")
plt.ylabel("Minimum ratio of (BOM + SOM)/FB")
plt.title("Minimum ratio of (BOM + SOM)/FB vs. Support size")
plt.suptitle("Precision = " + str(precision))
plt.savefig('/Users/stevenma/PycharmProjects/gainsfromtradeupdated/data/ratio vs. support size, support range = '
            +str([lower_bound, upper_bound])+'.png')
