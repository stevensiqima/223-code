import numpy as np

# Given range of buyer/seller support and alpha, function returns coefficients corresponding to gft_bom+gft_som-alpha*gft_fb
# and constraints corresponding to when the buyer always sets p = 0 in BOM, and the seller always sets p = n in SOM
# n+1 is the size of the buyer/seller supports, and the supports must both be (0, 1, 2, ... n)
def minimum_ratio_checker_extreme_case(n, alpha):
    # gft_bom is an array of the coefficients of gft in bom when the buyer always posts price p = 0
    # gft_som is an array of the coefficients of gft in som when the seller always posts price p = n
    gft_bom = np.zeros((n+1, n+1))
    gft_som = np.zeros((n+1, n+1))
    for i in range(n+1):
        gft_bom[0, i] = i
        gft_som[i, n] = n-i

    # gft_fb is an array of the coefficients of gft in the first best case
    gft_fb = np.zeros((n+1, n+1))
    for i in range(n+1):
        for j in range(i+1, n+1):
            gft_fb[i, j] = j-i

    # coefficient_to_minimize is the list of coefficients of the expression we want to minimize in the linear program
    coefficient_to_minimize = list((gft_bom + gft_som - alpha*gft_fb).flatten())

    # Constraints is the matrix of constraints in the linear program
    constraints = []

    # Adds in constraints for BOM
    for i in range(n+1):

        # buyer_utility_setting_lowest_price is array of coefficients associated with buyer's utility from setting price p = 0 when his valuation is i
        buyer_utility_setting_lowest_price = np.zeros((n + 1, n + 1))
        buyer_utility_setting_lowest_price[0, i] = i

        for k in range(1, i):

            # buyer_utility_setting_other_price is array of coefficients associated with buyer's utility from setting price p = k when his valuation is i
            # We check utility from setting price p = 1, 2, 3, ... i-1 and compare with utility from setting price p = 0
            buyer_utility_setting_other_price = np.zeros((n + 1, n + 1))
            for j in range(0, k+1):
                buyer_utility_setting_other_price[j, i] = i - k

            # bom_constraint is the constraint that setting price p = 0 should give at least as much utility to the buyer as setting price p = k
            bom_constraint = list((buyer_utility_setting_other_price - buyer_utility_setting_lowest_price).flatten())
            constraints.append(bom_constraint)

    # Adds in constraints for SOM
    for i in range(n+1):

        # seller_utility_setting_highest_price is array of coefficients associated with seller's utility from setting price p = n when his valuation is i
        seller_utility_setting_highest_price = np.zeros((n + 1, n + 1))
        seller_utility_setting_highest_price[i, n] = n-i

        for k in range(i+1, n):

            # seller_utility_setting_other_price is array of coefficients associated with seller's utility from setting price p = k when his valuation is i
            # We check utility from setting price p = i+1, i+2, ... n-1 and compare with utility from setting price p = n
            seller_utility_setting_other_price = np.zeros((n + 1, n + 1))
            for j in range(k, n+1):
                seller_utility_setting_other_price[i, j] = k - i

            # som_constraint is the constraint that setting price p = n should give at least as much utility to the buyer as setting price p = k
            som_constraint = list((seller_utility_setting_other_price - seller_utility_setting_highest_price).flatten())
            constraints.append(som_constraint)


    # bound_on_constraints is the upper bound for the constraints (which is all zeroes)
    bound_on_constraints = [0]*len(constraints)

    return(coefficient_to_minimize, constraints, bound_on_constraints)