# Designed to buyer/seller utility in BOM/SOM in cases where buyer/seller valuations are fixed by user input and buyer/seller densities
# are selected from a given range (also set by user input). Program will iterate through all possible buyer/seller
# densities in the given range.

import sys
sys.path.append('../')
from functions import gft_functions
import csv
import time
starttime = time.time()

# Buyer densities will range from 1 to x
x = 4

# Seller densities will range from 1 to y
y = 4

# Sorts data by entry in the zth column
z = 5

# How many rows to output
c = 100

# Sets buyer/seller valuations
buyervaluation = [1, 2, 3, 4]
sellervaluation = [0, 1, 2, 3]





# Ensures values in buyer support are increasing
if (all(x < y for x, y in zip(buyervaluation, buyervaluation[1:])) == False):
    print("Buyer support not increasing")
    exit()

# Ensures values in seller support are increasing
if (all(x < y for x, y in zip(sellervaluation, sellervaluation[1:])) == False):
    print("Seller support not increasing")
    exit()

print("Buyer support:", buyervaluation, "Seller support:", sellervaluation)

n = len(buyervaluation)
m = len(sellervaluation)

# Initializes list of unsorted data
datalist = []

# Iterates density of each value in buyer support from 1 to x
for i in range (0, x**n):
    buyerprobability = [((i - (i % x**(j-1)))/(x**(j-1)) % x)+1 for j in range(1, n+1)]

    # Iterates density of each value in seller support from 1 to y
    for k in range(0, y**m):
        sellerprobability = [((k - (k % y**(l-1)))/(y**(l-1)) % y)+1 for l in range(1, m+1)]

        # Computes utilities and adds to datalist
        data = gft_functions.utility_computer(sellervaluation, sellerprobability, buyervaluation, buyerprobability)
        row = [buyerprobability, sellerprobability, data[0], data[1], data[2], (data[0]+data[1])/data[2], data[3], data[4]]
        datalist.append(row)

# Sorts datalist by entry in the zth column
sorteddatalist = sorted(datalist, key=lambda tup: tup[z])

# Writes rows of sorted data list into csv file
with open('/Users/stevenma/PycharmProjects/gainsfromtradeupdated/data/n='+str(n)+', m='+str(m)+', x='+str(x)+', y='+str(y)+' with utility.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Buyer support:", buyervaluation, "Seller support:", sellervaluation])
    for i in range(0, c):
        writer.writerow(sorteddatalist[i])
csvfile.close()

# Prints how long it took for code to run
print("Code executed in " + str(time.time()-starttime) + " seconds")