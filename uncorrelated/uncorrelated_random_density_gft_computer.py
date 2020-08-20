import sys
sys.path.append('../')
from functions import gft_functions
import csv
import time
import itertools
import random
starttime = time.time()

# y is the size of the buyer/seller supports
y = 100

# x is the range of the buyer/seller densities
x = 10

# Sets buyer/seller valuations
buyervaluation = list(range(1, y+1))
sellervaluation = list(range(0, y))

n = len(buyervaluation)
m = len(sellervaluation)






# Writes rows of sorted data list into csv file
with open('/Users/stevenma/PycharmProjects/gainsfromtradeupdated/data/buyer = '+str(len(buyervaluation))+', seller = '+str(len(sellervaluation))+', gft.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    while True:


        i = random.randint(1, x**n)
        k = random.randint(1, x**n)

        buyer_density = [((i - (i % x**(j-1)))/(x**(j-1)) % x)+1 for j in range(1, y+1)]
        seller_density = [((k - (k % x**(j-1)))/(x**(j-1)) % x)+1 for j in range(1, y+1)]

        data = gft_functions.gftcomputer(sellervaluation, seller_density, buyervaluation, buyer_density)

        if ((data[0] + data[1]) / data[2]<=1.3):
            row = [data[0], data[1], data[2], (data[0]+data[1])/data[2], buyer_density, seller_density]
            print("hello", (data[0]+data[1])/data[2])
        else:
            row = [data[0], data[1], data[2], (data[0] + data[1]) / data[2]]

        writer.writerow(row)

csvfile.close()

