'''
Past Issues: 
- October -  Check if input boxes are loaded as a JavaScript Post-Load - They are.
    - Use implicit timed waits and try to do it, then figure out why explicit wont work
    - Try different by (e.g. selector, xpath, inner html, index in collection of same tags)
        - Make use of bs4 to organize and understand html
        - Recall Aaron said some property of the tables in SN are different ea time
    - FIX: Had to enter inline frame, using selenium before I could search for the login box  
- Nov 29 - SN Service Interruption: This instance is unavailable.
- index error fixed by removing first 2 table cols from fields, and first 2 and last 3 tags from each task (tr)
- Before Dec 4: During Table scrape, all tasks except top one would be Pulled in - FIX: idk but that task is gone from catalouge 
- Any window size other than maximized causes a problem while trying to click on first task

- NVM I just had debugger set to stopped on caught exceptions: for col in soup.find("tr", attrs={"id" : "hdr_sc_task"}): field_order.append(col.attrs['name']) inside scrape_task_list() - Throws Key error Exception when running in debugger 

TODO: Tasks
LAST: 
DOES NOT need worknotes -- So just fix bugs, export to csv and start testing. Also needs a Temp CLI, then eventually GUI
- given the location of python as their first line: #!/usr/bin/python and become executable.

1) Turn tasks into data objects:            # apachepoi
        # for task iteration: the data will already be in a table and a filter allows the user to specify the data thats provided,
        if its easier than drilling down with scrape_task, notify user of specified filter settings and go by that,
        otherwise just grab whatever you can while there b/c table data doesnt require page transition from selenium.
        # In go_scrape main loop, handle error checking and close browser and restart on error
        # Fill w/ params from GUI
        # Target takes to login then to target page
2) Export Task data to csv using apache poi or panda 
3) Replace any timed waits with multiple web element based waits for selenium interactions, error handling
        - Then handle TimeoutExceptions and NotfoundExceptions more gracefully than denials and browser Exceptions
4) wrap in Java Fx, Get params through GUI
- create a doc for how to document web dev proj
- download sphinx
- set up proper testing task page
- Rebase commits, clean up commit history
- save an offline copy of html w/ removed scripts and other stuff

TODO: Issues and Problems:
- Close request connection? - on reddCrawl too
- ## Needed Fields: We can handle deciding what fields to grab by:
        - have checkboxes with what fields to grab  
- Still no reboot checks on main() for WebDriverException: Conn refused and Timeout
- Table Scrape has a max of 30 attributes I can grab before I either need to scroll. 
        - This should be fine because most fields are blank, but can be reviewed after first table scrape 
        to determine if a second scrape (w/ altered attribute filter) is needed. (or a page scrape)  
- Every bs4 interaction, after using selenium, Needs a couple of error loops incase some data hasn't finished loading 
- Assume url takes you straight to task page, then if not found use backup url and navigate via selenium
        - You can check by grabbing page url and comparing with target

TODO: Moving Forward:
- Start from task lists and do for each task - https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task_list.do%3Fsysparm_userpref_module%3D59f8a2a60a0a0b9b00fd6bfe2e28ada5%26sysparm_query%3Dactive%3Dtrue%5EEQ%26sysparm_clear_stack%3Dtrue
- Can follow a direct link to catalog tasks or go through sidebar links by setting a checkbox in dash
- PARAMS: uname, password, target_url(Maybe w/ some webElement verification) and backup URL, checked off Task attributes, 
        - CONFIGS: bufferwait, seconds for time.sleep()'s, num restarts, 

TODO: Error Checks:
- Browser wont start - Message: Tried to run command without establishing a connection
- Malformed Url - Happened directly after adding browser.get(task_url)

Notes: 

reports -> umrf 

number, opened closed title assignmentgroup, 

Activities: assigned to and state



'''
# encoding: utf-8
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, NoSuchAttributeException, InvalidSessionIdException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import lxml
import requests
import pandas as pd
import re
import clipboard as cb
import time

