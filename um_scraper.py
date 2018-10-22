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

USER_NAME="admin"
USER_PASSWORD= 'Veryhap1*'

def getSoup(url):
        return BeautifulSoup((requests.get(url)).text, features="html.parser")

def getHtml(url):
        #can also get as JSON instead of text
        return getSoup(url).prettify()

def getBrowserDriver(url=None):
        driver_path = '.\\web_drivers\\chromedriver.exe'
        driver =webdriver.Chrome(executable_path=driver_path)
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

def exists_by_id(id):
    try:
        browser.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

#Lists headings and p's, then all frame names, then all links, then all div names  
def htmlRunDown(url):
        pass
        # browser = getBrowserDriver(url='https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task.do%3Fsys_id%3Ddfed669047801200e0ef563dbb9a712b%26sysparm_view%3Dmy_request%26sysparm_record_target%3Dsc_task%26sysparm_record_row%3D1%26sysparm_record_rows%3D1%26sysparm_record_list%3Drequest_item%253Daeed229047801200e0ef563dbb9a71c2%255EORDERBYDESCnumber')
        # print(f" >>> Before frame Switch:  \niFrame name: {(browser.find_elements_by_tag_name('iframe'))[0].title}")
        # print(f"iFrames: {len(browser.find_elements_by_tag_name('iframe'))}")
        # print(f"inputs: {len(browser.find_elements_by_tag_name('input'))}")
                
        # WebDriverWait(browser, 25).until(EC.frame_to_be_available_and_switch_to_it(
        #                 (0)))
        # # WebDriverWait(browser, 25).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'gsft_main')))
        
        # # browser.switch_to.frame('gsft_main')
        # try:
        #         # Notice wait is a bool , and there is only one iframe, auto switches to iframe
        #         # and there are no reg frames
                
        #         p = browser.find_elements_by_id('loginPage')

        #         print(f" >>> After frame[0] Switch:  \nFrames: {len(browser.find_elements_by_tag_name('frame'))}")        
        #         print(f"iFrames now: {len(browser.find_elements_by_tag_name('iframe'))}")
                
        #         l = browser.find_elements_by_tag_name('input')
        #         print(f"inputs: {len(l)}")
        #         print("   Attr: ")
        #         element = l[0]
        #         for i in browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element):
        #                 print(i)
        #         for i in range(0, len(l)): 
        #                 print(f"  Input {i}: {l[i].id}") 

        #         d= browser.find_elements_by_tag_name('div')
        #         element = d[0]
        #         for i in browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element):
        #                 print(i)
        #         print(f"Divs: {len(d)}")
        #         for i in range(0, len(d)):
        #                 print(f"  Div {i}: {d[i].title}")

        #         #try switching to login form
                
        # except Exception:
        #         print("-------------------- Error thrown --------------------")
        # finally:
        #         try:
        #                 # print("U box located")
        #                 (browser.find_element_by_name("user_name")).send_keys(USERNAME)
        #                 (browser.find_element_by_id("user_password")).send_keys(USER_PASSWORD + Keys.RETURN)
        #         except Exception:
        #                 print("-------------------- Couldnt add Text --------------------")
        #         finally:
        #                 browser.close()

