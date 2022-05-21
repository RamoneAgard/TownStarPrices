import time
import requests
import csv
from authInfo import apiKey

# token contract address for nft collection
tokenContractAddress = '0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c'

# file reading and writing variables
nftNameList = 'town_list.csv'
tableHead = [
    'Name',
    'Price',
    'Points',
    'Link'
]
csvWriteFile = 'townstar_nft_orders.csv'

# api related variables
targetURL = "https://api.opensea.io/wyvern/v1/orders"
resultLimit = 50
resultOffset = 0
maxNumIds = 30
apiHeaders = {
    "Accept": "application/json",
    "X-API-KEY": apiKey()
}
apiParams = [
    ('asset_contract_address', tokenContractAddress),
    #('bundled', 'false'),
    #('include_bundled', 'false'),
    ('side', '1'),
    ('limit', str(resultLimit)),
    #('order_by', 'created_date'),
    ('order_by', 'eth_price'),
    ('order_direction', 'asc'),
    #('token_id', '11909882842232846221218111260111887400960')
]

'''
read from an nft reference file
- returns a dictionary mapping tokenIds to points earned
- also returns a list of opeansea api params for the tokenIds 
if apiList is set to true
- optional placeholder can be defined if one is used to skip
entries in the file
'''
def readReferenceFile(csvFile, apiList = False, encoding = 'utf-8', placeholder = '0'):
    # dict mapping tokenId to points earned
    referenceDict = {}
    apiTuples = []
    # read nft information from the reference file
    with open(csvFile, 'r', newline='', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if(row['TokenID'] == placeholder):
                continue
            else:
                referenceDict[row['TokenID']] = row['Points']
                if apiList:
                    apiTuples.append(('token_ids', row['TokenID']))
    return (referenceDict,apiTuples) if apiList else referenceDict
    
'''
write list of dictionaries representing opensea orders to 
a csv file 
'''
def writeOrdersToFile(csvFile, fileHeaders, orderList, encoding = 'utf-8'):
    with open(csvFile, 'w', newline='', encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fileHeaders)
        writer.writeheader()
        writer.writerows(orderList)
    print("Orders writtern to file:", csvFile)

'''
for each opensea sell order in json format grab the
name, points, link, and price
'''
def retrieveOrders(apiOrders, pointReference):
    orderInfoList = []
    for o in apiOrders:
        name = o['asset']['name']
        id = o['metadata']['asset']['id']
        # use token id to reference the points earned from csv file
        points = pointReference[id]
        link = o['asset']['permalink']
        priceStr = o['base_price']
        # see what token the order takes as payment
        payToken = o['payment_token_contract']['symbol']
        decimalNums = int(o['payment_token_contract']['decimals'])
        # adjust length of price string to include all decimal places
        if(len(priceStr) < decimalNums):
            diff = decimalNums - len(priceStr)
            priceStr = ('0' * diff) + priceStr
        # insert the decimal in the right place
        price = priceStr[:-decimalNums] + '.' + priceStr[-decimalNums:]
        # convert payment token to eth equivalent if not already 
        if(payToken != 'ETH'):
            ethPrice = float(o['payment_token_contract']['eth_price'])
            conversion = float(price) * ethPrice
            price = str(conversion)
        # add order info to list of possible orders 
        orderInfoList.append({
            'Name': name,
            'Price': price,
            'Points': points,
            'Link': link
        })
    return orderInfoList



# grab the nft information from the reference file
lookupDict, apiTokenIds = readReferenceFile(nftNameList, True)
print("number of token ids:", len(apiTokenIds))

# list of dictionaries representing possible opensea orders
# {Name:  ,Price:  ,Points:  ,Link:}
possibleOrders = []
isNextPage = True
writeToFile = True
requestCount = 0

while(isNextPage):
    idOffset = maxNumIds if (len(apiTokenIds) > maxNumIds) else len(apiTokenIds)
    offsetParam = [
        ('offset', str(resultOffset))
    ]
    response = requests.get(
        targetURL,
        headers = apiHeaders,
        params = apiParams + offsetParam + apiTokenIds[:idOffset]
    )
    if(response.status_code != 200):
        print("Response status code:", response.status_code)
        print(response.text)
        writeToFile = False
        break
    else:
        requestCount += 1

    jsonResponse = response.json()
    resultOrders = jsonResponse['orders']
    # collect relevant order information
    possibleOrders.extend(retrieveOrders(resultOrders, lookupDict))

    print("length of result order:", len(resultOrders))
    # update the pagination offset for api request 
    if(len(resultOrders) < resultLimit):
        if(len(apiTokenIds) > maxNumIds):
            apiTokenIds = apiTokenIds[maxNumIds:]
            resultOffset = 0
            print("Reduce api token length")
        else:
            print("End of api calls")
            isNextPage = False
            break
    else:
        resultOffset += resultLimit
    print("after request number:", requestCount, " offset:", resultOffset, " aip token length:", len(apiTokenIds) )
    # if requestCount > 5:
    #     break
    time.sleep(0.5)

# write the opensea order information to a file
if writeToFile: 
    writeOrdersToFile(csvWriteFile, tableHead, possibleOrders)
