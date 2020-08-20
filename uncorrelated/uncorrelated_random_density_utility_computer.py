import sys
sys.path.append('../')
from functions import gft_functions, virtual_valuation_functions
import csv
import time
import itertools
import random
starttime = time.time()


# y is the size of the buyer/seller supports
y = 100

# x is the range of buyer/seller supports
x = 20

# Sets buyer/seller valuations
buyervaluation = list(range(1, y+1))
sellervaluation = list(range(0, y))

n = len(buyervaluation)
m = len(sellervaluation)




# Writes rows of sorted data list into csv file
with open('/Users/stevenma/PycharmProjects/gainsfromtradeupdated/data/buyer = '+str(len(buyervaluation))+', seller = '+str(len(sellervaluation))+', randomized with utility.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    while True:
        buyer_virtual_valuation = [sellervaluation[random.randint(0,x)] for x in range(n)]
        buyer_virtual_valuation = sorted(buyer_virtual_valuation)
        buyer_density = virtual_valuation_functions.virtualvaluationbuyerinverse(buyervaluation, buyer_virtual_valuation, 1)

        seller_density = buyer_density[::-1]


        data = gft_functions.utility_computer(sellervaluation, seller_density, buyervaluation, buyer_density)

        if ((data[0] + data[1]) / data[2]<=.86):
            row = [data[0], data[1], data[2], (data[0]+data[1])/data[2], buyer_density, seller_density]
            print("hello", (data[0]+data[1])/data[2])

        else:
            row = [data[0], data[1], data[2], (data[0] + data[1]) / data[2]]

        writer.writerow(row)



csvfile.close()

