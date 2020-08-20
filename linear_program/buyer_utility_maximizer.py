from scipy import optimize
import sys
sys.path.append('../')
from functions import linear_program_functions as lp
import numpy as np
from functions import gft_functions
import itertools



# Sets buyer/seller support size (ranges from 0 to buyer_support_size)
support_size = 16


joint_density = gft_functions.bom_som_minimum_ratio_density(support_size)

for i in joint_density:
    print(list(i))

exit()





density_for_trade_function = []
for i in joint_density:
    density_for_trade_function.append(list(i))

density_for_trade_function = sum(density_for_trade_function, [])
buyer_valuation = list(range(0, support_size + 1))
seller_valuation = list(range(0, support_size + 1))
valuation_pair = list(itertools.product(seller_valuation, buyer_valuation))
density_for_trade_function = list(zip(valuation_pair, density_for_trade_function))

print(density_for_trade_function)

(BOM_gft, SOM_gft, first_best_gft, BOM_trade_count_by_buyer_type, SOM_trade_count_by_seller_type, BOM_buyer_revenue_list,
 SOM_seller_revenue_list) = gft_functions.correlated_gft_computer(density_for_trade_function, buyer_valuation, seller_valuation)

print("BOM GFT:", BOM_gft)
print("SOM GFT:", SOM_gft)
print("FB GFT:", first_best_gft)
print("Ratio of BOM + SOM to FB:", (BOM_gft+SOM_gft)/first_best_gft)