USER_NAME="admin"
USER_PASSWORD= 'Veryhap1*'
list_url= "https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task_list.do%3Fsysparm_clear_stack%3Dtrue%26sysparm_query%3Dactive%253Dtrue%255EEQ"
task_url=""
buffer_wait = 2 # Seconds

# For testing
task_demo_url = 'https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task.do%3Fsys_id%3Ddfed669047801200e0ef563dbb9a712b%26sysparm_view%3Dmy_request%26sysparm_record_target%3Dsc_task%26sysparm_record_row%3D1%26sysparm_record_rows%3D1%26sysparm_record_list%3Drequest_item%253Daeed229047801200e0ef563dbb9a71c2%255EORDERBYDESCnumber'
restart_limit = 5
task_page_limit= 0

# Replace url with given Task Page url in GUI
def get_browser_driver(url=list_url):
# Creates and returns selenium browser window
        driver= webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe')
        driver.maximize_window()
        driver.set_page_load_timeout(20)
        driver.get(url)
        return driver

#  does the down task iter arrow, or the Next recs span, disappear when there is no more tasks? 
#       if so, we dont need to check NumRecords for the while loop task_cont boolean
# Change login to wait for username element; Tasks iteration needs testing with task table cutoff 
# (does it include all tasks or just those on current table page),
def go_scrape(failed_start_threshold=restart_limit):
        # Start selenium browser and begin scraping loop
        BROWSER_TIMEOUT = 45 # seconds
        
        cont_loop = True
        failed_starts= 0
        t=time.time()
        while (cont_loop==True and failed_starts < failed_start_threshold ):
                try:
                        browser= get_browser_driver()
                        try: 
                                # Try to start task crawl - Takes average of 20 secs to login
                                time.sleep(buffer_wait)
                                WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it((0)))
                                
                                # Change to wait until uname and password appear - should fix random errors
                                time.sleep(buffer_wait)
                                (browser.find_element_by_name("user_name")).send_keys(USER_NAME)
                                (browser.find_element_by_id("user_password")).send_keys(USER_PASSWORD + Keys.RETURN)
                                time.sleep(buffer_wait*2)
                        except Exception as e: 
                                print(f"Scraping Loop - Error During Login: {e}")
                        try:
                                # Scrape tasks table and return list
                                browser.switch_to.default_content() 
                                time.sleep(buffer_wait)
                                WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it("gsft_main"))
                                time.sleep(buffer_wait)
                                catalog_tasks= scrape_task_list(browser.page_source)
                                
                                # Click first task and start individual task page scrape loop 
                                browser.find_element_by_xpath("//a[@class='linked formlink']").click()
                        except Exception as e: 
                                print(f"Scraping Loop - Error Clicking on Task Link: {e}")           
                        
                        # For Checking next page of task table - Check vcr_controls div and return value for more tasks on next page or not
                        # div = soup.find("div", attrs={"class":"vcr_controls"}).findChild()
                        # print(div)

                        # set task limit to number of active tasks if no limit is specified
                        task_page_limit= 8

                        cont_task= True; num_tasks=0
                        while(cont_task and num_tasks < task_page_limit):
                        # Iterate through tasks and pass to scrape task with a flag for new/updated
                                soup = ""
                                try:
                                        # Switch browser focus to main frame and scrape task html
                                        time.sleep(buffer_wait) 
                                        browser.switch_to.default_content()
                                        time.sleep(buffer_wait)
                                        WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it("gsft_main"))
                                        time.sleep(buffer_wait*3)

                                        # Find "Next Task" button and check if next is last page
                                        next_button= browser.find_element_by_xpath("//button[@class='btn btn-icon icon-arrow-down']")
                                        
                                        soup = BeautifulSoup(browser.page_source, features="lxml")
                                
                                # Exceptions: On Timeout - Wrong frame, On NoSuchElement - Not loaded or Wrong frame 
                                except Exception as e: 
                                        print(f"Scraping Loop - Error Finding Next Task button: {e}")  

