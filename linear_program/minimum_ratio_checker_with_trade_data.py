# Determines whether the minimum ratio for (gft_bom+gft_som)/gft_fb is greater than or less than alpha, for an
# inputted value of alpha and inputted value for the size of the buyer/seller supports
# Also outputs gft data associated with the density that corresponds to the minimum value of the objective function

from scipy import optimize
import itertools
import sys
sys.path.append('../')
from functions import gft_functions
from functions import linear_program_functions as lp

# Alpha is the conjectured minimum ratio for (gft_bom+gft_som)/gft_fb
# If result is unbounded, then the min ratio is less than alpha
# If result is zero, then the min ratio is at least as large as alpha
alpha = .847243

# The buyer and seller supports will range from 0 to n (inclusive)
n = 16

# Method is the method used to solve the linear program
method = 'revised simplex'

# If bounds = (a,b), then all densities will be between a and b
bounds = (1, None)





# Gathers coefficients/constraints for linear program
(coefficient_to_minimize, constraints, bound_on_constraints) = lp.minimum_ratio_checker_extreme_case(n=n, alpha=alpha)

# Executes linear program
result = optimize.linprog(c=coefficient_to_minimize, A_ub=constraints, b_ub=bound_on_constraints, method=method,
                          bounds=bounds)

# Obtains density corresponding to the minimum value of the objective function
density = result["x"]

# Normalizes density
density = [x/density[n]/n for x in density]

# Checks whether linear program is unbounded or not
if result["success"] == True:
    print("Result:", "minimum ratio >= ", alpha)
else:
    print("Result:", "minimum ratio <", alpha)
print("message:", result["message"])

# Initializes buyer/seller supports to be 0, 1, 2, 3, ... n
buyer_valuation = list(range(0, n + 1))
seller_valuation = list(range(0, n + 1))
valuation_pair = list(itertools.product(seller_valuation, buyer_valuation))

# Flips all elements in valuation_pair from (buyer, seller) to (seller, buyer)
for i in range(len(valuation_pair)):
    valuation_pair[i] = valuation_pair[i][::-1]
joint_density = list(zip(valuation_pair, density))

# Computes GFT data associated with density corresponding to minimum value of objective function
(BOM_gft, SOM_gft, first_best_gft, BOM_trade_count_by_buyer_type, SOM_trade_count_by_seller_type, BOM_buyer_revenue_list,
 SOM_seller_revenue_list) = gft_functions.correlated_gft_computer(joint_density, buyer_valuation, seller_valuation)

print("BOM GFT:", BOM_gft)
print("SOM GFT:", SOM_gft)
print("FB GFT:", first_best_gft)
print("Ratio of BOM + SOM to FB:", (BOM_gft+SOM_gft)/first_best_gft)


print("BOM trade count by buyer type:", BOM_trade_count_by_buyer_type)
print("SOM trade count by seller type:", SOM_trade_count_by_seller_type)
print("BOM revenue list by buyer type:", BOM_buyer_revenue_list)
print("SOM revenue list by seller type", SOM_seller_revenue_list)

# Splits density into seperate rows (one for each seller type)
density_by_row = [list(density[i:i + n + 1]) for i in range(0, len(density), n + 1)]

density_by_row[6][14]=1/15/8/9
density_by_row[6][9]=1/132
density_by_row[7][14]=1/15/7/8
density_by_row[7][9]=1/48.0234737

# Prints the reciprocal of each density (rounded to 5 decimal places)
for i in range(len(density_by_row)):
    print(i, [round(1/x, 5)for x in density_by_row[i]])


# counter = 0
# # Checks if distributions is symmetric
# for i in range(n+1):
#     for j in range(n+1):
#         print(1/density_by_row[i][j]-1/density_by_row[n-j][n-i])
#         print(counter)
#         counter = counter + 1

# density = sum(density_by_row,[])
# joint_density = list(zip(valuation_pair, density))
# (BOM_gft, SOM_gft, first_best_gft, BOM_trade_count_by_buyer_type, SOM_trade_count_by_seller_type, BOM_buyer_revenue_list,
#  SOM_seller_revenue_list) = gft_functions.correlated_gft_computer(joint_density, buyer_valuation, seller_valuation)
#
# print("BOM GFT:", BOM_gft)
# print("SOM GFT:", SOM_gft)
# print("FB GFT:", first_best_gft)
# print("Ratio of BOM + SOM to FB:", (BOM_gft+SOM_gft)/first_best_gft)