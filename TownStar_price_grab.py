# Web scraping OpenSea and RarityTools
# Vox chainID = (Vox Collectibles #) + 584
#import requests
import time
#from tkinter import E
#from tkinter import Grid
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

hrefBase =  "https://rarity.tools"
options = webdriver.FirefoxOptions()
options.add_argument('--headless')

'''
Input: list of selected BS4 tags from rarity.tools
Ouput: list of dictionaries with rarity.tools listing info
    {name: nft name, link: nft view link, price: opeansea price}
'''
# def scrapeCells(driver, soup, cellSelector):
#     cellList = soup.select(cellSelector)
#     infoList = []
#     for cell in cellList:
#         cellChildren = cell.contents
#         link = cellChildren[2].a['href']
#         driver.find_element((By.CSS_SELECTOR, "a[href='"+link+"']"))
#         driver.click()
#         name = str(cellChildren[4].string).strip()
#         price = str(cellChildren[6].a.string)
#         infoList.append({
#             "name" : name,
#             "link" : link,
#             "price":  price
#         })
#     return infoList

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

# def nextReultsPage(driver, ):

driver = webdriver.Firefox()
driver.get("https://rarity.tools/collectvox?filters=%24buyNow%24On%3Atrue%3B%26auction%24On%3Atrue")
#driver.get("https://opensea.io/collection/town-star?search[sortAscending]=true&search[sortBy]=PRICE&search[stringTraits][0][name]=game&search[stringTraits][0][values][0]=Town%20Star&search[stringTraits][1][name]=category&search[stringTraits][1][values][0]=Building&search[stringTraits][1][values][1]=Crafting&search[stringTraits][1][values][2]=Farm%20Stands&search[stringTraits][1][values][3]=Storage&search[stringTraits][1][values][4]=Towers&search[stringTraits][1][values][5]=Solar%20Panels&search[stringTraits][1][values][6]=Trophy&search[stringTraits][1][values][7]=Fountains&search[stringTraits][1][values][8]=Death%20Row%20Records&search[stringTraits][1][values][9]=ElfBot&search[stringTraits][1][values][10]=Gala%20Music&search[stringTraits][1][values][11]=Trade%20Vehicles&search[stringTraits][1][values][12]=Exchange&search[stringTraits][1][values][13]=Snoop%20Dogg&search[stringTraits][1][values][14]=Misc&search[stringTraits][1][values][15]=Saltybot&search[stringTraits][1][values][16]=Galaverse%20Tickets&search[stringTraits][1][values][17]=Crafter")
#time.sleep(8)
soup = ''
btnGroup = ''
#waitCount = 0
done = 0
try: 
    if(WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR,'div.smallBtn.select-none'),'Next'))):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        btnGroup = driver.find_element_by_css_selector('div.smallBtn.select-none')
    else:
        print("Could not meet condition for wait")
        done = 1
except exceptions.TimeoutException:
    print("Driver Wait timeout")
    done = 1
except exceptions.NoSuchElementException:
    print("Could not find element")
    done = 1
except:
    print("Something went wrong")
    done = 1

if(done == 1):
    driver.close()
    done = 2
else:
    print("did it")
    print(btnGroup)

# scrapeInfo = []
# while(done == 0):
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div.transform')))
#         gridCells = soup.select(".transform")
#         scrapeInfo.append(scrapeCells(gridCells))
#         btnGroup.click()
#     except exceptions.StaleElementReferenceException:
#         print("End of pages to scrape")
#         done = 1
#     except exceptions.TimeoutException:
#         print("Driver wait timeout")
#         done = 1
#     except: 
#         print("Something else went wrong")
#         done = 1
#     time.sleep(5)


# btnGroup.click()
# time.sleep(5)
# btnGroup.click()
# time.sleep(5)
# btnGroup.click()
# time.sleep(5)
# btnGroup.click()
# time.sleep(5)
# btnGroup.click()
# time.sleep(5)


# while(len(btnGroup) < 1 and waitCount < 10):
#     time.sleep(2)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     btnGroup = driver.find_elements_by_css_selector('.smallBtn.select-none')
#     waitCount += 1
#     print("loading..." + str(waitCount))

# if(len(btnGroup) < 1):
#     driver.close()

# nextBtn = btnGroup[0]
# time.sleep(5)
# print(nextBtn)
# nextBtn.click()
# time.sleep(8)
# nextBtn.click()
# time.sleep(8)
gridCells = soup.select(".transform")
infoList = []
# print(type(gridCells[0].contents[2].a['href']))
currPage = driver.current_url
count = 0
for cell in gridCells:
    cellChildren = cell.contents
    link = cellChildren[2].a['href']
    score = ""
    viewLink = hrefBase + link
    driver.get(viewLink)
    try:
        loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'div.font-extrabold.text-green-500')))
        if(loaded):
            webEle = driver.find_element_by_css_selector('div.font-extrabold.text-green-500')
            score = webEle.get_attribute("innerText")
            print(score)
            print(type(score))
    except exceptions.TimeoutException:
        print("Driver wait timeout -- view url")
        done = 1
        break
    # webEle = driver.find_element(By.CSS_SELECTOR, linkSelector)
    # print(webEle)
    # webEle.click()
    # print(linkAnchor)
    name = str(cellChildren[4].string).strip()
    price = str(cellChildren[6].a.string)
    infoList.append({
        "name" : name,
        "price":  price,
        "points": score,
        "link" : viewLink,
    })
    count += 1
    if (count >= 5):
        break

done = 1
time.sleep(5)
print(infoList)    
#print(GridCells)
#print(len(gridCells))
#print(soup.prettify())

if(done == 1):
    driver.close()
# m-1.lg:m-1.5.mb-2.border.overflow-hidden.transition-all.border-gray-300.dark:border-gray-800.rounded-md.shadow-md.hover:border-pink-600.hover:-translate-y-1.5.hover:shadow-lg.transform.bg-white.bgCard
