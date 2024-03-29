# Web scraping OpenSea and RarityTools
# Vox chainID = (Vox Collectibles #) + 584

import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions


# global values
hrefBase =  "https://rarity.tools"
myOptions = webdriver.FirefoxOptions()
myOptions.add_argument('--headless')


'''
basic custom error class
'''
class CustomError(Exception):
    pass

'''
Input: list of selected BS4 tags from rarity.tools and the webdriver to use
Ouput: list of dictionaries with rarity.tools listing info
    {name: nft name, priceEth: opeansea price, Score: rarity score, Link: view link}
    (Throws exception if view page cannot load)
'''
def scrapeCells(cellList, driver):
    scrapeList = []
    for cell in cellList:
        cellChildren = cell.contents
        link = cellChildren[2].a['href']
        viewLink = hrefBase + link

        driver.get(viewLink)
        loaded = WebDriverWait(driver, 15).until( EC.presence_of_element_located(
            (By.CSS_SELECTOR,'div.font-extrabold.text-green-500')))
        if(not loaded):
            raise CustomError("Something went wrong in scrapeCells function ")
            
        webEle = driver.find_element_by_css_selector('div.font-extrabold.text-green-500')
        score = webEle.get_attribute("innerText")
        name = str(cellChildren[4].string).strip()
        price = str(cellChildren[6].a.string)[:-4]
        scrapeList.append({
            "Name" : name,
            "Price":  price,
            "Points": score,
            "Link" : viewLink,
        })
        # break
    return scrapeList

'''
Input: Webdriver to use
Output: the WebElement associated with the next page results button
        (Throws an exception if button is not found)
'''
def getNextBtn(driver):
    if(WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='select-none smallBtn'][contains(text(),'Next')]")))):
        return driver.find_element(By.XPATH,"//div[@class='select-none smallBtn'][contains(text(),'Next')]")
    else:
        raise CustomError("Something else went wrong retrieving the next button")




target_csv_file = "townstar_vox_nfts.csv"
target_url = "https://rarity.tools/collectvox?filters=%24buyNow%24On%3Atrue%3B%26auction%24On%3Atrue"
# create WebDriver and get desired rarity.tools page plus the filters
driver = webdriver.Firefox(options=myOptions)
#driver.get("https://opensea.io/collection/town-star?search[sortAscending]=true&search[sortBy]=PRICE&search[stringTraits][0][name]=game&search[stringTraits][0][values][0]=Town%20Star&search[stringTraits][1][name]=category&search[stringTraits][1][values][0]=Building&search[stringTraits][1][values][1]=Crafting&search[stringTraits][1][values][2]=Farm%20Stands&search[stringTraits][1][values][3]=Storage&search[stringTraits][1][values][4]=Towers&search[stringTraits][1][values][5]=Solar%20Panels&search[stringTraits][1][values][6]=Trophy&search[stringTraits][1][values][7]=Fountains&search[stringTraits][1][values][8]=Death%20Row%20Records&search[stringTraits][1][values][9]=ElfBot&search[stringTraits][1][values][10]=Gala%20Music&search[stringTraits][1][values][11]=Trade%20Vehicles&search[stringTraits][1][values][12]=Exchange&search[stringTraits][1][values][13]=Snoop%20Dogg&search[stringTraits][1][values][14]=Misc&search[stringTraits][1][values][15]=Saltybot&search[stringTraits][1][values][16]=Galaverse%20Tickets&search[stringTraits][1][values][17]=Crafter")

writeInfoToFile = True
amendFile = False
#list of total scraped info
infoList = []
pageNum = 1
clickCount = 1

while(True):
    driver.get(target_url)
    # wait for results to load 
    try:
        nextBtn = getNextBtn(driver)
        if nextBtn != None:
            for x in range(pageNum-1):
                nextBtn.click()
                time.sleep(1)
        else:
            print("Failed to get next button")
            writeInfoToFile = False
            break
        loaded = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR,'div.transform')))
        if(not loaded):
            print("Driver wait returned false")
            writeInfoToFile = False
            break
    except exceptions.TimeoutException:
        print("Timeout loading page results")
        writeInfoToFile = False
        break
    except exceptions.NoSuchElementException:
        print("Found but could not retrieve next button")
        print("Something went wrong")
        writeInfoToFile = False
        break
    except CustomError as e:
        print(e.__str__)
        writeInfoToFile = False
        break
    except exceptions.StaleElementReferenceException:
        print("No next page")
        print("End of Scraping")
        break

    # soup the page source and extract result cells 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    gridCells = soup.select(".transform")

    # try to append more scrapped information to total list
    try:
        infoList.extend(scrapeCells(gridCells, driver))
    except exceptions.TimeoutException:
        print("Driver Timeout scraping page results")
        #writeInfoToFile = False
        if pageNum == 1:
            writeInfoToFile = False
        break
    except CustomError as e:
        print(e.__str__)
        writeInfoToFile = False
        break
    time.sleep(4)
    print("End of page", pageNum)
    # if(pageNum >= 4):
    #     break
    pageNum += 1

driver.quit()

# Write the info to csv file if its still okay to
if(writeInfoToFile):
    openParam = 'a' if amendFile else 'w'
    with open(target_csv_file, openParam, newline='', encoding='utf-8') as f:
        headers = ['Name', 'Price', 'Points', 'Link']
        writer = csv.DictWriter(f, fieldnames=headers)
        if not amendFile:
            writer.writeheader()
        writer.writerows(infoList)
    print("Results written to file:", target_csv_file)
        
