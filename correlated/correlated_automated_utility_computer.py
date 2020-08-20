# Designed to compute buyer utility in BOM and seller utility in SOM
# in cases where buyer/seller valuations are fixed by user input and buyer/seller joint densities
# are selected from a given range (also set by user input). Program will iterate through all possible buyer/seller joint
# densities in the given range.

import sys
sys.path.append('../')
from functions import gft_functions
import csv
import time
import itertools
starttime = time.time()

# Set the range of the joint densities to be from 1 to density_range
density_range = 2

# Sorts data by entry in desired column
sort_by = 4

# Sets buyer/seller valuations
buyer_valuation = [1, 2, 3, 4]
seller_valuation = [0, 1, 2, 3]

# Only outputs data with ratio of BOM utility + SOM utility to FB being less than the desired bound
bound_on_ratio = 1.5





n = len(buyer_valuation)
m = len(seller_valuation)

# Initializes list of all possible buyer/seller pairs
valuation_pair = list(itertools.product(buyer_valuation, seller_valuation))
data_list = []

# Iterates through all possible joint densities
for i in range(0, density_range ** (n * m)):
    density = [((i - (i % density_range ** (j - 1))) / (density_range ** (j - 1)) % density_range) + 1 for j in range(1, n * m + 1)]
    joint_density = list(zip(valuation_pair, density))

    # Computes utility
    (BOM_utility, SOM_utility, first_best_gft) = gft_functions.correlated_utility_computer(joint_density, buyer_valuation, seller_valuation)
    row = [density, BOM_utility, SOM_utility, first_best_gft, (BOM_utility+SOM_utility)/first_best_gft]

    # Checks to see if GFT ratio is low enough to be displayed
    if (BOM_utility+SOM_utility)/first_best_gft < bound_on_ratio:
        data_list.append(row)

# Sorts data_list by entry in the desired column
sorted_data_list = sorted(data_list, key=lambda tup: tup[sort_by])

# Writes rows of sorted data list into csv file
with open('/Users/stevenma/PycharmProjects/gainsfromtradeupdated/data/buyer = ' + str(buyer_valuation) + ', seller = '
          + str(seller_valuation) + ', density range = ' + str(density_range) + ', correlated utility.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Valuation pair", valuation_pair])
    writer.writerow(["Joint density", "BOM utility", "SOM utility", "FB GFT", "Ratio of BOM utility + SOM utility to FB"])
    for row in sorted_data_list:
        writer.writerow(row)
csvfile.close()

# Prints how long it took for code to run
print("Code executed in " + str(time.time()-starttime) + " seconds")


