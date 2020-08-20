# Operates in the same way as uncorrelated_automated_gft_computer.py, except the virtual valuations for each distribution will also be computed.
# In addition, for each distinct trade count pair in the cases computed, the GFT for the optimal case (meaning the case
# with the conjectured lower bound for (BOM+SOM)/FB) for that given trade count pair will also be computed.
# If desired, the program can filter out non-regular distributions or also filter out the cases with a GFT
# that is greater than the conjectured optimal case (if conjecture is true, then all non-optimal cases should be gone)

import sys
sys.path.append('../')
from functions import gft_functions
from functions import virtual_valuation_functions
import csv
import time
import operator
starttime = time.time()

# Buyer densities will range from 1 to x
x = 4

# Seller densities will range from 1 to y
y = 4

# Sorts data by entry in the zth column (starting with leftmost element in list)
z = [5, 6, 8]

# Increment to decrease/increase virtual valuation (increment is 1/b)
b = 4

# If regular = true, only regular distributions will be outputted, otherwise all distributions will be outputted
regular = True

# If filtered = true, only distributions with GFT less than the conjectured optimal GFT (lowest ratio) for a given trade count pair will be displayed
filtered = False

# Sets buyer/seller valuations
buyervaluation = [1, 3, 6, 9]
sellervaluation = [0, 4, 5, 7]





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

        # Computes GFT
        data = gft_functions.gftcomputer(sellervaluation, sellerprobability, buyervaluation, buyerprobability)

        # Computes virtual valuation for buyer and seller
        buyer_virtual_valuation = virtual_valuation_functions.virtualvaluationbuyer(buyervaluation, buyerprobability)
        seller_virtual_valuation = virtual_valuation_functions.virtualvaluationseller(sellervaluation, sellerprobability)

        # Adds buyer density, seller density, BOM/FB, SOM/FB, (BOM+SOM)/FB, trade count by buyer type, trade count
        # by seller type, buyer virtual valuation, seller virtual valuation
        row = [buyerprobability, sellerprobability, data[0]/data[2], data[1]/data[2], (data[0]+data[1])/data[2],
               data[3], data[4], buyer_virtual_valuation, seller_virtual_valuation]

        # If regular = True, data will only be added if distributions are regular
        if regular:
            if buyer_virtual_valuation[1] == "regular" and seller_virtual_valuation[1] == "regular":
                datalist.append(row)
        # If regular = False, data will be added regardless of regularity
        else:
            datalist.append(row)

# Sorts datalist by entry in the zth column
sorteddatalist = sorted(datalist, key=operator.itemgetter(*z))





# Initializes list of sorted data, with addition of optimal case (case with conjectured lowest ratio of GFT) for each trade_count_pair
sorted_list_with_optimal_case = []

# Trade_count_pair is the pair (trade count by buyer type, trade count by seller type) for the data in each row of sorteddatalist
# We want to know whenever trade_count_pair changes so we can compute a new "optimal case"
trade_count_pair = []

# Initializes optimal_gft, which is gains from trade for the optimal case (optimal_gft changes every time trade_count_pair changes)
# Value of 0 is unimportant
optimal_gft = 0

