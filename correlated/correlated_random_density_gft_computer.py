# Designed to compute GFT in cases where buyer/seller valuations are fixed by user input and buyer/seller joint densities
# are selected from a given range (also set by user input). Program will repeatedly randomly pick possible buyer/seller joint
# densities in the given range and compute the GFT until manually stopped

import sys
sys.path.append('../')
from functions import gft_functions
import csv
import time
import itertools
import random
starttime = time.time()

# Set the size of the buyer/seller support
support_size = 10

# Set the range of the joint densities to be from 1 to density_range
density_range = 12

# Only outputs data with ratio of BOM + SOM to FB being less than k
bound_on_ratio = 1.5






# Sets buyer/seller valuations
buyer_valuation = list(range(1, support_size + 1))
seller_valuation = list(range(0, support_size))

n = len(buyer_valuation)
m = len(seller_valuation)

# Initializes list of all possible buyer/seller pairs
valuation_pair = list(itertools.product(buyer_valuation, seller_valuation))

# Writes rows of sorted data list into csv file
with open('/Users/stevenma/PycharmProjects/gainsfromtradeupdated/data/buyer and seller support size = ' + str(n) + ', random density, correlated gft.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["BOM GFT", "SOM GFT", "FB GFT", "Ratio of BOM + SOM to FB", "Joint density"])
    while True:
        # Picks random density in range of all possible densities
        i = random.randint(1, density_range ** (n * m))
        density = [((i - (i % density_range ** (j - 1))) / (density_range ** (j - 1)) % density_range) + 1 for j in range(1, n * m + 1)]
        joint_density = list(zip(valuation_pair, density))

        # Computes GFT
        (BOM_gft, SOM_gft, first_best_gft, BOM_trade_count_by_buyer_type, SOM_trade_count_by_seller_type,
         BOM_buyer_revenue_list, SOM_seller_revenue_list) = gft_functions.correlated_gft_computer(joint_density, buyer_valuation, seller_valuation)

        # Checks to see if GFT ratio is low enough to be outputted
        if (BOM_gft + SOM_gft) / first_best_gft < bound_on_ratio:
            row = [BOM_gft, SOM_gft, first_best_gft, (BOM_gft + SOM_gft) / first_best_gft, density]
            writer.writerow(row)

csvfile.close()