# Problem - all Activities before last task's added to new tasks bc name isnt valid
# either just hit next Task button until it dissapears or 
# get total number of Tasks from Table first then set that as cap if none is specified
  
                                # Check if task number is already in Catalog_tasks list to determine whether to grab extra details with Tasks Activities
                                name = soup.find(name="input", attrs={"id":"sc_task.number", "name":"sc_task.number", "class":"form-control"}).attrs['value']
                                update_index=-1
                                for task_index in range(len(catalog_tasks)): 
                                        if catalog_tasks[task_index].number == name: update_index= task_index

                                # Scrape Task Page and create new task obj if not in catalog task, otherwise update task  
                                if (update_index == -1) : 
                                        catalog_tasks += [scrape_Task(browser.page_source)]
                                elif (update_index >= 0): 
                                        catalog_tasks[update_index] = scrape_Task(browser.page_source, catalog_tasks[update_index])
                                num_tasks += 1
                                
                                try: next_button.click()
                                except Exception as e:
                                        print("Error cannot iterate Task, button not found: ", int(time.time()-t))
                                        cont_loop = True
                                        failed_starts += 1
                                # Also check button text for next page being last

####    Iteratting through Task pages - down button DOES disappear and become unclickable on last task in single page list. 
        # So you'll have to check one iteration beforehand and signal that the next is the last one
        # Also the page that it shows as text is the next page after not current task page 
                                # Check if reached final task and if not Click down arrow to iterate tasks pages
                                # records_str = soup.find("div", {"class":"record-paging-nowrap"}).findChild("button", attrs= {"class":"btn btn-icon icon-arrow-down" }).findChild("span", attrs={"class":"sr-only"}).get_text()
                                # records = [int(s) for s in records_str if s.isdigit()] # Next record (\d of \d)
                                # if (records[0] == records[1]): cont_task=False # Stop Task Scraping loop
                                # print(records)
                                
####    Clicking the down button, this ones having issues clicking, it did it once but once I looped it it started bugging. 
        # try: timed waits, double clicking, window size
        # MORE SPECIFIC XPATH, that worked last time 
 ########## OKAY JUST Looked at the driver window and it is definitely scrolling thru pgs, 
 # theres just some error happening that stops the loop. Its prob that the button disappears  
 # on last Task page and I cant tell if its got the data by that point or not. Functional just needs cleanup
 # for all the sloppy selenium interactions. 
        # to think about later: I would add some verifiers or assertions so we can get some consistency going as far as running.
        # Maybe setup a temporary log, also look at gecko logs               
                                        # Iterate tasks by clicking down arrow
                                  
                                        
####    On another note one error throws off entire scraping loop. Either split up with try-catch loops so data does'nt get lost
        # Or just load each entry into csv and pick up where you left off when you run again
                                
                        # Stop main scraper loop
                        cont_loop = False
                        browser.close()
                        for i in catalog_tasks: i.show()
                        print(f"Total Tasks Scraped: {len(catalog_tasks)}") 
                except TimeoutError:
                        print(f"Timeout Error: {int(time.time()-t)}")
                        browser.close()  
                        cont_loop = True
                        failed_starts += 1
                except NoSuchElementException as e:
                        print(f"Not Found Error: {int(time.time()-t)} - {e}")
                        browser.close()
                        cont_loop = True
                        failed_starts += 1
                except WebDriverException as e:
                        print(f"Web Driver Error: {int(time.time()-t)} - {e}")
                        browser.close()
                        cont_loop = True
                        failed_starts += 1
                finally:
                        pass # print(f"Total Scraping Loop Restarts: {failed_starts}\n")

# Still doesnt go next page
def scrape_task_list(html):
# Scrapes what it can from table, based on whats already set in filter, to establish list of tasks 
        soup= BeautifulSoup(html, features="lxml")
        field_order= [] 

        # Gets column headers from table header tags
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
                tasks=[]
                # grab text from each field(td) in each row of table(tr) and assign to data in task obj
                for task in rows:
                        # Grab Task attributes
                        k=0
                        task_attrs= {}
                        task_data= task.findChildren("td")
                        task_data= task_data[2:(len(task_data)-4)] # frst of 3 datex is [20:]
                        for attr in task_data:
                                task_attrs[str(fields[k])] = attr.get_text() # IndexError: list index out of range
                                if attr.get_text() == None or attr.get_text()== "" : # make sure attr are properly assigned
                                        task_attrs[str(fields[k])] = 'N/A'
                                k=k+1
                        tasks += [Task(task_attrs[str(fields[0])], task_attrs, [])]
                return tasks
        except Exception as e:
                print(f"Task Table Scraping Error: {e}")

