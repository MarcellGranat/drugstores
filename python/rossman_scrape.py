import bs4
import string
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import string
import time
import requests
from datetime import date
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import warnings
warnings.filterwarnings("ignore")

options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') #
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

url = 'https://shop.rossmann.hu/'
# driver = webdriver.Chrome(chrome_options=options, executable_path='C:/Users/mgranat/Downloads/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(executable_path='C:/Users/mgranat/Downloads/chromedriver_win32/chromedriver.exe')

links = list()

for i in range(1, 14):
    driver.get(url)
    time.sleep(1)
    button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "skip-nav", " " ))]')
    time.sleep(.2)
    button.click()
    xpath = '//*[@id="nav"]/ol/li[' + str(i) + ']/a'
    print(xpath)
    button = driver.find_element_by_xpath(xpath)
    button.click()
    time.sleep(.2)
    links.append(driver.current_url)

df = pd.DataFrame({'links': links})
df.to_csv('c:/pyprojects/dm/data/rm_links_to_brands' + str(date.today()) + '.csv')

driver.quit()
