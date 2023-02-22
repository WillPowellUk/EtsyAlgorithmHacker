# details from https://github.com/SeleniumHQ/docker-selenium/tree/selenium-3 

# Release
# docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome:3.141.59-20210929

# Debug: VNC on 127.0.0.1:5900 
# docker run -d -p 4444:4444 -p 5900:5900 --shm-size=2g selenium/standalone-chrome-debug:3.141.59-20210929

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

class Webscrape:
    def __init__(self, websiteURL, option=''):
        options = Options()
        options.add_argument('–ignore-ssl-errors=yes')
        options.add_argument('–ignore-certificate-errors')
        if option != 'debug':
            options.add_argument('--headless')
        self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
        self.driver.get(websiteURL)
        self.websiteURL = websiteURL

    def rotateProxy(self):
        pass

    def checkPage(self, keyword):
        self.driver.get(self.websiteURL)
        sourceText = self.driver.page_source
        return (keyword.lower() in sourceText.lower())

if __name__=="__main__":

    # create new driver
    web = Webscrape('https://www.etsy.com/uk/','debug')

    # accept cookies
    web.driver.find_element(By.XPATH, '//*[@id="gdpr-single-choice-overlay"]/div/div[2]/div[2]/button').click() 

    # search for key word
    searchBar = web.driver.find_element(By.XPATH, '//*[@id="global-enhancements-search-query"]')
    searchBar.click()
    searchBar.send_keys("Grinder")
    searchBar.send_keys(Keys.RETURN)

    # filter 
    web.driver.find_element(By.XPATH, '//*[@id="search-filter-button"]').click()
    web.driver.get('https://www.etsy.com/search?q=grinder&explicit=1&min=7.99&max=7.99&ship_to=GB')
    
    # wait for page to load, then select listing containing 'Biscuit Herb'
    web.driver.find_element(By.XPATH, "//*[contains(text(), 'Biscuit Herb')]").click()
    
    # add to favourites using listing id 1401070274
    # web.driver.find_element(By.CSS_SELECTOR, "button[data-listing-id='1401070274']").click()
        
    # wait for the dropdown to become visible
    # dropdown = WebDriverWait(web.driver, 10).until(EC.visibility_of_element_located((By.ID, "variation-selector-0")))

    # create a Select object for the dropdown
    # select = Select(dropdown)

    # select an option by its text
    # select.select_by_visible_text("Black")

    # select colour (option is black (3247764331))
    # web.driver.find_element(By.ID, "variation-selector-0").click()
    # web.driver.find_element(By.CSS_SELECTOR, "option[value='3247764331']").click()

    # add to basket
    WebDriverWait(web.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-selector="add-to-cart-button"] button[type="submit"]'))).click()
