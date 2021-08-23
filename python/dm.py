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
options.add_argument("--headless")  # Runs Chrome in headless mode.
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized')  #
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

url = "https://www.dm.hu/markak"
driver = webdriver.Chrome(chrome_options=options,
                           executable_path='C:/Users/mgranat/Downloads/chromedriver_win32/chromedriver.exe')
# driver = webdriver.Chrome(executable_path='C:/Users/mgranat/Downloads/chromedriver_win32/chromedriver.exe')

letters = list()
letters.append('Zahlen')

for letter in string.ascii_uppercase:
    letters.append(letter)

df_total = pd.DataFrame()

for letter in letters:
    i = 1
    while True:
        driver.get(url)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Zahlen"]/div/div/div/ul/li[1]/a')))
        time.sleep(1)
        try:
            xpath = '//*[@id="' + letter + '"]/div/div/div/ul/li[' + str(i) + ']/a'
            button = driver.find_element_by_xpath(xpath)
        except:
            break
        print(button.text)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        chwd = driver.window_handles
        if len(chwd) > 1:
            driver.switch_to.window(chwd[1])
            url_brand = driver.current_url
            driver.switch_to.window(chwd[0])
            driver.close()
            driver.switch_to.window(chwd[1])
        else:
            url_brand = driver.current_url
        try:
            button_spam = driver.find_element_by_xpath('//*[@id="cookiebar-ok"]')
            driver.execute_script("arguments[0].click();", button_spam)
        except:
            print('')
        button_click = 0
        add_total = True
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dz span')))
        except:
            reload_attempt = True
            reload_attempt_number = 1
            while reload_attempt:
                print('ONE MORE TRY: ', url_brand)
                try:
                    driver.get(url_brand)
                    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dz span')))
                    reload_attempt = False
                except:
                    print('Failed for #' + str(reload_attempt_number) + ' try :(')
                    reload_attempt_number += 1
                if reload_attempt_number >= 3:
                    reload_attempt = False
                    print(url_brand, " - NO PRODUCT !!!")
                    add_total = False
        if add_total:
            time.sleep(1)
            while True:  # load more product on the page if possible
                try:
                    more_button = driver.find_element_by_xpath('//*[@id="load-more-products-button"]')
                    driver.execute_script("arguments[0].click();", more_button)
                    button_click += 1
                    time.sleep(1)
                except:
                    break
            print('CLICK: ', button_click)
            time.sleep(1)
            products = driver.find_elements_by_css_selector('.dz span')
            products = [product.text for product in products]
            print(products)
            # TODO: find url

            prices = driver.find_elements_by_xpath("//*[@data-dmid='price-localized']")
            prices = [price.text for price in prices]
            prices = [price for price in prices if price.__contains__(' Ft')]

            try:
                df = pd.DataFrame({'product': products, 'price': prices})
                df['brand'] = url_brand
                print(df)
                df_total = df_total.append(df)
            except:
                print("Some bug... :( ---", url_brand)

        i += 1

print(df_total)

df_total.to_csv('c:/rprojects/drugstores/data/dm_product_data_' + str(date.today()) + '.csv')
driver.quit()
