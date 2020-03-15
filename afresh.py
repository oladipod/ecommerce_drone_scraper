import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import bs4 as bs
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import mysql.connector
from mysql.connector import (connection)

class Scraper:
    def __init__(self,mainUrl:str):
        self.mainUrl = mainUrl
        self.csvInitialized = False
        self.filename = 'scraped.csv'
        self.products = []
        self.page = 1
        self.main_url_lists = [
            'https://www.bol.com/nl/l/boeken/N/8299/?promo=books-intl_360__A_29683-44295-alle-boeken_1_',
            
        ]
    

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='chromedriver')

    def dataBase(self):
        self.conn = connection.MySQLConnection(user='sql10326702', password='dAv2eCEWLb', host='sql10.freemysqlhosting.net', database='sql10326702')
        cursor = self.conn.cursor()
        sql = "CREATE database PRODUCTINFO";
CREATE TABLE table_name(product_url datatype, title datatype          
);
    cursor.execute(sql)
    

    def writeInfo():
        


        
        all_sql_tables = [...]
        sql_product = 

        #Closing the connection
        conn.close()

    
    def startScraping(self):
        self.setUp()
        self.browser.get(self.mainUrl)
        time.sleep(2)
         # add code - proceed if element is found within 3 seconds otherwise will raise TimeoutException 
        #nav_list = self.browser.find_elements_by_class_name('navigation-block__node  navigation-block__link')
        nav_list = self.browser.find_elements_by_class_name('navigation-block__link')
        print(nav_list) #wait, we got them?
        print(len(nav_list))
        
        links = []  
        for i in range(len(nav_list)):
            links.append(nav_list[i].get_attribute('href'))
        for link in links:
            print ('navigating to: ' + link)
            self.browser.get(link)

        #sub_link =     
           

            self.browser.back

    # do stuff within that page here...

        for nav_li in nav_list:
            ActionChains(self.browser).click(nav_li).perform()
            #product_list = 
            time.sleep(2)
            self.browser.back()
            
        
        
        self.tearDown()

    def tearDown(self):
        self.browser.close()

s = Scraper('https://www.bol.com/nl/?language=nl')
s.startScraping()

# page = requests.get("https://www.bol.com/nl/?language=nl")
# soup = BeautifulSoup(page.content, "html.parser")
