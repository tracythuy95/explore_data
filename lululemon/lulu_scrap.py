from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import csv
import json
import numpy as np
import seaborn as sns

driver = webdriver.Chrome('/Users/tracynguyen/Applications/chromedriver')
# url = 'https://shop.lululemon.com/c/women/_/N-7vf'
url = 'https://shop.lululemon.com/c/women-maintops/_/N-815'

driver.get(url)  # open WMTM page
i = 0
while True:
    try:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight + 1000);')  
        time.sleep(15)  
        button = driver.find_element_by_xpath("//span[text()='View more products']")
        actions = ActionChains(driver)
        actions.move_to_element(button).perform()  # move button into view
        button.click()  
    
    except NoSuchElementException:  # all products loaded
        break


product_urls = [(i.get_attribute('href')).split("?", 1)[0] for i in driver.find_elements_by_xpath('.//div[@class="product-tile"]//a')]
product_urls = list(dict.fromkeys(product_urls))
product_urls

product_name = [ urllib.parse.unquote(json.loads(i.get_attribute('data-lulu-attributes'))['product']['name']) for i in driver.find_elements_by_xpath('.//h3[@class="product-tile__product-name lll-text-body-1"]//a')]
product_name

def main():

    ## loop through list of urls to do
    ## get list of product urls from a page
    ## get list of product names from a page

    


    # initialize dataframe
    df  = pd.DataFrame(columns = ['Category', 'Item Category', 'Display Name', 'Color', 'URL', 'Sale Price', 'Original Price', 'Sizes In Stock', 'Sizes OOS'] )

    womens = scraper_to_df('Women')
    df = df.append(womens)
    mens = scraper_to_df('Men')
    df = df.append(mens)
    df.to_csv('luluwmtm.csv',index=False,header=True)

    # writes to google drive sheet, comment out the rest if running locally
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('lulu-wmtm-scraper')

    with open('luluwmtm.csv', 'r', encoding='utf-8') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content.encode('utf-8'))


if __name__=="__main__":
    main()