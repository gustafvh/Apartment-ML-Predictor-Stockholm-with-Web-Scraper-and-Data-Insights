from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from CreateData import createDataframe

import pandas as pd

import time


options = Options()
options.add_argument("--incognito")
options.add_argument("--window-size=1920x1080")


driver = webdriver.Chrome(options=options,
                          executable_path="/Users/gustafvh/Heavy Learning/Machine Learning/Stockholm Apartments/Application/Web Crawler/chromedriver")


url = "https://www.hemnet.se/salda/bostader?housing_form_groups%5B%5D=apartments&location_ids%5B%5D=18031"
driver.get(url)

# Click Privacy Policy pop-up
consentButton = driver.find_elements_by_css_selector(
    ".consent-modal__button")

consentButton[0].click()


def getAllApartmentsInPage(driver):

    # Adresses
    apAdress = driver.find_elements_by_css_selector(
        ".item-result-meta-attribute-is-bold")
    apAdress = [adress.text for adress in apAdress]

    # Prices, Size, Rooms
    apPSR = driver.find_elements_by_css_selector(
        ".sold-property-listing__subheading")
    apPSR = [price.text for price in apPSR]

    apPrice = apPSR[1::2]

    apSR = apPSR[::2]

    apSize = []
    apRooms = []

    # '54 m  2 rum' --> [54 m, 2 rum]
    for el in apSR:
        both = el.split('  ')
        both[0] = both[0].strip()
        both[1] = both[1].strip()
        apSize.append(both[0])
        apRooms.append(both[1])

    for i, price in enumerate(apPrice):
        apPrice[i] = price.replace('Slutpris ', '').replace(
            'kr', '').replace(' ', '')

    for i, rooms in enumerate(apRooms):
        apRooms[i] = rooms.strip().replace(' rum', '')

    for i, size in enumerate(apSize):
        apSize[i] = size[:-3]

    # Rent
    apRent = driver.find_elements_by_css_selector(
        ".sold-property-listing__fee")
    apRent = [rent.text for rent in apRent]

    for i, rent in enumerate(apRent):
        apRent[i] = rent.replace(' kr/mån', '').replace(' ', '')

    # SaleDate
    apDate = driver.find_elements_by_css_selector(
        ".sold-property-listing__sold-date")
    apDate = [date.text for date in apDate]

    for i, date in enumerate(apDate):
        apDate[i] = date.replace('Såld ', '')

    # Realtor
    apBroker = driver.find_elements_by_css_selector(
        ".sold-property-listing__broker")
    apBroker = [broker.text for broker in apBroker]

    for i, broker in enumerate(apBroker):
        apBroker[i] = broker.strip()

    totalData = [apDate, apAdress,
                 apSize, apRooms, apBroker, apRent, apPrice]

    totalDataFrame = createDataframe(totalData)

    return totalDataFrame


apData = pd.DataFrame()

for i in range(0, 3):

    # Get all aprtments at this page
    newApData = getAllApartmentsInPage(driver)

    print(newApData.info())

    apData.append(newApData)

    # Scroll to bottom of page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Click Next Page Button
    nextButton = driver.find_elements_by_css_selector(
        ".next_page")
    nextButton[0].click()


print(apData.info())
