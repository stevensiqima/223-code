# Contains lp_functions related to computing virtual valuations

# Calculates virtual valuation for buyer (phi function)
def virtualvaluationbuyer(buyersupport, buyerdensity):
    n = len(buyersupport)

    # Probability[i] is the sum buyerdensity[i+1]+...+buyerdensity[n-1]
    probability = [sum(buyerdensity[x+1:]) for x in range(n-1)]

    # Computes virtual valuation for first n-1 terms
    valuation = [buyersupport[x]-(buyersupport[x+1]-buyersupport[x])*probability[x]/buyerdensity[x] for x in range(n-1)]

    # Adds on virtual valuation for final term
    valuation.append(buyersupport[n-1])

    # Checks if distribution is regular
    if (all(x <= y for x, y in zip(valuation, valuation[1:]))):
        regularity = "regular"
    else:
        regularity = "non-regular"
    return(valuation, regularity)

# Calculates virtual valuation for seller (tau function)
def virtualvaluationseller(sellersupport, sellerdensity):
    m = len(sellersupport)

    # Probability[i] is the sum sellerdensity[0]+...+sellerdensity[i]
    probability = [sum(sellerdensity[0:x]) for x in range(1, m)]

    # Computes virtual valuations for terms 1, 2, 3, ... n-1
    valuation = [sellersupport[x]+(sellersupport[x]-sellersupport[x-1])*probability[x-1]/sellerdensity[x] for x in range(1, m)]

    # Adds on virtual valuation for term 0
    valuation.insert(0, sellersupport[0])

    # Checks if distribution is regular
    if (all(x <= y for x, y in zip(valuation, valuation[1:]))):
        regularity = "regular"
    else:
        regularity = "non-regular"
    return (valuation, regularity)

# Given buyer support and desired virtual valuation, function computes necessary densities
# Common mulitple is essentially a value to multiply all values in the density by - in order to make all densities integers
def virtualvaluationbuyerinverse(buyersupport, virtualvaluation, common_multiple):
    buyerdensity = []
    length = len(buyersupport)

    # Sets default density of initial term to be common_multiple
    buyerdensity.append(common_multiple)

    # Computes density of remaining terms
    for i in range (1, length):
        buyerdensity.append(((buyersupport[length-i]-buyersupport[length-1-i])*(sum(buyerdensity))/(buyersupport[length-1-i]-virtualvaluation[length-1-i])))

        # Ensures that terms in buyerdensity are integers if terms in buyersupport are integers
        buyerdensity[:] = [x * (buyersupport[length-1-i]-virtualvaluation[length-1-i]) for x in buyerdensity]
    buyerdensity.reverse()


    return(buyerdensity)

# Given seller support and desired virtual valuation, function computes necessary densities
# Common mulitple is essentially a value to multiply all values in the density by - in order to make all densities integers
def virtualvaluationsellerinverse(sellersupport, virtualvaluation, common_multiple):
    length = len(sellersupport)
    sellerdensity = []

    # Sets default density of initial term to be common_multiple
    sellerdensity.append(common_multiple)

    # Computes density of remaining terms
    for i in range(1, length):
        sellerdensity.append(sum(sellerdensity)*(sellersupport[i]-sellersupport[i-1])/(virtualvaluation[i]-sellersupport[i]))

        # Ensures that terms in sellerdensity are integers if terms in sellersupport are integers
        sellerdensity[:] = [x * (virtualvaluation[i]-sellersupport[i]) for x in sellerdensity]
    return(sellerdensity)


