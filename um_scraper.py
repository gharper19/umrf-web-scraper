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

Getting Links: 
redditAll = soup.find_all("a")
for links in soup.find_all('a'):
    print (links.get('href'))

Browser Nav:
navigate().back()

#Selenium visits each Job Title page
    python_button = driver.find_element_by_id('MainContent_uxLevel2_JobTitles_uxJobTitleBtn_' + str(x))
    python_button.click() #click link
    
    #Selenium hands of the source of the specific job page to Beautiful Soup
    soup_level2=BeautifulSoup(driver.page_source, 'lxml')

'''

from bs4 import BeautifulSoup
import requests
import clipboard as cb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re as regex

def getHtml(url):
        #can also get as JSON instead of text
        return BeautifulSoup((requests.get(url)).text, features="html.parser").prettify()
    
def openBrowserSearchBox(url=None):
        browser = webdriver.Edge()
        if not(url==None):
                browser.get(url)
                return
        browser.get('http://www.youtube.com')
        assert 'Youtube' in browser.title
        elem = browser.find_element_by_name('p') 
        elem.send_keys('stock prices' + Keys.RETURN)
        browser.quit()

def openBrowser(url):
        browser = webdriver.Edge()
        browser.get(url)
        browser.
        elem = browser.find_element_by_name('q') 
        elem.send_keys('stock prices' + Keys.RETURN)


x = 0 
data = []

soup = getHtml('https://dev58662.service-now.com/pm')
openBrowser('https://dev58662.service-now.com/pm')

'''
s = getHtml("https://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python")
r = getHtml("http://www.storybench.org/how-to-scrape-reddit-with-python/")
'''