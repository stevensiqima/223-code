# Designed to compute ratio of utilities to FB in cases where buyer valuation is inputted by user, ane seller valuation is set to be
# the symmetric version of the buyer valuation. Buyer/seller densities are also symmetric, with buyer/seller densities
# iterated through all possible densities in a given range (inputted by user). Able to run faster than uncorrelated_automated_utility_computer.py

import sys
sys.path.append('../')
import csv
import time
from functions import gft_functions

starttime = time.time()

# Buyer/seller densities will range from 1 to x
x = 25

# Sets values in buyer support
buyervaluation = [1, 2, 3, 4]

# Shifts seller values down by k
k = 1

# Sorts data by entry in zth column
z = 1







# Makes seller support symmetric to buyer support
n = len(buyervaluation)
sellervaluation = [buyervaluation[n-1]+buyervaluation[0]-buyervaluation[n-1-x]-k for x in range(0, n)]

print("Buyer support:", buyervaluation, "Seller support:", sellervaluation)

# Initializes list of unsorted data
datalist = []

# Iterates density of each value in buyer/seller support from 1 to x
for i in range(0, x**n):
    buyerprobability = [((i - (i % x ** (j - 1))) / (x ** (j - 1)) % x) + 1 for j in range(1, n + 1)]

    # Ensures seller densities are symmetric to buyer densities
    sellerprobability = buyerprobability[::-1]

    # Computes utility ratio and adds to datalist
    data = gft_functions.utility_computer_symmetric(sellervaluation, sellerprobability, buyervaluation, buyerprobability)
    row = [buyerprobability, 2*data[0]/data[1], data[2]]
    datalist.append(row)

# Sorts datalist by entry in the zth column
sorteddatalist = sorted(datalist, key=lambda tup: tup[z])

# Writes rows of sorted data list into csv file
with open('/Users/stevenma/PycharmProjects/gainsfromtradeupdated/data/symmetric n='+str(n)+', x='+str(x)+' with utility.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Buyer distributions and seller distributions are symmetric"])
    writer.writerow(["Buyer support:",buyervaluation, "Seller support:", sellervaluation])
    writer.writerow(["Buyer densities", "Ratio of BOM buyer utility + SOM seller utility to FB"+"\n"])
    for row in sorteddatalist:
        writer.writerow(row)
csvfile.close()


# Prints how long it took for code to run
print("Code executed in " + str(time.time()-starttime) + " seconds")
