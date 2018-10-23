'''
## REQUESTS: 
-------------
- post: r = requests.post('https://httpbin.org/post', data = {'key1': 'value1', 'key2': ['value2', 'value3']})
- get: requests.get('https://github.com/', timeout=0.001)
- r.status_code or r.raise_for_status() 
- Url w/ params: print(r.url)
- print http resp: print(r.text) or r.content
- get/set encoding: r.encoding
- r = requests.get(url, headers={'user-agent': 'my-app/0.0.1'}, auth= {})

--

DECODING: 
- Create an image from binary data returned by a request: 
from PIL import Image
from io import BytesIO
i = Image.open(BytesIO(r.content))
- r.json()


### BeautifulSoup - Navigating html 
------------------------------------
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

## Selenium:
-------------
# Element interaction: 
        browser.find_element_by_partial_link_text('.txt')
        browser.find_element_by_id('searchbox').clear()

# Browser Nav: 
   Navigating Frames:
        browser.switch_to_frame(By.id('mainFrame'))
        Switch to default frame: browser.switch_to_default_content()
        Switch to 1st frame: browser.switch_to_frame('mainFrame.0.child')
        Find xpath containing: 
           dyn_frame = browser.find_element_by_xpath(
                   '//frame[contains(@name, "fr_resultsNav")]' )
                   # framename = dyn_frame[0].get_attribute('name')
# Window Nav: 
        Switch window to the handle of the 2nd window opened: 
           browser.switch_to_window(browser.window_handles[1]) 

# Waiting: 
----------
- Wait: driver.implicitly_wait(10)
        time.sleep(random.random() * max_seconds)
- Wait until:
```
driver = webdriver.Firefox()
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(
        expected_condtions.presence_of_element_located((By.ID, "myDynamicElement"))
    )
except TimeoutException, NoSuchElementException, NoSuchFrameException:
finally:
    driver.quit()
```
# Locating - https://selenium-python.readthedocs.io/locating-elements.html
---------------------------------------------------------------------------
- EC.element_to_be_located((By.CSS_SELECTOR, 'img[alt=\"Some Button\"]'))

# Downloading files with selenium (experimental, likely won't work):
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': '/Users/yourname/Desktop/LexisNexis_results/'}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options = chrome_options)
or use
os.system('wget {}'.format(results_url)) w/ wget

# Second Level Scrape
Selenium hands of the source of the specific job page to Beautiful Soup
soup_level2=BeautifulSoup(driver.page_source, 'lxml')

************* OTHER *************

# Check attributes of a web element
element = browser.find_elements( X )[0]
for i in browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element):
        print(i)


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

Debugging:
----------
# setting up a log: 
- Put this in beginning and write to it each time exception is thrown
path_to_log = '/Users/yourname/Desktop/'
log_errors = open(path_to_log + 'log_errors.txt', mode = 'w')

'''
# encoding: utf-8
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import requests
import pandas as pd
import re as regex
import clipboard as cb
import time

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

#Lists headings and p's, then all frame names, then all links, then all div names  
def htmlRunDown(self, url):
        # Just start off in uname, tab to password -- Or try parent child movement
        browser = getBrowserDriver(url)

        print(f"+ First frame Switch ({browser.find_element_by_tag_name('iframe').get_attribute('id')}): ")
        print(f"Inputs at Load: {[frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')]}")
        WebDriverWait(browser, 25).until(EC.frame_to_be_available_and_switch_to_it((0)))

        print([frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')])
        # AS of Now output here is gsft_main - ['sysparm_ck', 'user_name', 'user_password', ...
        # Still times out tho - doubling up on Web waits works as well as one switchTo(0) with a webWait


        print(f"iFrames #: {len(browser.find_elements_by_tag_name('iframe'))}")
        print(f"inputs #: {len(browser.find_elements_by_tag_name('input'))}")

        print(f"\n+ Second frame Switch:  ")
        WebDriverWait(browser, 25).until(EC.frame_to_be_available_and_switch_to_it((0)))
        print([frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')])
        print(browser.find_element_by_tag_name('iframe').get_attribute('id'))
        print(browser.find_element_by_tag_name('div').get_attribute('id'))

        browser.close  

class ServiceNowCrawler:
        def _init_(self):
                # Target takes to login then to target page
                nonlocal target_url = 'https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task.do%3Fsys_id%3Ddfed669047801200e0ef563dbb9a712b%26sysparm_view%3Dmy_request%26sysparm_record_target%3Dsc_task%26sysparm_record_row%3D1%26sysparm_record_rows%3D1%26sysparm_record_list%3Drequest_item%253Daeed229047801200e0ef563dbb9a71c2%255EORDERBYDESCnumber'
                nonlocal BROWSER_TIMEOUT = 45 # seconds
                nonlocal buffer_wait = 2 # Seconds
                
                nonlocal USER_NAME="admin"
                nonlocal USER_PASSWORD= 'Veryhap1*'
                
                nonlocal browser= exec_Prefs(webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe'))
                start_tasks_crawl()

        def exec_Prefs(self, driver):
                # driver.manage().window().setSize(new Dimension(100,100))
                # driver.manage().window().setPosition(new Point(0,200))
                return driver

        def exists_by_id(self, id):
                try:
                        browser.find_element_by_id(id)
                except NoSuchElementException:
                        return False
                return True

        def start_tasks_crawl(self):
                login_ServiceNow()
                scrape_Task()
                browser.close

        # Open and scrape Activities in Catalog Tasks
        def login_ServiceNow(self, url=target_url):
                time.sleep(buffer_wait)
                
                print(f"Inputs at Load: {[frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')]}")
                WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it((0)))
                print(f"Inputs at Switch: {[frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')]}")
                time.sleep(buffer_wait)
                print(f"Inputs after timed wait: {[frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')]}")
                
                (browser.find_element_by_name("user_name")).send_keys(USER_NAME)
                (browser.find_element_by_id("user_password")).send_keys(USER_PASSWORD + Keys.RETURN)

        def scrape_Task(self):
                # Just making sure html matches what i am seeing
                time.sleep(buffer_wait)
                soup = BeautifulSoup(browser.page_source, features="html.parser")
                writeHtmlToFile(soup.prettify, task, overwriteFile=True)
                inputs = soup.find_all('input')
                tables = soup.find_all('table')
                print(len(inputs), len(table))
                col = soup.findAll('ul')
                print(f"Table Column 0: {len(col)}")
                rows = soup.findChildren()
                print(len(rows))
                for i in rows: 
                        print(i)
                        print(i.content)
                


    

ServiceNowCrawler()
'''
s = getHtml("https://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python")
r = getHtml("http://www.storybench.org/how-to-scrape-reddit-with-python/")
soup = getHtml('https://dev58662.service-now.com/pm')
openBrowser('https://dev58662.service-now.com/pm')

'''