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

- NVM on key error - I just had debugger set to stopped on caught exceptions: for col in soup.find("tr", attrs={"id" : "hdr_sc_task"}): field_order.append(col.attrs['name']) inside scrape_task_list() - Throws Key error Exception when running in debugger 

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
        - Replace url with given Task Page url in GUI

TODO: Error Checks:
- Browser wont start - Message: Tried to run command without establishing a connection
- Clean up Any user interaction errors to tell user to restart loop - Do for all try/excepts - On Timeout - Wrong frame, On NoSuchElement - Not loaded or Wrong frame 
- Malformed Url - Happened directly after adding browser.get(task_url)

Notes: 

reports -> umrf 

number, opened closed title assignmentgroup, 

Activities: assigned to and state

AUTOFIX Commit Notes: 
- line 250 may be a problem in EPDSM, it correctly cuts first 2 td of each row in table, but also cuts last 4 off the end, if this is important data it will be a problem - Easily solved by fixing fields section or just use indv page scrape
- Go through testing different wait times to try and shorten runtime
- Currently exports to csv, but with small set column widths. Can fix col widths(https://www.bing.com/search?q=cant+increase+column+size+in+excel+csv&PC=U316&FORM=CHROMN), but can also be changed to another file type if neccessary.
- but concerning Exporting to CSV: you can send it to a txt for backup (incase of runtime interruption) then csv once complete, really just reread csv and ignore those already fully updated
- Only prioritized task number, state, assigned_to, and all activity cards. I can still update descriptions and other details during indiviual page scrape
- May be an issue with Assigned_Group - Since Scraper doesn't iterate table pages and assigned_group doesn't
appear on task page; its not a problem if Assigned_to == Assigned group, but otherwise ill need to add in a table iterator first. 
- field names will probably need to be renamed when combining updated(table scraped) and new(page scraped) Tasks, before export
- No checks in place rn, a single error will throw off whole loop. Needs proper waits, checkpoints - maybe on start check current progress of csv,
- needs initialization from user via config file (use/find a parser?) 
- to think about later: I would add some verifiers or assertions so we can get some consistency going as far as running.
- Maybe setup a temporary log, also look at gecko logs                                             
- On another note one error throws off entire scraping loop. Either split up with try-catch loops so data does'nt get lost
        -  Or just load each entry into csv and pick up where you left off when you run again

feild_names = ['number', 'active', 'priority', 'state', 'assigned_to', 'sys_created_by', 'opened_at', 'opened_by', 'assignment_group', 'sys_created_on', 
'short_description', 'description', 'comments_and_work_notes', 'work_notes', 'work_notes_list', 'closed_at', 'closed_by', 'reassignment_count', 'sys_updated_on', 
'sys_updated_by', 'due_date', 'expected_start', 'follow_up', 'sys_class_name', 'time_worked', 'approval_history', 
'additional_assignee_list', 'comments', 'business_duration', 'close_notes', 'company', 'upon_approval', 'upon_reject']

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
import pandas as pd
import time

task_url=""

# Set by config/GUI
USER_NAME="admin"
USER_PASSWORD= 'Veryhap1*'
list_url= "https://dev58662.service-now.com/nav_to.do?uri=%2Fsc_task_list.do%3Fsysparm_clear_stack%3Dtrue%26sysparm_query%3Dactive%253Dtrue%255EEQ"
buffer_wait = 2 # Seconds to wait implicitly in between selenium interactions
BROWSER_TIMEOUT = 20 # Maximum seconds selenium waits for DOM web elements appear
filename_for_export= "SN_Catalog_Tasks.csv"

# For Runtime Limits
restart_limit = 5
task_page_limit= 0

def get_browser_driver(url=list_url):
# Creates and returns selenium browser window
        driver= webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe')
        driver.maximize_window()
        driver.set_page_load_timeout(20)
        driver.get(url)
        return driver

def go_scrape(failed_start_threshold=restart_limit):
        # Start selenium browser and begin scraping loop
        global BROWSER_TIMEOUT
        catalog_tasks =[]
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
                                        time.sleep(buffer_wait)

                                        # Find "Next Task" button hand off html to BS4
                                        next_button= browser.find_element_by_xpath("//button[@class='btn btn-icon icon-arrow-down']")
                                        
                                        soup = BeautifulSoup(browser.page_source, features="lxml")
                                
                                
                                except Exception as e: 
                                        print(f"Scraping Loop - Error Finding Next Task button: {e}")  
  
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
                                
                                # Try to click next Task button. If it fails and we have the maximum num of Tasks, then the current task is the final task 
                                try: next_button.click()
                                except Exception as e:
                                        if len(catalog_tasks) == task_page_limit:
                                                print(f"Done. \nScraping loop took {int(time.time()-t)}s to complete.")
                                        else: print("Error clicking on Task iteratoration arrow: ", e)
                                
                        # Stop main scraper loop
                        cont_loop = False
                        browser.close()
                        return catalog_tasks
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
                        print(f"\nTotal Scraping Loop Restarts: {failed_starts}\n")

def scrape_task_list(html):
# Scrapes what it can from table, based on whats already set in filter, to establish list of catalog tasks. Sets task limit to number of active tasks if no limit is specified.
        soup= BeautifulSoup(html, features="lxml")
        field_order= [] 

        for col in soup.find("tr", attrs={"id" : "hdr_sc_task"}):
        # Gets column headers from table header tags. Adds "No Attribute" if the attribute has no name. Always throws Key error for first two cols.        
                try: 
                        field_order.append(col.attrs['name'])    
                except Exception:
                        field_order.append("No Attribute")
        fields = field_order[2:]

        max_tasks = int(soup.find("div", attrs={"class":"vcr_controls"}).findChildren("span")[1].findChildren("span")[1].get_text())
        print(f"Total Tasks to Scrape: {max_tasks}")
        global task_page_limit
        if task_page_limit < 1:
                task_page_limit= max_tasks

        try:
        # Find table body and grab text from each field(td) in each row of table(tr) and assign to data in task obj based on header fields
                table= soup.find("tbody", attrs={"class":"list2_body"})
                rows = table.findChildren("tr")
                tasks=[]
                for task in rows:
                # Grab relevant td tags for each row and set Task attributes, then append Task object to tasks list to return
                        k=0
                        task_attrs= {}
                        task_data= task.findChildren("td")
                        task_data= task_data[2:(len(task_data)-4)] # frst of 3 datex is [20:]
                        for attr in task_data:
                                task_attrs[str(fields[k])] = attr.get_text()
                                if attr.get_text() == None or attr.get_text()== "" :
                                        task_attrs[str(fields[k])] = 'NaN'
                                k=k+1
                        tasks += [Task(task_attrs[str(fields[0])], task_attrs, [])]
                return tasks
        except Exception as e:
                print(f"BS4 Error: Task Table Scrape failed: {e}")

def scrape_Task(html, update_task=None):
        # Grabs Activity cards from Task page and creates a lists of TaskActivity objects for Tasks, then returns task object with activity list based on update task
        soup = BeautifulSoup(html, features="lxml")
        activity_cards = []
        
        task_number = soup.find(name='input', attrs={'id':'sc_task.number', 'name':'sc_task.number', 'class':'form-control'}).attrs['value']
        print(f"Scraping {task_number} Page ...")
        try:
        # Grabbing Activity Cards
                created_by, status_changes, date_changed = {},{},{}
                activities = soup.find(name='ul', attrs={"class":"h-card-wrapper activities-form"}).findChildren(name='li',
                        attrs={"class":"h-card h-card_md h-card_comments"})
                c= 0
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
                        activity_cards += [TaskActivity(c, created_by, date_changed, task_changes)]
                        c += 1
                
                if not (update_task==None): 
                # if Task to update is provided just append cards, otherwise just grab necessary information                     
                        update_task.activity_cards= activity_cards
                        return update_task
                else: 
                        new_task_attrs = {"number": task_number, 
                                "state": soup.find("select", attrs={"name": "sc_task.state", "id": "sc_task.state"}).findChild("option", selected=True).get_text(),
                                "assigned_to": soup.find("input", attrs={"name": "sys_display.sc_task.assigned_to", "id": "sys_display.sc_task.assigned_to"}).get_text()
                                }
                        return Task(task_number, new_task_attrs, activity_cards)

        except NoSuchAttributeException as e:
                print(f"BS4 Error - Individual Task Scrape Failed - Attribute not found: {e}")
        except Exception as e:
                print(f"BS4 Error - Individual Task Scrape Failed: {e}")

################### Last time   ####################
# Currently has two task number cols, but throws error when no index is provided to pd DataFrame(ALL SCALAR VALS)
  # First try index on empty df (in comment), if that doesnt work just uncomment detailed_frame
def get_tasks_df(tasks):
# Turns catalog tasks data into a panda dataframe and writes frame to csv 
        df = pd.DataFrame({})# , index=[i.number for i in tasks] )
        for task in tasks:
                details = task.task_attributes
                details["Activities"] = str([a.get_card() for a in task.activity_cards])
                detailed_frame= pd.DataFrame(details) #, index=details["number"])
                df = pd.concat([df, detailed_frame])
        return df

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
                for s in self.activity_cards: s.show()
                
class TaskActivity:
# Contains activity information from each card. Note that a lower index indicates a more recent activity with 0 being the most recent  
        def __init__(self, index, created_by, date_changed, changes_list):
                self.index = index
                self.created_by = created_by
                self.date_changed = date_changed
                self.changes_list = changes_list

        def get_card(self):
                changes= ""
                for i in self.changes_list: 
                        changes += i + ". "
                return (str(self.created_by) + " on " + str(self.date_changed) + " - Effective Changes: " + changes)

        def show(self):
                print(f"{self.index}:\n\tUser: {self.created_by}\n \tDate: {self.date_changed}\n \tChanges: {self.changes_list}\n")

def main():
        tasks = go_scrape()
        tasks_frame = get_tasks_df(tasks)
        tasks_frame.to_csv(filename_for_export, encoding='utf-8') 

if __name__ == "__main__":
        main()

'''
s = getHtml("https://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python")
r = getHtml("http://www.storybench.org/how-to-scrape-reddit-with-python/")
soup = getHtml('https://dev58662.service-now.com/pm')
openBrowser('https://dev58662.service-now.com/pm')

'''