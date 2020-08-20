# Contains lp_functions related to computing gains from trade

from functions import virtual_valuation_functions
import numpy as np


# Error_tolerance should be a number a little more than 1 (or 1 if we want no error tolerance) so that the lowest price is offered in BOM
# (and highest price is offered in SOM) as long as the revenue obtained by posting the lowest price in BOM multiplied
# by error_tolerance is at least the revenue obtained by posting any other price

error_tolerance = 1.000000001

# Calculates gains from trade of BOM where seller has multiple valuations and buyer has one valuation
# Sellervalues/sellerdensities should be list of floats, buyervalue should be one float
def individualBOM(sellervalues, sellerdensities, buyervalue):

    m = len(sellervalues)

    # Probability is the chance that trade happens from setting trade price at sellervalues[i]
    probability = [sum(sellerdensities[0:x+1]) for x in range(m)]

    # Buyerrevenue[i] is the expected revenue to the buyer for setting price at sellervalues[i]
    buyerrevenue = [(buyervalue - sellervalues[x])*probability[x] for x in range(m)]

    # Computes bestprice so that sellervalues[bestprice] is the profit maximizing price for buyer
    bestprice = 0
    for i in range(1, m):
        if(buyerrevenue[i] > buyerrevenue[bestprice]*error_tolerance):
            bestprice = i

    # Computes gains from trade
    # Ensures engaging in trade is rational for buyer
    if(buyerrevenue[bestprice] < 0):
        gft = 0
    else:
        gft = sum([(buyervalue - sellervalues[x])*sellerdensities[x] for x in range(bestprice+1)])

    # Bestprice + 1 is the number of seller types that will engage in trade
    return(gft, bestprice + 1)

# Calculates gains from trade of SOM where buyer has multiple valuations and seller has one valuation
# Buyervalues/buyerdensities should be list of floats, sellervalue should be one float
def individualSOM(buyervalues, buyerdensities, sellervalue):

    n = len(buyervalues)

    # Probability is the chance that trade happens from setting trade price at buyervalues[i]
    probability = [sum(buyerdensities[x:]) for x in range(n)]

    # Sellerrevenue[i] is the expected revenue to the seller for setting price at buyervalues[i]
    sellerrevenue = [(buyervalues[x]-sellervalue)*probability[x] for x in range(n)]

    # Computes bestprice so that buyervalues[bestprice] is the profit maximizing price for seller
    bestprice = 0
    for i in range (1, n):
        if(sellerrevenue[i]*error_tolerance >= sellerrevenue[bestprice]):
            bestprice = i

    # Computes gains from trade
    # Ensures that engaging in trade is rational for seller
    if(sellerrevenue[bestprice] < 0):
        gft = 0
    else:
        gft = sum([(buyervalues[x] - sellervalue)*buyerdensities[x] for x in range(bestprice, n)])

    # n - bestprice is the number of buyer types that will engage in trade
    return(gft, n - bestprice)

# Computes BOM, SOM, FB GFT
def gftcomputer(sellersupport, sellerdensity, buyersupport, buyerdensity):

    m = len(sellersupport)
    n = len(buyersupport)

    # Computes GFT from BOM
    gftbom = sum([individualBOM(sellersupport, sellerdensity, buyersupport[x])[0]*buyerdensity[x] for x in range(n)])

    # Tradecount_by_buyertype[i] is the number of seller types engaging in trade with buyersupport[i] in BOM
    tradecount_by_buyertype = [individualBOM(sellersupport, sellerdensity, buyersupport[x])[1] for x in range(n)]

    # Computes GFT from SOM
    gftsom = sum([individualSOM(buyersupport, buyerdensity, sellersupport[x])[0]*sellerdensity[x] for x in range(m)])

    # Tradecount_by_sellertype[i] is the number of buyer types engaging in trade with sellersupport[i] in SOM
    tradecount_by_sellertype = [individualSOM(buyersupport, buyerdensity, sellersupport[x])[1] for x in range(m)]

    # Computes optimal (first best) GFT
    gftfb = 0
    # Loops through buyer valuations
    for i in range(0, n):
        # Loops through seller valuations
        for j in range (0, m):
            # Adds term to gftfb if buyer valuation exceeds seller valuation
            if(sellersupport[j] < buyersupport[i]):
                gftfb = gftfb + (buyersupport[i] - sellersupport[j])*(buyerdensity[i])*(sellerdensity[j])

    return(gftbom, gftsom, gftfb, tradecount_by_buyertype, tradecount_by_sellertype)

