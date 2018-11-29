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
# Used to write a fixed sequence of characters to a file writelines()
# writelines can write a list of strings

import os.path
save_path = 'C:/example/'
name_of_file = raw_input("What is the name of the file: ")
completeName = os.path.join(save_path, name_of_file+".txt")

# Debugging:            https://code.visualstudio.com/Docs/editor/debugging
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

 
## Problems and Solns: 
- index error fixed by removing first 2 table cols from fields, and first 2 and last 3 tags from each task (tr)

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

Issues: 
        ## Needed Fields: We can handle deciding what fields to grab by:
               1) have checkboxes with what fields to grab  
        # Still no reboot checks on main() for WebDriverException: Conn refused and Timeout
'''

class TaskScraper:
        # Class Structure: 1) def function which will handle error checking and close browser and restart on error
        # Fill w/ params from GUI
        # Target takes to login then to target page
        task_url = 'https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task.do%3Fsys_id%3Ddfed669047801200e0ef563dbb9a712b%26sysparm_view%3Dmy_request%26sysparm_record_target%3Dsc_task%26sysparm_record_row%3D1%26sysparm_record_rows%3D1%26sysparm_record_list%3Drequest_item%253Daeed229047801200e0ef563dbb9a71c2%255EORDERBYDESCnumber'
        list_url= "https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task_list.do%3Fsysparm_clear_stack%3Dtrue%26sysparm_query%3Dactive%253Dtrue%255EEQ"
        buffer_wait = 2 # Seconds

        USER_NAME="admin"
        USER_PASSWORD= 'Veryhap1*'

        def __init__(self):
                def exec_window_prefs(driver):
                        driver.set_window_position(0, 0)
                        driver.set_window_size(325, 250)
                        return driver
                # self.url= url
                self.browser= exec_window_prefs(webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe'))

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
                        except WebDriverException as e:
                                print(f"Web Driver Error: {int(time.time()-t)} - {e}")
                                self.browser.close
                                go = True
                                failed_starts += 1
                        finally:
                                self.browser.close()
                                print(f"Total Exception Restarts: {failed_starts}\n")

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
        
        def scrape_task_list(self, html):
                # Well grab what we can from table, then go back for any incomplete data (desc w/ ...)
                def get_table_columns(soup):
                        table_header= soup.find("tr", attrs={"id" : "hdr_sc_task"})
                        field_order= []
                        for col in table_header:
                                try: 
                                        field_order.append(col.attrs['name'])    
                                except Exception:
                                        field_order.append("No Attribute")
                        return field_order[2:]
                #  I just need to know the order
                #  - The harder part is actually changing the order, 
                #       it may make more since to just keep order same and add whats missing then 
                #       just use order given to determine which order you assign the tds to Task vars
        
                soup= BeautifulSoup(html, features="lxml")
                try:
                        # data in table/tbody/tr/td/div/table/-> thead & tbody/tr/td
                          # You can check what fields are included in columns by looking at thead - 
                        fields = get_table_columns(soup)
                        table= soup.find("tbody", attrs={"class":"list2_body"})
                        rows = table.findChildren("tr")

                        # grab text from each field(td) in each row of table(tr) and assign to data in task obj
                        for task in rows: 
                                task_data= task.find_all("td")
                                task_attrs= {}
                                k=0

                                # Task attributes saved in data, not labelled
                                for attr in task_data:
                                        task_attrs[str(fields[k])] = attr.text
                                        if task_data[k].get_text() == "" or task_data[k].get_text() == re.compile("(empty)"): # make sure attr are properly assigned
                                                task_attrs[str(fields[k])] = 'N/A'
                                        k=k+1
                                Task(task_attrs[str(fields[0])], task_attrs)

                        # print(f">>> True String({len(task_data)})/False Strings({len(empty_tags)})\n- {task_data}\n -{empty_tags}")       
                        
                        # parse table data w/ panda or apace poi
                        print(f"\n----------\nTotal rows: {len(rows)}")
                        print(f"Total table fields: {len(fields)}")

                except Exception as e:
                        print(f"Go Loop Error: {e}")


# Last issue 
                # Alt option: Set gear filter before grabbing, use only fields garunteed to be there 
                # Last option: just grab name and basics and present list to user, allow them to specify the extra fields needed and start slower 2nd round of scraping(w/ error checking loops w/ max cap)

# Just for use in interactive shell for testing purposes: trying to inject blank spaces into blcnk table cells
class EZTask:
        list_url= "https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task_list.do%3Fsysparm_clear_stack%3Dtrue%26sysparm_query%3Dactive%253Dtrue%255EEQ"
        buffer_wait = 2 # Seconds

        USER_NAME="admin"
        USER_PASSWORD= 'Veryhap1*'

        def __init__(self):
                def exec_window_prefs(driver):
                        driver.set_window_position(0, 0)
                        driver.set_window_size(325, 250)
                        return driver
                # self.url= url
                self.browser= exec_window_prefs(webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe'))

        # Start scraping loop        - Loop can either be main, in init or just here as a kickoff method
        def go(self, failed_start_threshold=5 ):
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
                                time.sleep(self.buffer_wait*3)
                                html = self.browser.page_source
                                self.browser.close()
                                go= False
                        except Exception as e:
                                print(f"Exploration Error: {e}")
                                self.browser.close
                                go = True
                                failed_starts += 1
                return BeautifulSoup(html, features="lxml")
        
        def setEm(self):
                def get_table_columns(soup): # Gets field headers
                        table_header= soup.find("tr", attrs={"id" : "hdr_sc_task"})
                        field_order= []
                        for col in table_header:
                                try: 
                                        field_order.append(col.attrs['name'])    
                                except Exception:
                                        field_order.append("Missing Attribute")
                        return field_order[2:]
                soup= self.go()
                self.fields =get_table_columns(soup)
                self.table= soup.find("tbody", attrs={"class":"list2_body"})
                self.rows = self.table.contents# self.table.find_all("tr")

## NEXT UP: Issue: Some tasks are not being, THEN: press button and go to next page, if data matches prev page toss it
## Will be followed by Showing data in gui then asking about follow up individual tasks scrape
## Issue: Some tasks are not being included at all in the html - Not webwait(no new items appear), Not panda(Doesnt understand field structure)

## try: find(text="Task1111") to find it, pandas.read_html, giving selenium more time to load the page, scrolling table (not likely)
## Debugging: Where are the other tasks going? How many are missing? 
#try loading html in browser, try just decomposing unneccessary tags, check num rows is consistent(7 vs 10)
#  Whats all in the html: table, num rows, num cols, do task attributes change?

                t= soup.find("table")
                
                
                print(f"Children: {len(t.findChildren())}")
                print(f"T is : {len(t)}")
                print(f"First Child: \n{t.findChildren()[0]}")
                print(f"All Table Contents ({len(t.find_All())}): \n{len(t.find_All())}")
                print(f"Table itself: \n{t}")
                

                # grab text from each field(td) in each row of table(tr) and assign to data in task obj
                self.tasks= []
                for task in self.rows:
                        # Grab Task attributes
                        task_data= task.findChildren("td")
                        task_data= task_data[2:(len(task_data)-4)] # frst of 3 datex is [20:]
                        task_attrs= {}
                        k=0
                        l= len(task_data)
                        # More task_data attr(td) than fields (col names)
                        for attr in task_data:
                                task_attrs[str(self.fields[k])] = attr.get_text() # IndexError: list index out of range
                                if attr.get_text() == None or attr.get_text() == re.compile("(empty)") or attr.get_text()== "" : # make sure attr are properly assigned
                                        task_attrs[str(self.fields[k])] = 'N/A'
                                k=k+1
                        self.tasks += [Task(task_attrs[str(self.fields[0])], task_attrs, l)]

                        # Adding blanks as temp fix for indexing error in fields(3 less than )
                for i in self.tasks:
                        pass#i.show()
                         
                          
class Task:                                             
        def __init__(self, number, task_attributes, numTags):
                self.number= number
                self.task_attributes= task_attributes
                self.numTags= numTags
        def show(self):
                print(f"\n## {self.number} ... attrs: {len(self.task_attributes)} out of {self.numTags} Tags")
                for i in self.task_attributes: 
                        print(f"\t- {i}:  {self.task_attributes[i]}")

def main():
        # Catch Errors: Webdriver - Permisson denied(for update or other browser error),
        # NoSuchElem for uname login,
        # Message: connection refused for random browser error
        # Timeout excep loop with counter for resets on connection
        t= EZTask()
        # t.go_scrape()
        soup= t.setEm()

if __name__ == "__main__":
        main()

'''
s = getHtml("https://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python")
r = getHtml("http://www.storybench.org/how-to-scrape-reddit-with-python/")
soup = getHtml('https://dev58662.service-now.com/pm')
openBrowser('https://dev58662.service-now.com/pm')

'''