# Still needs to grab data for a new task - unless we're sure all tasks will be documented by the table scrape                    
def scrape_Task(html, update_task=None):
        # Returns task object
        soup = BeautifulSoup(html, features="lxml")
        activity_cards = []
        
        print(f"Scraping {soup.find(name='input', attrs={'id':'sc_task.number', 'name':'sc_task.number', 'class':'form-control'}).attrs['value']} Page ...")
     
        
        try:
        # Grabbing Activities
                created_by, status_changes, date_changed = {},{},{}
                activities = soup.find(name='ul', attrs={"class":"h-card-wrapper activities-form"}).findChildren(name='li',
                        attrs={"class":"h-card h-card_md h-card_comments"})
                for card in activities:
                        created_by= card.findChild(name='span', attrs={"class":"sn-card-component-createdby"}).get_text()
                        date_changed = card.findChild(name='div', attrs={"class":"date-calendar"}).get_text()
                        status_changes = card.findChild(name='ul',
                                attrs={"class":"sn-widget-list sn-widget-list-table"}).findChildren("li")
                        task_changes= []
                        for li in status_changes:
                                spans= li.findChildren()
                                spans[1] = spans[1].findChild()
                                task_changes += [str(spans[0].get_text()) + " " + str(spans[1].get_text())] 
                        
                        # Group activity details by each card and add card to activity list of respective Task object 
                        activity_cards += [TaskActivity(created_by, date_changed, task_changes)]
                
                if not (update_task==None): 
                # if Task to update is provided just append cards                        
                        update_task.activity_cards= activity_cards
                        return update_task
                else: 
# Remove Tasks_page_limit and handle check for next page being last task page
# if newTask get detailed info and return new task object
                        return Task("Should Create New Task HERE", {"sad":"sdSZd"}, activity_cards)
        except NoSuchAttributeException as e:
                print(f"Error: Attribute attribute requested, {e}")
        except Exception as e:
                print(f"Individual Task Scraping Error: {e}")







# Its not really neccessary until it becomes a prob, 
# but concerning Exporting to CSV: you can send it to a txt for backup 
# (incase of runtime interruption) then csv once complete, really just reread csv and ignore those already fully updated
class Task:                                             
        def __init__(self, number, task_attributes, activity_cards):
                self.number= number
                self.task_attributes= task_attributes
                self.activity_cards = activity_cards
        
        def show(self):
                print(f"\n## {self.number}")
                for i in self.task_attributes: 
                        print(f"\t- {i}:  {self.task_attributes[i]}")
                print(f" Activity Cards: ")
                try: 
                        for s in self.activity_cards: s.show()
                except Exception as e: print(e, self.activity_cards) # For debugging
class TaskActivity:
        # Contains activity information from each card 
        def __init__(self, created_by, date_changed, changes_list):
                self.created_by = created_by
                self.date_changed = date_changed
                self.changes_list = changes_list

        def show(self):
                print(f"\tUser: {self.created_by}\n \tDate: {self.date_changed}\n \tChanges: {self.changes_list}\n")
        

def main():
        # Catch Errors: Webdriver - Permisson denied(for update or other browser error),
        # NoSuchElem for uname login,
        # Message: connection refused for random browser error
        # Timeout excep loop with counter for resets on connection
        go_scrape()

if __name__ == "__main__":
        main()

'''
s = getHtml("https://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python")
r = getHtml("http://www.storybench.org/how-to-scrape-reddit-with-python/")
soup = getHtml('https://dev58662.service-now.com/pm')
openBrowser('https://dev58662.service-now.com/pm')

'''