# Computes BOM, SOM, FB GFT if buyer and seller distributions are symmetric (faster than gftcomputer)
def gftcomputersymmetric(sellersupport, sellerdensity, buyersupport, buyerdensity):

    n = len(buyersupport)

    # Computes GFT from BOM
    gftbom = sum([individualBOM(sellersupport, sellerdensity, buyersupport[x])[0] * buyerdensity[x] for x in range(n)])

    # Tradecount_by_buyertype[i] is the number of seller types engaging in trade with buyersupport[i] in BOM
    tradecount_by_buyertype = [individualBOM(sellersupport, sellerdensity, buyersupport[x])[1] for x in range(n)]

    # Computes optimal (first best) GFT
    gftfb = 0
    # Loops through buyer valuations
    for i in range(0, n):
        # Loops through seller valuations
        for j in range(0, n):
            # Adds term to gftfb if buyer valuation exceeds seller valuation
            if (sellersupport[j] < buyersupport[i]):
                gftfb = gftfb + (buyersupport[i] - sellersupport[j]) * (buyerdensity[i]) * (sellerdensity[j])

    return(gftbom, gftfb, tradecount_by_buyertype)

# Computes BOM, SOM, FB GFT given seller/buyer distributions and virtual valuations
# Common multiple should be inputted so that seller and buyer densities are all approximately integers before any rounding
# Common multiple should typically be a value so that every element in both virtual valuations is an integer after being multiplied by common multiple
def gft_computer_virtual_valuation(seller_support, seller_virtual_valuation, buyer_support, buyer_virtual_valuation, common_multiple):

    # Computes buyer density that produces desired virtual valuation (all elements in buyer_density are rounded to be integers)
    buyer_density = [round(x) for x in virtual_valuation_functions.virtualvaluationbuyerinverse(buyer_support, buyer_virtual_valuation, common_multiple)]

    # Computes seller density that produces desired virtual valuation (all elements in seller_density are rounded to be integers)
    seller_density = [round(x) for x in virtual_valuation_functions.virtualvaluationsellerinverse(seller_support, seller_virtual_valuation, common_multiple)]

    # Computes gains from trade
    data = gftcomputer(seller_support, seller_density, buyer_support, buyer_density)

    # New virtual valuations should be same as originals, otherwise some rounding error occurred
    new_buyer_virtual_valuation = virtual_valuation_functions.virtualvaluationbuyer(buyer_support, buyer_density)[0]
    new_seller_virtual_valuation = virtual_valuation_functions.virtualvaluationseller(seller_support, seller_density)[0]

    # Returns ((0) buyer density, (1) seller density, (2) ratio of BOM to FB, (3) ratio of SOM to FB, (4) ratio of (BOM+SOM)/FB,
    # (5) trade count by buyer type, (6) trade count by seller type, (7) updated buyer virtual valuation, (8) updated seller virtual valuation)
    return(buyer_density, seller_density, data[0]/data[2], data[1]/data[2], (data[0]+data[1])/data[2], data[3], data[4], new_buyer_virtual_valuation, new_seller_virtual_valuation)

