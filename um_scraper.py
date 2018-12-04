'''
Past Issues: 
- Nov 29 - SN Service Interruption: This instance is unavailable.

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
        1) Write alg for getting task list and turn tasks into data objects:            # apachepoi
                # for task iteration: the data will already be in a table and a filter allows the user to specify the data thats provided,
                if its easier than drilling down with scrape_task, notify user of specified filter settings and go by that,
                otherwise just grab whatever you can while there b/c table data doesnt require page transition from selenium.
                # def function which will handle error checking and close browser and restart on error
                # Fill w/ params from GUI
                # Target takes to login then to target page
        3) Replace any timed waits with multiple web element based waits for selenium interactions, error handling
        4) wrap in Java Fx

Issues: 
        ## Needed Fields: We can handle deciding what fields to grab by:
               1) have checkboxes with what fields to grab  
        # Still no reboot checks on main() for WebDriverException: Conn refused and Timeout
'''

USER_NAME="admin"
USER_PASSWORD= 'Veryhap1*'
task_url = 'https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task.do%3Fsys_id%3Ddfed669047801200e0ef563dbb9a712b%26sysparm_view%3Dmy_request%26sysparm_record_target%3Dsc_task%26sysparm_record_row%3D1%26sysparm_record_rows%3D1%26sysparm_record_list%3Drequest_item%253Daeed229047801200e0ef563dbb9a71c2%255EORDERBYDESCnumber'
list_url= "https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task_list.do%3Fsysparm_clear_stack%3Dtrue%26sysparm_query%3Dactive%253Dtrue%255EEQ"
buffer_wait = 2 # Seconds

# Replace url with given Task Page url in GUI
def get_browser_driver(url=list_url):
# Creates and returns selenium browser window
        driver= webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe')
        driver.set_window_position(0, 0)
        driver.set_window_size(325, 250)
        driver.set_page_load_timeout(20)
        driver.get(url)
        return driver

# Start selenium browser and begin scraping loop        - Loop can either be main, in init or just here as a kickoff method
def go_scrape(failed_start_threshold=5):
        BROWSER_TIMEOUT = 45 # seconds
        cont_loop = True
        failed_starts= 0
        while (cont_loop==True and failed_starts < failed_start_threshold ):
                try:
                        # Try to start task crawl - Takes average of 20 secs to login
                        time.sleep(buffer_wait)
                        WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it((0)))
                        
                        # Change to wait until uname and password appear - should fix random errors
                        time.sleep(buffer_wait)
                        (browser.find_element_by_name("user_name")).send_keys(USER_NAME)
                        (browser.find_element_by_id("user_password")).send_keys(USER_PASSWORD + Keys.RETURN)
                        time.sleep(buffer_wait*2)

                        # Scrape tasks list
                        browser.switch_to_default_content() 
                        time.sleep(buffer_wait)
                        WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it("gsft_main"))
                        scrape_task_list(browser.page_source)
                        # Click nextpage then repeat
                        # browser.find()

                        # Show Results and confirm second individual scrape or ask before starting 
                
                        
                        # Switch browser focus to main frame and scrape task html
                        '''
                        browser.get(task_url)
                        browser.switch_to_default_content()
                        print('Time consuming: ', time.time() - t)
                        time.sleep(buffer_wait)
                        WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it("gsft_main"))
                        scrape_Task(browser.page_source)
                        '''

                        # Stop loop
                        cont_loop = False

                except TimeoutError:
                        print(f"Timeout Error: {int(time.time()-t)}")
                        browser.close
                        cont_loop = True
                        failed_starts += 1
                except NoSuchElementException as e:
                        print(f"Not Found Error: {int(time.time()-t)} - {e}")
                        browser.close
                        cont_loop = True
                        failed_starts += 1
                except WebDriverException as e:
                        print(f"Web Driver Error: {int(time.time()-t)} - {e}")
                        browser.close
                        cont_loop = True
                        failed_starts += 1
                finally:
                        browser.close()
                        print(f"Total Exception Restarts: {failed_starts}\n")

def scrape_Task(html):
        soup = BeautifulSoup(html, features="lxml")
        try:
                k=0
                created_by, status_changes, date_changed = {},{},{}

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


