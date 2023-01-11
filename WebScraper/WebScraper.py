from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import numpy as np

import time


def initCrawler(minSize, maxSize):

    minSize = str(minSize)
    maxSize = str(maxSize)

    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--window-size=1366x768")

    driver = webdriver.Chrome(options=options,
                              executable_path="/home/mansur/.local/bin/chromedriver")

    # url = "https://www.hemnet.se/salda/bostader?housing_form_groups%5B%5D=apartments&location_ids%5B%5D=18031&page=1"

    url = "https://www.hemnet.se/salda/bostader?location_ids%5B%5D=18031&item_types%5B%5D=bostadsratt&living_area_min=" + \
        minSize + "&living_area_max=" + maxSize + "&sold_age=all"

    driver.get(url)

    # Click Privacy Policy pop-up
    driver.implicitly_wait(10)
    print(driver.window_handles)
    consentButton = driver.find_elements(By.CLASS_NAME, "hcl-button.hcl-button--primary")
    # Debug & change the index below if clicking fails    
    consentButton[5].click()

    return driver


def getAllApartmentsInPage(driver):

    # Get all listings-objects on page
    apListings = driver.find_elements(By.CSS_SELECTOR,
        ".sold-property-listing")

    apDate, apAdress, apSize, apRooms, apBroker, apRent, apPrice = [], [], [], [], [], [], []

    for i, listing in enumerate(apListings):

        # SaleDate
        date = listing.find_elements(By.CSS_SELECTOR,
            ".sold-property-listing__sold-date")
        apDate.append('Unknown') if len(
            date) == 0 else apDate.append(date[0].text.replace('Såld ', '').strip())

        # Adress
        adress = listing.find_elements(By.CSS_SELECTOR,
            ".sold-property-listing__heading")
        apAdress.append('Unknown') if len(
            adress) == 0 else apAdress.append(adress[0].text.strip())

        # Size & Rooms
        both = listing.find_elements(By.CSS_SELECTOR,
            ".sold-property-listing__subheading")
        both = both[0].text.split('  ')
        size = both[0][:-3]

        # If rooms field wasn't found
        if both[1]:
            room = both[1][1].replace(' rum', '')
        else:
            room = 'Unknown'

        apSize.append('Unknown') if len(
            size) == 0 else apSize.append(size)
        apRooms.append('Unknown') if len(
            room) == 0 else apRooms.append(room)

        # Realtor
        broker = listing.find_elements(By.CSS_SELECTOR,
            ".sold-property-listing__broker-name")
        apBroker.append('Unknown') if len(
            broker) == 0 else apBroker.append(broker[0].text.strip())

        # Rent
        rent = listing.find_elements(By.CSS_SELECTOR,
            ".sold-property-listing__fee")
        apRent.append('Unknown') if len(
            rent) == 0 else apRent.append(rent[0].text.replace(' kr/mån', '').replace(' ', ''))

        # Price
        price = listing.find_elements(By.CSS_SELECTOR,
            ".sold-property-listing__subheading")
        # price = price[0].text.split('\n')[0]
        if len(price) == 0 or len(price) == 1:
            apPrice.append('Unknown')
        else:
            apPrice.append(price[1].text.replace(
                'Slutpris ', '').replace('kr', '').replace(' ', ''))

    totalData = [apDate, apAdress,
                 apSize, apRooms, apBroker, apRent, apPrice]

    print(totalData)
    totalDataFrame = createDataframe(totalData)
    
    # Save the data temporarily for in case of crashes
    pageData = pd.DataFrame()
    pageData = pageData.append(totalDataFrame, ignore_index=True)
    pageData.to_csv('./Data/tmpData.csv', mode='a', index=False)
    
    return totalDataFrame


def getMultiplePages(driver, numberOfPages):
    apD = pd.DataFrame()
    for i in range(0, numberOfPages):

        # Get all aprtments at this page
        newApData = getAllApartmentsInPage(driver)

        apD = apD.append(newApData, ignore_index=True)

        # Scroll to bottom till pagination button is visible
        if check_exists_by_xpath(driver, "//a[contains(text(), 'Nästa')]"):
            element = driver.find_element(By.XPATH, "//a[contains(text(), 'Nästa')]")
            driver.execute_script('arguments[0].scrollIntoView();', element)
            driver.execute_script('window.scrollBy(0, -200);')
            print(i)
            # Click Next Page Button
            nextButton = driver.find_elements(By.CSS_SELECTOR,
                ".next_page")
            nextButton[0].click()
        else:
            print('No next page!')
            break        

    return apD


def createDataframe(apColumns):

    apColumns = {
        'Date': apColumns[0],
        'Adress': apColumns[1],
        'Size': apColumns[2],
        'Rooms': apColumns[3],
        'Broker': apColumns[4],
        'Rent': apColumns[5],
        'Price': apColumns[6],
    }

    apDf = pd.DataFrame(data=apColumns)

    return apDf

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True