# Calculates buyer utility in BOM where seller has multiple valuations and buyer has one valuation
# Sellervalues/sellerdensities should be list of floats, buyervalue should be one float
def individual_BOM_utility(sellervalues, sellerdensities, buyervalue):

    m = len(sellervalues)

    # Probability is the chance that trade happens from setting trade price at sellervalues[i]
    probability = [sum(sellerdensities[0:x+1]) for x in range(m)]

    # Buyerrevenue[i] is the expected revenue to the buyer for setting price at sellervalues[i]
    buyerrevenue = [(buyervalue - sellervalues[x])*probability[x] for x in range(m)]

    # Computes bestprice so that sellervalues[bestprice] is the profit maximizing price for buyer
    bestprice = 0
    for i in range(1, m):
        if(buyerrevenue[i] > buyerrevenue[bestprice]*error_tolerance):
            bestprice = i

    # Returns (buyer utility, # of seller types that will engage in trade)
    # Ensures engaging in trade is rational for buyer
    if(buyerrevenue[bestprice] < 0):
        return(0, bestprice + 1)
    else:
        return(buyerrevenue[bestprice], bestprice + 1)


# Calculates seller utility in SOM where buyer has multiple valuations and seller has one valuation
# Buyervalues/buyerdensities should be list of floats, sellervalue should be one float
def individual_SOM_utility(buyervalues, buyerdensities, sellervalue):

    n = len(buyervalues)

    # Probability is the chance that trade happens from setting trade price at buyervalues[i]
    probability = [sum(buyerdensities[x:]) for x in range(n)]

    # Sellerrevenue[i] is the expected revenue to the seller for setting price at buyervalues[i]
    sellerrevenue = [(buyervalues[x]-sellervalue)*probability[x] for x in range(n)]

    # Computes bestprice so that buyervalues[bestprice] is the profit maximizing price for seller
    bestprice = 0
    for i in range (1, n):
        if(sellerrevenue[i]*error_tolerance >= sellerrevenue[bestprice]):
            bestprice = i

    # Returns (seller utility, # of buyer types that will engage in trade)
    # Ensures that engaging in trade is rational for seller
    if(sellerrevenue[bestprice] < 0):
        return(0, n - bestprice)
    else:
        return(sellerrevenue[bestprice], n - bestprice)

# Computes buyer and seller utility, FB GFT
def utility_computer(sellersupport, sellerdensity, buyersupport, buyerdensity):

    m = len(sellersupport)
    n = len(buyersupport)

    # Computes buyer utility in BOM
    BOM_buyer_utility = sum([individual_BOM_utility(sellersupport, sellerdensity, buyersupport[x])[0]*buyerdensity[x] for x in range(n)])

    # Tradecount_by_buyertype[i] is the number of seller types engaging in trade with buyersupport[i] in BOM
    tradecount_by_buyertype = [individual_BOM_utility(sellersupport, sellerdensity, buyersupport[x])[1] for x in range(n)]

    # Computes seller utility in SOM
    SOM_seller_utility = sum([individual_SOM_utility(buyersupport, buyerdensity, sellersupport[x])[0]*sellerdensity[x] for x in range(m)])

    # Tradecount_by_sellertype[i] is the number of buyer types engaging in trade with sellersupport[i] in SOM
    tradecount_by_sellertype = [individual_SOM_utility(buyersupport, buyerdensity, sellersupport[x])[1] for x in range(m)]

    # Computes optimal (first best) GFT
    gftfb = 0
    # Loops through buyer valuations
    for i in range(0, n):
        # Loops through seller valuations
        for j in range (0, m):
            # Adds term to gftfb if buyer valuation exceeds seller valuation
            if(sellersupport[j] < buyersupport[i]):
                gftfb = gftfb + (buyersupport[i] - sellersupport[j])*(buyerdensity[i])*(sellerdensity[j])

    return(BOM_buyer_utility, SOM_seller_utility, gftfb, tradecount_by_buyertype, tradecount_by_sellertype)