def scrape_task_list(html):
# grabs what it can from table, then later if neccessary goes back for any incomplete data (desc, worknotes, ... )
        soup= BeautifulSoup(html, features="lxml")

        # Gets column headers from table header tags
        field_order= [] 
        for col in soup.find("tr", attrs={"id" : "hdr_sc_task"}):
                try: 
                        field_order.append(col.attrs['name'])    
                except Exception:
                        field_order.append("No Attribute")
        fields = field_order[2:]
        
        # Find and scrape table body based on header fields
        try:
                table= soup.find("tbody", attrs={"class":"list2_body"})
                rows = table.findChildren("tr")

                # Pulled from EZTask
                # grab text from each field(td) in each row of table(tr) and assign to data in task obj
                tasks= []
                for task in rows:
                        # Grab Task attributes
                        task_data= task.findChildren("td")
                        task_data= task_data[2:(len(task_data)-4)] # frst of 3 datex is [20:]
                        task_attrs= {}
                        k=0
                        l= len(task_data)
                        # More task_data attr(td) than fields (col names)
                        for attr in task_data:
                                task_attrs[str(fields[k])] = attr.get_text() # IndexError: list index out of range
                                if attr.get_text() == None or attr.get_text() == re.compile("(empty)") or attr.get_text()== "" : # make sure attr are properly assigned
                                        task_attrs[str(fields[k])] = 'N/A'
                                k=k+1
                        tasks += [Task(task_attrs[str(fields[0])], task_attrs, l)]
                for i in tasks:
                        i.show()
                # parse table data w/ panda or apace poi
                print(f"\n----------\nTotal rows: {len(rows)}")
                print(f"Total table fields: {len(fields)}")

        except Exception as e:
                print(f"Go Loop Error: {e}")


# Last issue 
                # Alt option: Set gear filter before grabbing, use only fields garunteed to be there 
                # Last option: just grab name and basics and present list to user, allow them to specify the extra fields needed and start slower 2nd round of scraping(w/ error checking loops w/ max cap)

# Class for testing in instance
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
                self.browser= exec_window_prefs(webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe'))
        def get_list_soup(self, failed_start_threshold=5 ):
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
        
        def get_browser():
                BROWSER_TIMEOUT = 45 # seconds
                cont_loop = True
                failed_starts= 0
                while (cont_loop==True and failed_starts < failed_start_threshold ):
                        try:
                                # Try to start task crawl - Takes average of 20 secs to login
                                browser.set_page_load_timeout(20)
                                browser.get(list_url)
                                time.sleep(buffer_wait)
                                WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it((0)))
                                
                                # Change to wait until uname and password appear - should fix random errors
                                time.sleep(buffer_wait)
                                (browser.find_element_by_name("user_name")).send_keys(USER_NAME)
                                (browser.find_element_by_id("user_password")).send_keys(USER_PASSWORD + Keys.RETURN)
                                time.sleep(buffer_wait*2)
                        except Exception as e: 
                                print(f"Error returning browser: {e}")


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
                soup= self.get_list_soup()
                self.fields =get_table_columns(soup)
                self.table= soup.find("table")
                self.tbody = soup.find("tbody", attrs={"class":"list2_body"})
        
## NEXT UP: Issue: Some tasks are not being, THEN: press button and go to next page, if data matches prev page toss it
## Will be followed by Showing data in gui then asking about follow up individual tasks scrape
## Issue: Some tasks are not being included at all in the html - Not webwait(no new items appear), Not panda(Doesnt understand field structure)

## Debugging: Where are the other tasks going? How many are missing? ; try: find(text="Task1111") to find it, scrolling table (not likely) 
# try loading html in browser, try just decomposing unneccessary tags, check num rows is consistent(7 vs 10)

# Dcoumentation - easy install sphinx: https://pythonhosted.org/an_example_pypi_project/sphinx.html
                self.rows = self.table.contents# self.table.find_all("tr")
                
                # Show for debugging
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
                        for attr in task_data:
                                task_attrs[str(self.fields[k])] = attr.get_text() # IndexError: list index out of range
                                if attr.get_text() == None or attr.get_text() == re.compile("(empty)") or attr.get_text()== "" : # make sure attr are properly assigned
                                        task_attrs[str(self.fields[k])] = 'N/A'
                                k=k+1
                        self.tasks += [Task(task_attrs[str(self.fields[0])], task_attrs, l)]

                        # Adding blanks as temp fix for indexing error in fields(3 less than )
                for i in self.tasks:
                        pass # i.show()
                         
                          
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