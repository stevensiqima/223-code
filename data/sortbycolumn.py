import csv
import operator

# Name of file that is to be sorted
filename = 'buyer = 50, seller = 50, randomized with utility.csv'

# Opens file to be sorted
datafile = csv.reader(open(filename))

# Sorts data by entries in the kth column
z = 3
data = min(datafile, key=operator.itemgetter(z))

# Writes sorted data into a new csv file
# with open('z=' + str(z) + ", " + filename, 'a') as csvfile:
#     writer = csv.writer(csvfile)
#     for row in sortedfile:
#         writer.writerow(row)
# csvfile.close()

data[4] = data[4][1:-1]
data[5] = data[5][1:-1]

buyer_density = [round(float(x)*10**15) for x in data[4].split(",")]
seller_density = [round(float(x)*10**15) for x in data[5].split(",")]

# y is the size of the buyer/seller supports
y = 50

# Sets buyer/seller valuations
buyervaluation = list(range(1, y+1))
sellervaluation = list(range(0, y))

print(functions.gftfunctions.utility_computer(sellervaluation, seller_density, buyervaluation, buyer_density))