# Open and scrape Activities in Catalog Tasks
def find_Catalog_Tasks():
        # Just start off in uname, tab to password -- Or try parent child movement
        browser = getBrowserDriver(url='https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task.do%3Fsys_id%3Ddfed669047801200e0ef563dbb9a712b%26sysparm_view%3Dmy_request%26sysparm_record_target%3Dsc_task%26sysparm_record_row%3D1%26sysparm_record_rows%3D1%26sysparm_record_list%3Drequest_item%253Daeed229047801200e0ef563dbb9a71c2%255EORDERBYDESCnumber')

        print(f" >>> Before frame Switch:  ")  #\niFrame name: {(browser.find_elements_by_tag_name('iframe'))[0].id}")
        frame_names = [frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('iframe')]
        browser.switch_to_frame(0)
        input_names = [frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')]
        
        print(f"Frame Names: {frame_names}")
        print(f"Input Names: {input_names}")
        print(f"iFrames #: {len(browser.find_elements_by_tag_name('iframe'))}")
        print(f"inputs #: {len(browser.find_elements_by_tag_name('input'))}")
                
        WebDriverWait(browser, 25).until(EC.frame_to_be_available_and_switch_to_it(
                        (0)))
        # WebDriverWait(browser, 25).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'gsft_main')))
        
        # browser.switch_to.frame('gsft_main')
        try:
                # Notice wait is a bool , and there is only one iframe, auto switches to iframe
                # and there are no reg frames
                

        # OKAY, SO ID Changes each time so use page layout to find web elements OOOR 
        # see if you can select web elements using attributes OOR
        # See if its the browser?

                p = browser.find_elements_by_id('loginPage')
                print(f"Form id: {p.__getattribute__}\n")

                print(f" >>> After frame[0] Switch:  \nFrames: {len(browser.find_elements_by_tag_name('frame'))}")        
                print(f"iFrames now: {len(browser.find_elements_by_tag_name('iframe'))}")
                
                l = browser.find_elements_by_tag_name('input')
                print(f"inputs: {len(l)}")
                print("   Attr: ")
                element = l[0]
                input_names = [frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')]
                print(f"Input Names: {input_names}")

                d= browser.find_elements_by_tag_name('div')
                div_names = [frame.get_attribute('id') for frame in browser.find_elements_by_tag_name('input')]
                print(f"Div Names: {div_names}")
                #try switching to login form
                
        except Exception:
                print("-------------------- Error thrown --------------------")
        finally:
                try:
                        # print("U box located")
                        (browser.find_element_by_name("user_name")).send_keys(USERNAME)
                        (browser.find_element_by_id("user_password")).send_keys(USER_PASSWORD + Keys.RETURN)
                except Exception:
                        print("-------------------- Couldnt add Text --------------------")
                finally:
                        browser.close()
        
        # try: 
        #         wait.until(EC.frame_to_be_available_and_switch_to_it(By.ID('gsft_main')))
        #         print("frame located")
        #         # uname = wait.until(EC.presence_of_element_located(
        #         #         (By.XPATH, '//*[@id="user_name"]')))
        #         # 
        #         # pword = wait.until(EC.presence_of_element_located(
        #         #         (By.XPATH, '//*[@id="user_password"]')))
        #         # print("Pass located")
        # except Exception:
        #         print("EC Timeout - Can't find web elements. ")
        #         browser.close()
        # # Service Now Login 
        # try:
        #         wait = WebDriverWait(browser, 30)
        #         wait.until(EC.visibility_of_element_located(By.XPATH('//*[@id="user_name"]')))
        #         # browser.switch_to.frame('gsft-main')              
        #         # print('swtitched to gsft-main')  
        #         # browser.switch_to_active_element('loginPage')
        #         # print('swtitched to loginPage')

        #         (browser.find_element_by_xpath('//*[@id="user_name"]')).send_keys(USERNAME)
        #         print('Added uname')
        #         (browser.find_element_by_xpath('//*[@id="user_password"]')).send_keys(USER_PASSWORD, Keys.RETURN)
        #         print('Added pword')
        #         # Parse html
        #         soup = BeautifulSoup(browser.page_source, features='html.parser')

        # finally: 
        #         browser.close()

MAX_PAGES = 100 #include stopper  
ALLOWED_DOMAINS =[]

pages_visited = [] 
numPages = 0

find_Catalog_Tasks()
'''
s = getHtml("https://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python")
r = getHtml("http://www.storybench.org/how-to-scrape-reddit-with-python/")
soup = getHtml('https://dev58662.service-now.com/pm')
openBrowser('https://dev58662.service-now.com/pm')

'''