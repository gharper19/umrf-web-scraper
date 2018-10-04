'''
Navigating html 
---------------
Going down
        Navigating using tag names
        .contents and .children
        .descendants
        .string
        .strings and stripped_strings

Going up
        .parent
        .parents

Going sideways
        .next_sibling and .previous_sibling
        .next_siblings and .previous_siblings

Going back and forth
        .next_element and .previous_element
        .next_elements and .previous_elements

Selenium Browser Nav:
        navigate().back()

Getting Links: 
        redditAll = soup.find_all("a")
        for links in soup.find_all('a'):
                print (links.get('href'))

Wait until:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(
        expected_condtions.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()

# Second Level Scrape
---------------------
Selenium visits each Job Title page
    python_button = driver.find_element_by_id('MainContent_uxLevel2_JobTitles_uxJobTitleBtn_' + str(x))
    python_button.click() #click link
    
    #Selenium hands of the source of the specific job page to Beautiful Soup
    soup_level2=BeautifulSoup(driver.page_source, 'lxml')

# FileWriter
------------
The read functions contains different methods,
# read() return one big string readline
# readline() return one line at a time readlines
# readlines() returns a list of lines

This method writes a sequence of strings to the file. write ()
#Used to write a fixed sequence of characters to a file writelines()
#writelines can write a list of strings

import os.path
save_path = 'C:/example/'
name_of_file = raw_input("What is the name of the file: ")
completeName = os.path.join(save_path, name_of_file+".txt") 

'''

from bs4 import BeautifulSoup
import requests
import clipboard as cb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import pandas as pd
import re as regex

def getSoup(url):
        return BeautifulSoup((requests.get(url)).text, features="html.parser")

def getHtml(url):
        #can also get as JSON instead of text
        return getSoup(url).prettify()

def getBrowserDriver(url=None):
        driver =webdriver.Chrome()
        if not(url==None): driver.get(url)
        return driver

def writeHtmlToFile(html, name, ext="html", overwriteFile=False):
        file = "./html/" + str(name) + '.' + str(ext)
        try:
                if overwriteFile:
                        f=open(file, 'w')
                        f.write(html) 
                        f.close()
                else:
                        f=open(file, 'a') 
                        f.write(html)
                        f.close()
        except FileNotFoundError:
                f=open(file, 'w+') 
                f.write(html)
                f.close()

def drillDownWikipedia(topic):
        url ='https://www.wikipedia.org/'
        soup = getSoup(url)
        browser = getBrowserDriver(url)
        
        # Enter into Search 
        try: 
                searchBox = (browser).find_element_by_id('searchInput')
                searchBox.send_keys(topic + Keys.RETURN)
                holup = WebDriverWait(browser, 2)  
                
                # give html source back to BS and parse list of divs
                soup = BeautifulSoup(browser.page_source, features="html.parser")
                for i in soup.find_all('div'):
                        print(i)
        except WebDriverException:
                print('Error Clicking on stuff')
        finally:
                browser.close()

def drillDownServiceNow(topic=None):
        url = 'https://dev58662.service-now.com/'
        soup = getSoup(url)
        browser = getBrowserDriver(url)
        print(soup.getHtml().prettify())

MAX_PAGES = 100 #include stopper  

pages_visited = [] 
numPages = 0

drillDownServiceNow()
'''
s = getHtml("https://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python")
r = getHtml("http://www.storybench.org/how-to-scrape-reddit-with-python/")
soup = getHtml('https://dev58662.service-now.com/pm')
openBrowser('https://dev58662.service-now.com/pm')
'''