# Computes buyer and seller utility, FB GFT for symmetric case (faster than utility_computer)
def utility_computer_symmetric(sellersupport, sellerdensity, buyersupport, buyerdensity):

    n = len(buyersupport)

    # Variable utility_list initiated to avoid computing individual_BOM_utility multiple times
    utility_list = [individual_BOM_utility(sellersupport, sellerdensity, buyersupport[x]) for x in range(n)]

    # Computes GFT from BOM
    BOM_buyer_utility = sum(utility_list[x][0] * buyerdensity[x] for x in range(n))

    # Tradecount_by_buyertype[i] is the number of seller types engaging in trade with buyersupport[i] in BOM
    tradecount_by_buyertype = [utility_list[x][1] for x in
                               range(n)]

    # Computes optimal (first best) GFT
    gftfb = 0
    # Loops through buyer valuations
    for i in range(0, n):
        # Loops through seller valuations
        for j in range(0, n):
            # Adds term to gftfb if buyer valuation exceeds seller valuation
            if (sellersupport[j] < buyersupport[i]):
                gftfb = gftfb + (buyersupport[i] - sellersupport[j]) * (buyerdensity[i]) * (sellerdensity[j])

    return(BOM_buyer_utility, gftfb, tradecount_by_buyertype)

# For each value in the buyer support, function determines what price the buyer will post in correlated BOM
def correlated_BOM_posted_price(buyer_support, joint_density):

    # Initializes list recording the optimal trade price in BOM for every buyer type (list of integers)
    optimal_posted_price = []

    # Initializes list recording the revenue each buyer type will receive from posting every possible trade price
    # (list of tuples, with each tuple containing a float and a list of floats)
    buyer_revenue_list = []
    for buyer_value in buyer_support:

        # For every buyer type, the conditional seller probabilities (from the buyer's point of view) are recorded
        seller_support = []
        conditional_seller_density = []
        for pair in joint_density:

            # Goes through elements in joint density with desired buyer valuation and records seller valuation/density
            if pair[0][0] == buyer_value:
                seller_support.append(pair[0][1])
                conditional_seller_density.append(pair[1])

        # Ensures values in seller support are increasing
        if (all(x < y for x, y in zip(seller_support, seller_support[1:])) == False):
            print("Seller support not increasing")
            exit()

        m = len(seller_support)

        # Probability is the chance that trade happens from setting trade price at seller_support[i]
        probability = [sum(conditional_seller_density[0:x + 1]) for x in range(m)]

        # Buyer_revenue[i] is the expected revenue to the buyer for setting price at seller_support[i]
        buyer_revenue = [(buyer_value - seller_support[x]) * probability[x] for x in range(m)]

        # Computes bestprice so that seller_support[bestprice] is the profit maximizing price for buyer
        # Error tolerance ensures that buyer will post the lower of two prices if the revenue corresponding to the
        # two prices are roughly equal
        bestprice = 0
        for i in range(1, m):
            if (buyer_revenue[i] > buyer_revenue[bestprice]*error_tolerance):
                bestprice = i

        # If the buyer is guaranteed to lose money from making a trade, bestprice is set to -1 to indicate that trade
        # does not happen
        if buyer_revenue[bestprice] < 0:
            bestprice = -1

        optimal_posted_price.append(bestprice)
        buyer_revenue_list.append((buyer_value, buyer_revenue))

    return(optimal_posted_price, buyer_revenue_list)

# For each value in the seller support, function determines what price the seller will post in correlated SOM
def correlated_SOM_posted_price(seller_support, joint_density):

    # Initializes list recording the optimal trade price in SOM for every seller type (list of integers)
    optimal_posted_price = []

    # Initializes list recording the revenue each seller type will receive from posting every possible trade price
    # (list of tuples, with each tuple containing a float and a list of floats)
    seller_revenue_list = []
    for seller_value in seller_support:

        # For every seller type, the conditional buyer probabilities (from the seller's point of view) are recorded
        buyer_support = []
        conditional_buyer_density = []
        for pair in joint_density:

            # Goes through elements in joint density with desired seller valuations and records buyer valuation/density
            if pair[0][1] == seller_value:
                buyer_support.append(pair[0][0])
                conditional_buyer_density.append(pair[1])

        # Ensures values in buyer support are increasing
        if (all(x < y for x, y in zip(buyer_support, buyer_support[1:])) == False):
            print("Buyer support not increasing")
            exit()

        n = len(buyer_support)

        # Probability is the chance that trade happens from setting trade price at buyer_support[i]
        probability = [sum(conditional_buyer_density[x:]) for x in range(n)]

        # Seller_revenue[i] is the expected revenue to the seller for setting price at buyer_support[i]
        seller_revenue = [(buyer_support[x]-seller_value)*probability[x] for x in range(n)]

        # Computes bestprice so that buyer_support[bestprice] is the profit maximizing price for seller
        # error_tolerance ensures that seller sets higher price in SOM if the revenues associated with the two prices
        # are roughly equal
        bestprice = 0
        for i in range (1, n):
            if(seller_revenue[i]*error_tolerance >= seller_revenue[bestprice]):
                bestprice = i

        # If seller is guaranteed to lose money from trade, then bestprice is set to n to indicate that trade does not
        # happen
        if seller_revenue[bestprice] < 0:
            bestprice = n

        optimal_posted_price.append(bestprice)
        seller_revenue_list.append((seller_value, seller_revenue))

    return(optimal_posted_price, seller_revenue_list)

