# Web scraping OpenSea and RarityTools
#import requests
import time
from tkinter import Grid
from bs4 import BeautifulSoup
from selenium import webdriver
 
'''
Input: list of selected BS4 tags from rarity.tools
Ouput: list of dictionaries with rarity.tools listing info
    {name: nft name, link: nft view link, price: opeansea price}
'''
def scrapeCells(cellList):
    infoList = []
    for cell in cellList:
        cellChildren = cell.contents
        link = cellChildren[2].a['href']
        name = str(cellChildren[4].string).strip()
        price = str(cellChildren[6].a.string)
        infoList.append({
            "name" : name,
            "link" : link,
            "price":  price
        })
    return infoList

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox()
driver.get("https://rarity.tools/collectvox?filters=%24buyNow%24On%3Atrue%3B%26auction%24On%3Atrue")
#driver.get("https://opensea.io/collection/town-star?search[sortAscending]=true&search[sortBy]=PRICE&search[stringTraits][0][name]=game&search[stringTraits][0][values][0]=Town%20Star&search[stringTraits][1][name]=category&search[stringTraits][1][values][0]=Building&search[stringTraits][1][values][1]=Crafting&search[stringTraits][1][values][2]=Farm%20Stands&search[stringTraits][1][values][3]=Storage&search[stringTraits][1][values][4]=Towers&search[stringTraits][1][values][5]=Solar%20Panels&search[stringTraits][1][values][6]=Trophy&search[stringTraits][1][values][7]=Fountains&search[stringTraits][1][values][8]=Death%20Row%20Records&search[stringTraits][1][values][9]=ElfBot&search[stringTraits][1][values][10]=Gala%20Music&search[stringTraits][1][values][11]=Trade%20Vehicles&search[stringTraits][1][values][12]=Exchange&search[stringTraits][1][values][13]=Snoop%20Dogg&search[stringTraits][1][values][14]=Misc&search[stringTraits][1][values][15]=Saltybot&search[stringTraits][1][values][16]=Galaverse%20Tickets&search[stringTraits][1][values][17]=Crafter")
time.sleep(8)
soup = BeautifulSoup(driver.page_source, 'html.parser')
nextBtn = soup.select('div.smallBtn.select-none')[0]
print(nextBtn)
gridCells = soup.select(".transform")
infoList = []
#print(type(gridCells[0].contents[2].a['href']))
# for cell in gridCells:
#     cellChildren = cell.contents
#     link = cellChildren[2].a['href']
#     #print(linkAnchor)
#     name = str(cellChildren[4].string).strip()
#     price = str(cellChildren[6].a.string)
#     infoList.append({
#         "name" : name,
#         "link" : link,
#         "price":  price
#     })

print(infoList)    
#print(GridCells)
print(len(gridCells))
#print(soup.prettify())
driver.close()
# m-1.lg:m-1.5.mb-2.border.overflow-hidden.transition-all.border-gray-300.dark:border-gray-800.rounded-md.shadow-md.hover:border-pink-600.hover:-translate-y-1.5.hover:shadow-lg.transform.bg-white.bgCard
