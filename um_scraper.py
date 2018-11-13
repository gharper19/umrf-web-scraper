'''

V3ryhap


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
General
        find_all_previous

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
CSS Selectors
        soup.select("p > a") : link directly under p

bs4 can also modify or prettify html

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

# Exclude tags from search - bs4
   for element in soup.find_all(text=True):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                pass

# Classes
---------
- when we changed the class element (static - outisde _init_), it changed for both objects.
But, changing the object element(inside init) does not

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

# Debugging:
-------------
# setting up a log:
- Put this in beginning and write to it each time exception is thrown
path_to_log = '/Users/yourname/Desktop/'
log_errors = open(path_to_log + 'log_errors.txt', mode = 'w') #Should use append, right, maybe also assigning log size threshold?


## Notes:
---------
Problems:
- Close request connection? - on reddCrawl too
- Check if input boxes are loaded as a JavaScript Post-Load
    - Use implicit timed waits and try to do it, then figure out why explicit wont work
    - Try different by (e.g. selector, xpath, inner html, index in collection of same tags)
        - Make use of bs4 to organize and understand html
        - Recall Aaron said some property of the tables in SN are different ea time

Moving Forward:
- Start from task lists and do for each task - https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task_list.do%3Fsysparm_userpref_module%3D59f8a2a60a0a0b9b00fd6bfe2e28ada5%26sysparm_query%3Dactive%3Dtrue%5EEQ%26sysparm_clear_stack%3Dtrue
- Can follow a direct link to catalog tasks or go through sidebar links by setting a checkbox in dash
- PARAMS: uname, password, target_url(Maybe w/ some webElement verification),
- Surround everything in try catch and surround try catch with do while counters

'''
# encoding: utf-8
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, NoSuchAttributeException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import lxml
import requests
import pandas as pd
import re
import clipboard as cb
import time

'''
TODO:
        1) Wrap in a class
        2) Write alg for getting task list and turn tasks into data objects:            # apachepoi
                - for task iteration: the data will already be in a table and a filter allows the user to specify the data thats provided,
                if its easier than drilling down with scrape_task, notify user of specified filter settings and go by that,
                otherwise just grab whatever you can while there b/c table data doesnt require page transition from selenium.
        3) Replace any timed waits with multiple web element based waits for selenium interactions, error handling
        4) wrap in Java Fx
'''
class Task:
        def __init__(self, name):
                pass

