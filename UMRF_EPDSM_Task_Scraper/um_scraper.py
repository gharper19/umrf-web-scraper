'''
NOTE: 
- Rebase commits, clean up commit history
- I would add some verifiers or assertions so we can get some consistency going as far as running.
- PROD TODO: 
        - Only prioritized task number, state, assigned_to, and all activity cards. I can still update descriptions and other details during indiviual page scrape
        - assigned_to vs. assignment group in EPDSM - Assigned_Group doesn't appear on task pages, so i may need to add in a table iterator anyway. 
        - line 250 may be a problem in EPDSM, it correctly cuts first 2 td of each row in table, but also cuts last 4 off the end, if this is important data it will be a problem - Easily solved by fixing fields section or just use indv page scrape
        - Currently exports to csv, but with small set column widths. Can fix col widths(https://www.bing.com/search?q=cant+increase+column+size+in+excel+csv&PC=U316&FORM=CHROMN), but can also be changed to another file type if neccessary.
        - file paths

feild_names = ['number', 'active', 'priority', 'state', 'assigned_to', 'sys_created_by', 'opened_at', 'opened_by', 'assignment_group', 'sys_created_on', 
'short_description', 'description', 'comments_and_work_notes', 'work_notes', 'work_notes_list', 'closed_at', 'closed_by', 'reassignment_count', 'sys_updated_on', 
'sys_updated_by', 'due_date', 'expected_start', 'follow_up', 'sys_class_name', 'time_worked', 'approval_history', 
'additional_assignee_list', 'comments', 'business_duration', 'close_notes', 'company', 'upon_approval', 'upon_reject']

'''
# given the location of python as their first line: #!/usr/bin/python and become executable.
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

config_filename="Scraper_Configuration"
restart_limit=0
list_url = ''

def init_from_config():
# Initializes global variables from config file 
        global USER_NAME
        global USER_PASSWORD
        global list_url
        global filename_for_export 

        global buffer_wait
        global BROWSER_TIMEOUT
        global restart_limit
        global task_page_limit

        # Get config values
        f= open(config_filename + ".txt", "r")
        values = []
        for line in f.readlines():
                if line[0] == "[":
                        check= False 
                        for i in range(len(line)):
                                if line[i] == ':' and check == False:
                                        values += [line[i+1:len(line)-1]]
                                        check= True 
        USER_NAME = values[0].strip()
        USER_PASSWORD = values[1].strip()
        list_url = values[2].strip()
        filename_for_export  = values[3].strip()
        buffer_wait = int(values[4])
        BROWSER_TIMEOUT = int(values[5])
        restart_limit = int(values[6])
        task_page_limit = int(values[7])

def get_browser_driver():
# Creates and returns selenium browser window
        driver= webdriver.Firefox(executable_path='.\\web_drivers\\geckodriver.exe')
        driver.maximize_window()
        driver.set_page_load_timeout(20)
        driver.get(list_url)
        return driver

def run_main_loop():
# Start selenium browser to get pages and return list of task objects - Total scrape Takes average of 20 secs to login
        t=time.time()
        failed_starts= 0
        cont_loop = True
        catalog_tasks =[]
        while (cont_loop==True and failed_starts < restart_limit ):
                browser= get_browser_driver()
                try:
                        try: 
                                # Use Credentials to Login
                                time.sleep(buffer_wait)
                                WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it((0)))
                                
                                # Include explicit wait until uname and password appear 
                                time.sleep(buffer_wait)
                                (browser.find_element_by_name("user_name")).send_keys(USER_NAME)
                                (browser.find_element_by_id("user_password")).send_keys(USER_PASSWORD + Keys.RETURN)
                                time.sleep(buffer_wait)

                        except Exception as e: 
                                print(f"Scraping Loop - Error During Login: {e}")

                        try:
                                # Scrape tasks table and return list
                                browser.switch_to.default_content() 
                                time.sleep(buffer_wait)
                                WebDriverWait(browser, BROWSER_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it("gsft_main"))
                                time.sleep(buffer_wait)
                                catalog_tasks= scrape_task_list(browser.page_source)

                                # Click first task and start scraping individual task pages 
                                browser.find_element_by_xpath("//a[@class='linked formlink']").click()

                        except Exception as e: 
                                print(f"Scraping Loop - Error Clicking on Task Link: {e}")           

                        cont_task= True; num_tasks=0
                        while(cont_task and num_tasks < task_page_limit):
                        # Iterate through tasks and pass each to scrape_task() if already in catalog_tasks lists, else just scrape neccessary data 
                                soup = ""
                                try:
                                        # Switch browser focus to main frame and scrape task html
                                        time.sleep(buffer_wait) 
                                        browser.switch_to.default_content()
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
                except TimeoutError as e:
                        print(f"Main Loop Halted - Timeout Error: {int(time.time()-t)} - {e}")        
                        browser.close()  
                        cont_loop = True
                        failed_starts += 1
                        if failed_starts == restart_limit:
                                print("Main Loop Restart Limit Reached - Cannot start scraping")
                except NoSuchElementException as e:
                        print(f"Main Loop Halted - Not Found Error: {int(time.time()-t)} - {e}")
                        browser.close()  
                        cont_loop = True
                        failed_starts += 1
                        if failed_starts == restart_limit:
                                print("Main Loop Restart Limit Reached - Cannot start scraping")
                except WebDriverException as e:
                        print(f"Main Loop Halted - Web Driver Error: {int(time.time()-t)} - {e}")
                        browser.close()  
                        cont_loop = True
                        failed_starts += 1
                        if failed_starts == restart_limit:
                                print("Main Loop Restart Limit Reached - Cannot start scraping")
                except Exception as e:
                        print(f"Main Loop Halted: {int(time.time()-t)}")
                        browser.close()  
                        cont_loop = True
                        failed_starts += 1
                        if failed_starts == restart_limit:
                                print("Main Loop Restart Limit Reached - Cannot start scraping")

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

def export_tasks_list_csv(tasks): 
# Turns catalog tasks data into a panda dataframe and writes frame to csv 
        df = pd.DataFrame({})
        i = 0
        for task in tasks:
                details = task.task_attributes
                details["Activities"] = str([a.get_card() for a in task.activity_cards])
                detailed_frame= pd.DataFrame(details, index=[i])
                df = pd.concat([df, detailed_frame])
                i += 1
        df.to_csv("exports\\" + filename_for_export + ".csv", encoding='utf-8', index=False)
        return df

class Task:
# Has a Task number, a dictionary of collected attribute details, and a list of TaskActivity objects representing the Task's activities
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
# Contains activity information from each card on individual Task Page. Note that a lower index indicates a more recent activity with 0 being the most recent
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

if __name__ == "__main__":
        init_from_config()
        data= run_main_loop()
        export_tasks_list_csv(data)
