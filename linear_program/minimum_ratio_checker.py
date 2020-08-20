# Determines whether the minimum ratio for (gft_bom+gft_som)/gft_fb is greater than or less than alpha, for an
# inputted value of alpha and inputted value for the size of the buyer/seller supports

from scipy import optimize
import sys
sys.path.append('../')
from functions import linear_program_functions as lp
import time
starttime = time.time()

# In an array, array[s, b] is the element associated with the seller_valuation = s, buyer_valuation = b

# Alpha is the conjectured minimum ratio for (gft_bom+gft_som)/gft_fb
# If result is unbounded, then the min ratio is less than alpha
# If result is zero, then the min ratio is at least as large as alpha
alpha = .8352025


# The buyer and seller supports will range from 0 to n (inclusive)
n = 17

# Method is the method used to solve the linear program
method = 'revised simplex'

# If bounds = (a,b), then all densities will be between a and b
bounds = (.1, None)

# If display_vector = True, then the vector that minimizes the expression will be displayed
display_vector = False




# Gathers coefficients/constraints for linear program
(coefficient_to_minimize, constraints, bound_on_constraints) = lp.minimum_ratio_checker_extreme_case(n=n, alpha=alpha)

print("Time to set up linear program:", time.time()-starttime)

# Executes linear program
result = optimize.linprog(c=coefficient_to_minimize, A_ub=constraints, b_ub=bound_on_constraints, method=method, bounds=bounds)

# Checks whether linear program is unbounded or not
if result["success"] == True:
    print("Result:", "minimum ratio >= ", alpha)
else:
    print("Result:", "minimum ratio <", alpha)
print("message:", result["message"])
print("min value:", result["fun"])
print("pivots:", result["nit"])
if display_vector == True:
    # Prints density that minimizes ratio by row
    density_by_row = [list(result["x"][i:i + n + 1]) for i in range(0, len(result["x"]), n + 1)]
    print("vector minimizing objective function", density_by_row)
print("Total time:", time.time()-starttime)

# Checks if distributions is symmetric
# for i in range(n+1):
#     for j in range(n+1):
#         print(density_by_row[i][j]-density_by_row[n-j][n-i])

