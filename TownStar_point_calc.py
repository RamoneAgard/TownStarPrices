import csv
# reference file names
voxOrdersFile = 'townstar_vox_nfts.csv'
townOrdersFile = 'townstar_nft_orders.csv'

# how much money to invest 
buyLimit = 10000

'''
read nft orders from a csv file
return a list of dictionaries with column headers as keys
'''
def readOrderFile(csvFile, encoding = 'utf-8'):
    orderList = []
    # read nft information from the reference file
    with open(csvFile, 'r', newline='', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            orderList.append(dict(row))
    return orderList


# retrieve list of orders from files 
allOrders = []
allOrders.extend(readOrderFile(townOrdersFile))
allOrders.extend(readOrderFile(voxOrdersFile))

# run algorithm to determine max earnings within investment range 

