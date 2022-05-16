from encodings import utf_8
import time
import requests
import csv
from authInfo import apiKey
#import json

# file reading and writing variables
nftNameList = 'town_list.csv'
# tableHead = [
#     'Name',
#     'TokenID',
#     'Points'
# ]
tableHead = [
    'Name',
    'Price',
    'Points',
    'Link'
]
csvWriteFile = ''

# api related variables
nullAddress = "0x0000000000000000000000000000000000000000"
targetURL = "https://api.opensea.io/wyvern/v1/orders"
resultLimit = 50
resultOffset = 0

apiHeaders = {
    "Accept": "application/json",
    "X-API-KEY": apiKey()
}

apiParams = [
    ('asset_contract_address', '0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c'),
    ('bundled', 'false'),
    ('include_bundled', 'false'),
    ('side', '1'),
    ('limit', str(resultLimit)),
    #('order_by', 'created_date'),
    ('order_by', 'eth_price'),
    ('order_direction', 'asc'),
    #('token_id', '11909882842232846221218111260111887400960')
]

didread = 0
# dict mapping tokenId to town points earned
lookupDict = {}
# read nft information from the reference file
with open(nftNameList, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if(row['TokenID'] == '0'):
            continue
        else:
            lookupDict[row['TokenID']] = row['Points']
            apiParams.append(('token_ids', row['TokenID']))
        didread += 1
        if(didread >= 7):
            break
        
print(lookupDict)

#lookupDict['11909882842232846221218111260111887400960'] = '1'

# list of dictionaries representing possible opensea orders
# {Name:  ,Price:  ,Points:  ,Link:}
possibleOrders = []

isNextPage = True
while(isNextPage):
    offsetParam = [
        ('offset', str(resultOffset))
    ]
    response = requests.get(
        targetURL,
        headers = apiHeaders,
        params = apiParams + offsetParam
    )
    jsonResponse = response.json()
    resultOrders = jsonResponse['orders']
    # for each order grab the name, points, link, and price
    for o in resultOrders:
        name = o['asset']['name']
        id = o['metadata']['asset']['id']
        # use token id to reference the points earned from csv file
        points = lookupDict[id]
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
            eth_price = float(o['payment_token_contract']['eth_price'])
            conversion = float(price) * eth_price
            price = str(conversion)
        # add order info to list of possible orders 
        possibleOrders.append({
            'Name': name,
            'Price': price,
            'Points': points,
            'Link': link
        })
        #print(possibleOrders)
        #break

    # update the pagination offset for api request 
    if(len(resultOrders) < resultLimit):
        isNextPage = False
    else:
        resultOffset += resultLimit
    #break
    
print(possibleOrders)


# requestOffset = 0
# url = "https://api.opensea.io/wyvern/v1/orders?asset_contract_address=0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c&bundled=false&include_bundled=false&token_ids=158571582985157323973932567063203986538496&token_ids=203148573051800262687634640636765622239232&token_ids=174905136597362370220174548219928860688384&side=1&limit=20&offset=0&order_by=created_date&order_direction=desc"



# headers = {
#     "Accept": "application/json",
#     "X-API-KEY": apiKey()
# }

# params = [
#     ('asset_contract_address', '0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c'),
#     ('bundled', 'false'),
#     ('include_bundled', 'false'),
#     ('side', '1'),
#     ('limit', '1'),
#     ('offset', str(requestOffset)),
#     ('order_by', 'created_date'),
#     ('order_direction', 'desc'),
#     ('token_id', '158571582985157323973932567063203986538496')
# ]

# # response = requests.get(url, headers=headers)
# response = requests.get(
#     targetURL, 
#     headers = headers,
#     params = params
# )
# print(response.request.url)
# print(response.json())