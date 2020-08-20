# Computes GFT in case where user manually inputs buyer/seller supports and densities.

import sys
sys.path.append('../')
from functions import gft_functions
from functions import virtual_valuation_functions

buyersupport = [3, 10, 13, 14]
buyerdensity = [3, 1, 1, 1]
sellersupport = [1, 2, 5, 12]
sellerdensity = [2, 1, 1, 5]





# Ensures buyer support/density have same length
if(len(buyersupport) != len(buyerdensity)):
    print("Buyer support and buyer density have different lengths")
    exit()

# Ensures seller support/density have same length
if(len(sellersupport) != len(sellerdensity)):
    print("Seller support and seller density have different lengths")
    exit()

# Ensures values in buyer support are increasing
if (all(x < y for x, y in zip(buyersupport, buyersupport[1:])) == False):
    print("Buyer support not increasing")
    exit()

# Ensures values in seller support are increasing
if (all(x < y for x, y in zip(sellersupport, sellersupport[1:])) == False):
    print("Seller support not increasing")
    exit()

# Calculates and prints GFT
data = gft_functions.gftcomputer(sellersupport, sellerdensity, buyersupport, buyerdensity)
print("Buyer offering GFT:", data[0])
print("Seller offering GFT:", data[1])
print("Optimal GFT:", data[2])
print("Ratio:", (data[0]+data[1])/data[2])
print("Trade count by buyer type in BOM:", data[3])
print("Trade count by seller type in SOM", data[4])
print("Buyer virtual valuation", virtual_valuation_functions.virtualvaluationbuyer(buyersupport, buyerdensity)[0])
print("Seller virtual valuation", virtual_valuation_functions.virtualvaluationseller(sellersupport, sellerdensity)[0])