for row in sorteddatalist:
    # Checks if the trade_count_pair for the new row is the same as the trade_count_pair for the previous row
    # If trade_count_pair is the same as the previous row, then no new optimal case needs to be computed
    if [row[5], row[6]] == trade_count_pair:
        # If filtered=true, then we filter out cases with GFT greater than or equal to optimal conjectured GFT
        if filtered == False:
            sorted_list_with_optimal_case.append(row)
        elif row[4] < optimal_gft:
            sorted_list_with_optimal_case.append(row)

    # In this case, trade_count_pair for the row is different than the previous row and new optimal case must be computed
    else:
        # Adds empty line whenever trade_count_pair changes
        sorted_list_with_optimal_case.append("")

        # Initializes buyer virtual valuations that corresponds to the conjectured optimal GFT case
        optimal_case_buyer_virtual_valuation_1 = []
        optimal_case_buyer_virtual_valuation_2 = []
        # Computes optimal virtual valuation for elements 0, 1, ... n-2
        for i in range(n-1):
            # For each element i in the buyer virtual valuation in the current row, i is increased to the least element
            # In the seller support that is greater than i. If no element in the seller support is greater than i,
            # Then i is decreased to the value that is 1/b greater than the greatest element in the seller support
            if min(j for j in sellervaluation+[buyervaluation[i]] if j>=row[7][0][i]) == buyervaluation[i]:
                optimal_case_buyer_virtual_valuation_1.append(max(j for j in sellervaluation if j < row[7][0][i]) + 1 / b)
            else:
                optimal_case_buyer_virtual_valuation_1.append(min(j for j in sellervaluation + [buyervaluation[i]] if j >= row[7][0][i]))

            if min(j for j in sellervaluation+[buyervaluation[i]] if j>=row[7][0][i]) == buyervaluation[i]:
                optimal_case_buyer_virtual_valuation_2.append(buyervaluation[i] - 1/b)
            else:
                optimal_case_buyer_virtual_valuation_2.append(min(j for j in sellervaluation + [buyervaluation[i]] if j >= row[7][0][i]))

        # Adds on virtual valuation for element n-1
        optimal_case_buyer_virtual_valuation_1.append(buyervaluation[n - 1])
        optimal_case_buyer_virtual_valuation_2.append(buyervaluation[n - 1])

        # Initializes seller virtual valuation that corresponds to the first conjectured optimal GFT case
        optimal_case_seller_virtual_valuation_1 = []
        optimal_case_seller_virtual_valuation_2 = []
        # Computes virtual valuation for elements 1, 2, 3, ... n-1
        for i in range(1, m):
            # For each element i in the seller virtual valuation in the current row, i is decreased to the greatest element
            # in the buyer support that is less than i. If no element in the buyer support is less than i, then i
            # is increased to the value that is 1/b less than the least element in the buyer support
            if max(j for j in buyervaluation+[sellervaluation[i]] if j<=row[8][0][i]) == sellervaluation[i]:
                optimal_case_seller_virtual_valuation_1.append(min(j for j in buyervaluation if j > row[8][0][i]) - 1 / b)
            else:
                optimal_case_seller_virtual_valuation_1.append(max(j for j in buyervaluation + [sellervaluation[i]] if j <= row[8][0][i]))

            if max(j for j in buyervaluation+[sellervaluation[i]] if j<=row[8][0][i]) == sellervaluation[i]:
                optimal_case_seller_virtual_valuation_2.append(sellervaluation[i] + 1/b)
            else:
                optimal_case_seller_virtual_valuation_2.append(max(j for j in buyervaluation + [sellervaluation[i]] if j <= row[8][0][i]))

        # Adds on virtual valuation for element 0
        optimal_case_seller_virtual_valuation_1.insert(0, sellervaluation[0])
        optimal_case_seller_virtual_valuation_2.insert(0, sellervaluation[0])

        # Computes GFT for the first pair of virtual valuations that is conjectured to optimize (minimize) GFT ratio
        optimal_case_1 = gft_functions.gft_computer_virtual_valuation(sellervaluation, optimal_case_seller_virtual_valuation_1,
                                                                      buyervaluation, optimal_case_buyer_virtual_valuation_1, b * b)

        # Computes GFT for the second pair of virtual valuations that is conjectured to optimize (minimize) GFT ratio
        optimal_case_2 = gft_functions.gft_computer_virtual_valuation(sellervaluation,
                                                                      optimal_case_seller_virtual_valuation_2,
                                                                      buyervaluation,
                                                                      optimal_case_buyer_virtual_valuation_2, b * b)

        # Computes GFT for the second pair of virtual valuations that is conjectured to optimize (minimize) GFT ratio
        optimal_case_3 = gft_functions.gft_computer_virtual_valuation(sellervaluation,
                                                                      optimal_case_seller_virtual_valuation_1,
                                                                      buyervaluation,
                                                                      optimal_case_buyer_virtual_valuation_2, b * b)

        # Computes GFT for the second pair of virtual valuations that is conjectured to optimize (minimize) GFT ratio
        optimal_case_4 = gft_functions.gft_computer_virtual_valuation(sellervaluation,
                                                                      optimal_case_seller_virtual_valuation_2,
                                                                      buyervaluation,
                                                                      optimal_case_buyer_virtual_valuation_1, b * b)


        optimal_gft_list = [optimal_case_1[4], optimal_case_2[4], optimal_case_3[4], optimal_case_4[4]]
        optimal_index = optimal_gft_list.index(min(optimal_gft_list)) + 1


        # Appends optimal case and takes ratio of GFT from optimal case
        sorted_list_with_optimal_case.append(["Optimal Case"])
        sorted_list_with_optimal_case.append(eval('optimal_case_' + str(optimal_index)))
        optimal_gft = eval('optimal_case_' + str(optimal_index))[4]

        # Filters out distributions with GFT higher than the optimal case if filtered = True
        if filtered == False:
            sorted_list_with_optimal_case.append(row)
        elif row[4] < optimal_gft:
            sorted_list_with_optimal_case.append(row)

        # Updates trade_count_pair so that future rows can be checked if trade_count_pair differs
        trade_count_pair = [row[5], row[6]]





# Writes rows of sorted data list into csv file
with open('/Users/stevenma/PycharmProjects/gainsfromtradeupdated/data/n='+str(n)+', m='+str(m)+', x='+str(x)+', y='+str(y)+', b='+str(b)+' with valuations.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Buyer support:",buyervaluation, "Seller support:", sellervaluation])
    writer.writerow(["Buyer densities", "Seller densities", "Ratio of BOM to FB", "Ratio of SOM to FB",
                     "Ratio of BOM + SOM to FB","Trade count by buyer type in BOM", "Trade count by seller type in SOM",
                     "Buyer virtual valuation", "Seller virtual valuation"+"\n"])
    for row in sorted_list_with_optimal_case:
        writer.writerow(row)
csvfile.close()

# Prints how long it took for code to run
print("Code executed in " + str(time.time()-starttime) + " seconds")