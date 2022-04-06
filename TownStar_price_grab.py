# Web scraping OpenSea and RarityTools
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
 

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox()
#page = requests.get("https://rarity.tools/collectvox?filters=%24buyNow%24On%3Atrue%3B%26auction%24On%3Atrue")
driver.get("https://opensea.io/collection/town-star?search[sortAscending]=true&search[sortBy]=PRICE&search[stringTraits][0][name]=game&search[stringTraits][0][values][0]=Town%20Star&search[stringTraits][1][name]=category&search[stringTraits][1][values][0]=Building&search[stringTraits][1][values][1]=Crafting&search[stringTraits][1][values][2]=Farm%20Stands&search[stringTraits][1][values][3]=Storage&search[stringTraits][1][values][4]=Towers&search[stringTraits][1][values][5]=Solar%20Panels&search[stringTraits][1][values][6]=Trophy&search[stringTraits][1][values][7]=Fountains&search[stringTraits][1][values][8]=Death%20Row%20Records&search[stringTraits][1][values][9]=ElfBot&search[stringTraits][1][values][10]=Gala%20Music&search[stringTraits][1][values][11]=Trade%20Vehicles&search[stringTraits][1][values][12]=Exchange&search[stringTraits][1][values][13]=Snoop%20Dogg&search[stringTraits][1][values][14]=Misc&search[stringTraits][1][values][15]=Saltybot&search[stringTraits][1][values][16]=Galaverse%20Tickets&search[stringTraits][1][values][17]=Crafter")
time.sleep(5)
driver.close()