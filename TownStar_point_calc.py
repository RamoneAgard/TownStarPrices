import csv



'''
read nft orders from a csv file
return a list of dictionaries with column headers as keys
'''

def readOrderFile(csvFile, ethPrice, encoding = 'utf-8'):
    orderList = []
    # read nft information from the reference file
    with open(csvFile, 'r', newline='', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            orderList.append({
                'Name': row['Name'],
                'Price': int(float(row['Price']) * ethPrice),
                'Points': float(row['Points']),
                'Link' : row['Link']
            })
    return orderList




# run algorithm to determine max earnings within investment range for each limit in capList
# returns a dict {$cap: [list of orders]}

def findBestOrders(orderList, capList, townPrice = 0.1):
    cap = max(capList)
    n = len(orderList)
    bestO = [ [0 for x in range(cap + 1)] for y in range(2) ]
    itemTrace = [ [[] for x in range(cap + 1)] for y in range(2) ]
    max1 = 0
    max2 = 0
    max1List  = []
    max2List  = []
    for i in range(n+1):
        for c in range(cap+1):
            if(i == 0 or c == 0):
                bestO[i % 2][c] = 0
            elif(orderList[i-1]['Price'] <= c):
                useOrder = orderList[i-1]['Points'] + bestO[(i-1) % 2][c - orderList[i-1]['Price']]
                passOrder = bestO[(i-1) % 2][c]
                if(useOrder > passOrder):
                    bestO[i % 2][c] = useOrder
                    itemTrace[i % 2][c] = [i-1] + itemTrace[(i-1) % 2][c - orderList[i-1]['Price']]
                else:
                    bestO[i % 2][c] = passOrder
                    itemTrace[i % 2][c] = itemTrace[(i-1) % 2][c]
            else:
                bestO[i % 2][c] = bestO[(i-1) % 2][c]
                itemTrace[i % 2][c] = itemTrace[(i-1) % 2][c]
            if(bestO[i % 2][c] > max1):
                max2 = max1
                max2List = max1List
                max1 = bestO[i % 2][c]
                max1List = itemTrace[i % 2][c]
                
    # print("Max 2:", max2)
    # print("Max 2 List:")
    # for dex in max2List:
    #     print(orderList[dex])
    res = {}
    for c in capList:
        orders = []
        for dex in itemTrace[n % 2][c]:
            orders.append(orderList[dex])
        res[c] = orders

    return res


# reference file names
voxOrdersFile = 'townstar_vox_nfts.csv'
townOrdersFile = 'townstar_nft_orders.csv'

# how much money to invest 
buyLimitList = [
    2500,
    5000,
    7500,
    10000,
    15000,
    20000,
    25000,
    30000
]
ethPriceUSD = 1950.00
townPriceUSD = 0.04
townPointConversion = 0.58

# retrieve list of orders from files 
allOrders = []
allOrders.extend(readOrderFile(townOrdersFile, ethPriceUSD))
allOrders.extend(readOrderFile(voxOrdersFile, ethPriceUSD))
print("Number of total orders:", len(allOrders))

bestOrders = findBestOrders(allOrders, buyLimitList, townPriceUSD)

for c in buyLimitList:
    print("Best list for $:", c)
    totalCost = 0.0
    totalPoints = 0.0
    print("Order List:")
    for order in bestOrders[c]:
        totalCost += order['Price']
        totalPoints += order['Points']
        print(order)
    usdEarnings = (totalPoints * townPointConversion) * townPriceUSD
    print("number of nfts:", len(bestOrders[c]))
    print("Total Cost: $",totalCost)
    print("Total TOWN Points:",totalPoints," ( = $", usdEarnings, " at current price of TOWN)") 
    print("Time to make money back is ", (totalCost/usdEarnings), " days" ) 
    print()
    print()