from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pandas as pd
import numpy as np

import time


def initCrawler():

    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=options,
                              executable_path="/Users/gustafvh/Heavy Learning/Machine Learning/Stockholm Apartments/Application/chromedriver")

    url = "https://www.hemnet.se/salda/bostader?housing_form_groups%5B%5D=apartments&location_ids%5B%5D=18031&page=1"
    driver.get(url)

    # Click Privacy Policy pop-up
    consentButton = driver.find_elements_by_css_selector(
        ".consent-modal__button")

    consentButton[0].click()

    return driver


def getAllApartmentsInPage(driver):

    # Get all listings-objects on page
    apListings = driver.find_elements_by_css_selector(
        ".sold-property-listing")

    apDate, apAdress, apSize, apRooms, apBroker, apRent, apPrice = [], [], [], [], [], [], []

    for i, listing in enumerate(apListings):

        # SaleDate
        date = listing.find_elements_by_css_selector(
            ".sold-property-listing__sold-date")
        apDate.append('Unknown') if len(
            date) == 0 else apDate.append(date[0].text.replace('Såld ', '').strip())

        # Adress
        adress = listing.find_elements_by_css_selector(
            ".item-result-meta-attribute-is-bold")
        apAdress.append('Unknown') if len(
            adress) == 0 else apAdress.append(adress[0].text.strip())

        # Size & Rooms
        both = listing.find_elements_by_css_selector(
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
        broker = listing.find_elements_by_css_selector(
            ".sold-property-listing__broker")
        apBroker.append('Unknown') if len(
            broker) == 0 else apBroker.append(broker[0].text.strip())

        # Rent
        rent = listing.find_elements_by_css_selector(
            ".sold-property-listing__fee")
        apRent.append('Unknown') if len(
            rent) == 0 else apRent.append(rent[0].text.replace(' kr/mån', '').replace(' ', ''))

        # Price
        price = listing.find_elements_by_css_selector(
            ".sold-property-listing__subheading")
        # price = price[0].text.split('\n')[0]
        if len(price) == 0 or len(price) == 1:
            apPrice.append('Unknown')
        else:
            apPrice.append(price[1].text.replace(
                'Slutpris ', '').replace('kr', '').replace(' ', ''))

    totalData = [apDate, apAdress,
                 apSize, apRooms, apBroker, apRent, apPrice]

    totalDataFrame = createDataframe(totalData)

    return totalDataFrame


def getMultiplePages(driver, numberOfPages):
    apD = pd.DataFrame()
    for i in range(0, numberOfPages):

        # Get all aprtments at this page
        newApData = getAllApartmentsInPage(driver)

        apD = apD.append(newApData, ignore_index=True)

        # Scroll to bottom of page
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Click Next Page Button
        nextButton = driver.find_elements_by_css_selector(
            ".next_page")
        nextButton[0].click()

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