class TaskScraper:
        # Class Structure: 1) def function which will handle error checking and close browser and restart on error
        # Fill w/ params from GUI
        # Target takes to login then to target page
        task_url = 'https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task.do%3Fsys_id%3Ddfed669047801200e0ef563dbb9a712b%26sysparm_view%3Dmy_request%26sysparm_record_target%3Dsc_task%26sysparm_record_row%3D1%26sysparm_record_rows%3D1%26sysparm_record_list%3Drequest_item%253Daeed229047801200e0ef563dbb9a71c2%255EORDERBYDESCnumber'
        list_url= "https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task_list.do%3Fsysparm_clear_stack%3Dtrue%26sysparm_query%3Dactive%253Dtrue%255EEQ"
        buffer_wait = 2 # Seconds

        USER_NAME="admin"
        USER_PASSWORD= 'Veryhap1*'

        def __init__(self, url=task_url, browser=None):
                def exec_window_prefs(driver):
                        driver.set_window_position(0, 0)
                        driver.set_window_size(325, 250)
                        return driver
                # self.url= url
                self.browser= exec_window_prefs(webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe'))

        def exists_by_id(self, id):
                try:
                        self.browser.find_element_by_id(id)
                except NoSuchElementException:
                        return False
                return True

        # Start scraping loop        - Loop can either be main, in init or just here as a kickoff method
        def go_scrape(self, failed_start_threshold=5 ):
                BROWSER_TIMEOUT = 45 # seconds
                go = True
                failed_starts= 0
                while (go==True and failed_starts < failed_start_threshold ):
                        try:
                                # Try to start task crawl
                                t = time.time()
                                self.browser.set_page_load_timeout(20)
                                self.browser.get(self.list_url)
                                print('Time consuming: ', time.time() - t)

                                ## Log in to SN using credintials
                                time.sleep(self.buffer_wait)
                                WebDriverWait(self.browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it((0)))

                                # Change to wait until uname and password appear - should fix random errors
                                time.sleep(self.buffer_wait)
                                (self.browser.find_element_by_name("user_name")).send_keys(self.USER_NAME)
                                (self.browser.find_element_by_id("user_password")).send_keys(self.USER_PASSWORD + Keys.RETURN)
                                print('Time consuming: ', time.time() - t)
                                time.sleep(self.buffer_wait*2)

                                # Scrape tasks list
                                self.browser.switch_to_default_content()
                                time.sleep(self.buffer_wait)
                                WebDriverWait(self.browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it("gsft_main"))
                                print('Time consuming: ', time.time() - t)
                                self.scrape_task_list(self.browser.page_source)
                                
                                # Switch browser focus to main frame and scrape task html
                                '''
                                self.browser.get(self.task_url)
                                self.browser.switch_to_default_content()
                                print('Time consuming: ', time.time() - t)
                                time.sleep(self.buffer_wait)
                                WebDriverWait(self.browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it("gsft_main"))
                                self.scrape_Task(self.browser.page_source)
                                '''

                                # Stop loop
                                go = False

                        except TimeoutError:
                                print(f"Timeout Error: {int(time.time()-t)}")
                                self.browser.close
                                go = True
                                failed_starts += 1
                        except NoSuchElementException as e:
                                print(f"Not Found Error: {int(time.time()-t)} - {e}")
                                self.browser.close
                                go = True
                                failed_starts += 1
                        finally:
                                self.browser.close()
                                print(f"Total Exception Restarts: {failed_starts}")

        def scrape_task_list(self, html):
                soup= BeautifulSoup(html, features="lxml")
                try:
                        # data in table/tbody/tr/td/div/table/-> thead & tbody/tr/td
                          # You can check what fields are included in columns by looking a thead - id: hdr_sc_task
                        table= soup.find("tbody", attrs={"class":"list2_body"})
                        rows = table.findChildren("tr")

                        # grab text from each field(td) in each row of table(tr) and assign to data in task obj
                        for field in row: 
                                pass
                      
                        # parse table data w/ panda or apace aoi
                        print(rows)
                        
                        
                except Exception as e:
                        print(f"error: {e}")

        def scrape_Task(self, html):
                pass
        '''
                soup = BeautifulSoup(html, features="lxml")
                try:
                        k=0
                        created_by, status_changes, date_changed = {},{},{}    # Assigning all in one line throws value error
                        

                        # IDEA: Instead of findChild, create new soup obj using web element
                        # Each card divided into 3 blocks: CreatedBy, DateChanged, and statusChange
                        activities = soup.find(name='ul', attrs={"class":"h-card-wrapper activities-form"}).findChildren(name='li',
                                attrs={"class":"h-card h-card_md h-card_comments"})
                        for card in activities:
                                created_by= soup.findChild(name='span', attrs={"class":"sn-card-component-createdby"})
                                date_changed = soup.findChild(name='div', attrs={"class":"date-calendar"})
                                status_changes = soup.findChild(name='ul',
                                        attrs={"class":"sn-widget-list sn-widget-list-table"}).findChildren("li") # each li is an additional status change

                                change, effect = [], []; j=0 # Holds spans from li
                                for i in status_changes:
                                        # get two spans from each li in card status
                                        status = i.findChildren("span", {"class": "sn-widget-list-table"})
                                        s=""
                                        for l in status: 
                                                s=+ str(l + " ")
                                        # change[j] = status_changes[0]
                                        # effect[j] = status [1]
                                        pass
                                # print(f"User: {created_by}, Date: {date_changed}")
                                # print(f"\n\nStatus: {status}")

                except NoSuchAttributeException as e:
                        print(f"Error: Attribute attribute requested, {e}")
                except Exception as e:
                        print(f"SCRAPING ERROR: {e}")
        '''                        

def main():
        # Catch Errors: Webdriver - Permisson denied(for update or other browser error),
        # NoSuchElem for uname login,
        # Message: connection refused for random browser error
        # Timeout excep loop with counter for resets on connection
        t= TaskScraper()
        t.go_scrape()

if __name__ == "__main__":
        main()

'''
s = getHtml("https://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python")
r = getHtml("http://www.storybench.org/how-to-scrape-reddit-with-python/")
soup = getHtml('https://dev58662.service-now.com/pm')
openBrowser('https://dev58662.service-now.com/pm')

'''