# Computes the buyer utility in BOM, the seller utility in SOM, and first best gft, in the correlated case
def correlated_utility_computer(joint_density, buyer_support, seller_support):

    # Obtains list of which seller types the buyer will trade with in BOM
    BOM_posted_index_list = correlated_BOM_posted_price(buyer_support, joint_density)[0]

    # Obtains list of what buyer types the seller will trade with in SOM
    SOM_posted_index_list = correlated_SOM_posted_price(seller_support, joint_density)[0]

    # Initializes BOM utility, SOM utility, and first best gft totals
    BOM_utility = 0
    SOM_utility = 0
    first_best_gft = 0

    # Checks each element in the joint density and adds to BOM, SOM, or first best if applicable
    for pair in joint_density:
        buyer_value = pair[0][0]
        seller_value = pair[0][1]
        probability = pair[1]

        # If trading generates negative utility to the buyer, then the trade price in BOM is set so that no seller will
        # agree to the trade
        if BOM_posted_index_list[buyer_support.index(buyer_value)] == -1:
            BOM_trade_price = min(seller_support) - 1

        # If trading is profitable to the buyer, the BOM_trade_price is set to be the exact price the buyer will post
        else:
            BOM_trade_price = seller_support[BOM_posted_index_list[buyer_support.index(buyer_value)]]

        # If trading generates negative utility to the seller, then the trade price in SOM is set so that no buyer will
        # agree to the trade
        if SOM_posted_index_list[seller_support.index(seller_value)] == len(buyer_support):
            SOM_trade_price = max(buyer_support) + 1

        # If trading is profitable to the seller, then SOM_trade_price is set to be the exact price the seller will post
        else:
            SOM_trade_price = buyer_support[SOM_posted_index_list[seller_support.index(seller_value)]]

        # If trade is efficient, then the gains from trade is added to the first best total
        if buyer_value > seller_value:
            first_best_gft = first_best_gft + (buyer_value - seller_value) * probability

        # If trade between these two types happens in BOM, the utility is added to the buyer utility total
        if BOM_trade_price >= seller_value:
            BOM_utility = BOM_utility + (buyer_value - BOM_trade_price) * probability

        # If trade between these two types happens in SOM, the utility is added to the seller utility total
        if SOM_trade_price <= buyer_value:
            SOM_utility = SOM_utility + (SOM_trade_price - seller_value) * probability

    return(BOM_utility, SOM_utility, first_best_gft)

def correlated_gft_computer(joint_density, buyer_support, seller_support):

    # Obtains list of which seller types the buyer will trade with in BOM, along with the revenues the buyer obtains from posting every possible price
    [BOM_posted_index_list, BOM_buyer_revenue_list] = correlated_BOM_posted_price(buyer_support, joint_density)

    # Obtains list of which buyer types the seller will trade with in SOM, along with the revenues the seller obtains from posting every possible price
    [SOM_posted_index_list, SOM_seller_revenue_list] = correlated_SOM_posted_price(seller_support, joint_density)

    # Initializes BOM gft, SOM gft, and first best gft totals
    BOM_gft = 0
    SOM_gft = 0
    first_best_gft = 0

    # Initializes list of how many seller types each buyer type will trade in BOM (and similar for SOM)
    BOM_trade_count_by_buyer_type = [x+1 for x in BOM_posted_index_list]
    SOM_trade_count_by_seller_type = [len(seller_support) - x for x in SOM_posted_index_list]

    # Checks each element in the joint density and adds to BOM, SOM, or first best if applicable
    for pair in joint_density:
        buyer_value = pair[0][0]
        seller_value = pair[0][1]
        probability = pair[1]

        # If trading generates negative utility to the buyer, then the trade price in BOM is set so that no seller will
        # agree to the trade
        if BOM_posted_index_list[buyer_support.index(buyer_value)] == -1:
            BOM_trade_price = min(seller_support) - 1

        # If trading is profitable to the buyer, the BOM_trade_price is set to be the exact price the buyer will post
        else:
            BOM_trade_price = seller_support[BOM_posted_index_list[buyer_support.index(buyer_value)]]

        # If trading generates negative utility to the seller, then the trade price in SOM is set so that no buyer will
        # agree to the trade
        if SOM_posted_index_list[seller_support.index(seller_value)] == len(buyer_support):
            SOM_trade_price = max(buyer_support) + 1

        # If trading is profitable to the seller, then SOM_trade_price is set to be the exact price the seller will post
        else:
            SOM_trade_price = buyer_support[SOM_posted_index_list[seller_support.index(seller_value)]]

        # If trade is efficient, then the gains from trade is added to the first best total
        if buyer_value > seller_value:
            first_best_gft = first_best_gft + (buyer_value - seller_value) * probability

        # If trade between these two types happens in BOM, the gains from trade is added to the BOM total
        if BOM_trade_price >= seller_value:
            BOM_gft = BOM_gft + (buyer_value - seller_value) * probability

        # If trade between these two types happens in SOM, then the gains from trade is added to the SOM total
        if SOM_trade_price <= buyer_value:
            SOM_gft = SOM_gft + (buyer_value - seller_value) * probability


    return (BOM_gft, SOM_gft, first_best_gft, BOM_trade_count_by_buyer_type, SOM_trade_count_by_seller_type,
            BOM_buyer_revenue_list, SOM_seller_revenue_list)

# Constructs joint density that minimizes the ratio of (BOM+SOM)/FB for a given support size
# joint_density[i][j] is the probability that the buyer valuation is i and the seller valuation is j
def bom_som_minimum_ratio_density(support_size):

    # Checks if buyer support size is even
    if support_size % 2 != 0:
        print("Support size must be even")
        exit()

    # Initializes joint density, joint_density[i][j] is the probability that buyer=i, seller=j
    joint_density = np.zeros((support_size + 1, support_size + 1))

    joint_density[support_size][0] = 1 / support_size
    for seller in range(1, int(support_size / 2)):
        joint_density[support_size][seller] = 1 / ((support_size - seller) * (support_size - seller + 1))

    for buyer in range(1, support_size):
        for seller in range(1, buyer):
            if buyer + seller > support_size:
                joint_density[buyer][seller] = 1 / ((buyer + 1) * (buyer - seller) * (buyer - seller + 1))

    for seller in range(int(support_size / 2), support_size - 1):
        joint_density[support_size][seller] = sum([joint_density[buyer][seller] for buyer in range(support_size)]) / (
                    support_size - seller - 1)

    for buyer in range(1, support_size):
        for seller in range(0, buyer):
            if buyer + seller < support_size:
                k = support_size - buyer - seller
                joint_density[buyer][seller] = joint_density[buyer + k][seller + k]

    for seller in range(1, int(support_size / 2)):
        joint_density[support_size - seller][seller] = 1 / (
                    (support_size - seller + 1) * (support_size - seller * 2)) - sum(
            [joint_density[support_size - seller][i] for i in range(seller)])

    return joint_density


