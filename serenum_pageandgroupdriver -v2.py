import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # ← 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime, timedelta
import shutil
import psutil
import random
import re
import pytz
from PIL import Image
import calendar
import pyautogui
import pyperclip
import cv2
import pytesseract
from PIL import ImageGrab
import numpy as np


# Global driver and wait objects
driver = None
wait = None

# Global JSON configuration path
JSON_CONFIG_PATH = r'C:\xampp\htdocs\serenum\pageandgroupauthors.json'
GUI_PATH = r'C:\xampp\htdocs\serenum\files\gui'
# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\xampp\htdocs\serenum\pytesseract\tessdata"


def initialize_driver(mode="headed"):
    """Initialize the Chrome WebDriver."""
    global driver, wait
    print("Closing existing Chrome instances...")
    closed_any = False
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in ['chrome', 'chrome.exe', 'chromedriver', 'chromedriver.exe']:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except psutil.TimeoutExpired:
                    proc.kill()
                closed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if closed_any:
        print("Closed Chrome process(es)")
    time.sleep(1)

    user_data_dir = os.path.expanduser("~/.chrome-user-data")
    profile_directory = "Default"

    chrome_options = Options()
    if mode == "headless":
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
    else:
        chrome_options.add_argument("--start-maximized")
    
    # Specify the Chrome binary path
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    wait = WebDriverWait(driver, 15)
    return driver, wait


def load_urls():
    """Load URLs from pageandgroupaccounts.json based on author from pageandgroupauthors.json."""
    json_path = r"C:\xampp\htdocs\serenum\pageandgroupaccounts.json"
    groupauthors_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    
    try:
        # Load author from pageandgroupauthors.json
        with open(groupauthors_path, 'r') as author_file:
            author_data = json.load(author_file)
            author = author_data.get('author')
            if not author:
                raise Exception("No 'author' key found in pageandgroupauthors.json")
        
        # Load URLs from pageandgroupaccounts.json
        with open(json_path, 'r') as file:
            data = json.load(file)
            if author not in data:
                raise Exception(f"Author '{author}' not found in pageandgroupaccounts.json")
            if "schedule" not in data[author]:
                raise Exception(f"'schedule' key not found for author '{author}' in pageandgroupaccounts.json")
            return data[author]["schedule"][0]
    except Exception as e:
        print(f"Failed to load URLs from JSON: {str(e)}")
        raise

   

def launch_profile():
    """Navigate to the upload post URL, confirm it, and continuously recheck every 2 seconds."""
    global driver, wait
    try:
        uploadpost_url = load_urls()
        # Initial navigation attempt
        while True:
            current_url = driver.current_url
            if uploadpost_url in current_url:
                print(f"Confirmed: URL is {uploadpost_url}.")
                wait.until(
                    EC.presence_of_element_located((By.XPATH, "//textarea | //div[@contenteditable='true'] | //input[@placeholder='Write something...']"))
                )
                print("Navigated to upload post page.")
                break
            else:
                print(f"Current URL ({current_url}) is not the upload post URL.")
                # Reset trackers on initial navigation failure (possible page reload or redirect)
                reset_trackers()
                try:
                    # Check for overlay
                    overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
                    if overlay:
                        print("Detected overlay blocking interaction. Reloading page...")
                        driver.refresh()
                        time.sleep(2)
                        continue
                    # Attempt to find a URL input field and fill it
                    url_input = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='url'] | //input[@placeholder*='URL'] | //input[@name='url']"))
                    )
                    url_input.clear()
                    url_input.send_keys(uploadpost_url)
                    print(f"Filled URL input with: {uploadpost_url}")
                    # Attempt to submit or navigate
                    try:
                        submit_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //button[contains(text(), 'Go')] | //button[contains(text(), 'Navigate')]"))
                        )
                        submit_button.click()
                    except:
                        print("No submit button found, attempting direct navigation.")
                        driver.get(uploadpost_url)
                except:
                    print(f"No URL input field found, navigating directly to {uploadpost_url}.")
                    driver.get(uploadpost_url)
                
                print("Waiting 2 seconds before rechecking URL...")
                time.sleep(2)
        
        # Continuous URL rechecking, caption writing, schedule toggling, media interaction, and file selection
        last_url = driver.current_url  # Track last URL to detect changes
        while True:
            try:
                print("Checking if the URL is the specified")
                current_url = driver.current_url
                if uploadpost_url in current_url:
                    if current_url != last_url:
                        print(f"URL changed from {last_url} to {current_url}. Resetting trackers due to possible page reload.")
                        reset_trackers()
                        last_url = current_url
                    # Write to driverprogress.json before proceeding with operations
                    driver_progress_path = r"C:\xampp\htdocs\serenum\driverprogress.json"
                    progress_data = {
                        "driver": "started",
                        "scheduled": "waiting"
                    }
                    try:
                        with open(driver_progress_path, 'w') as f:
                            json.dump(progress_data, f, indent=4)
                        print(f"Updated {driver_progress_path} with driver: started, scheduled: waiting")
                    except Exception as e:
                        print(f"Failed to write to {driver_progress_path}: {str(e)}")

                    print(f"Recheck confirmed: URL is {uploadpost_url}. Proceeding to write caption, toggle schedule, interact with media, and select file.")
                    print("checking add photo")
                    markjpgs()
                    update_calendar()
                    manage_group_switch()
                    resetgroupswitchandscheduledate()
                    selectgroups()
                    toggleaddphoto()
                    #writecaption_ocr()
                    writecaption_element()
                    toggleschedule()
                    set_webschedule_v2()
                    time.sleep(12093)
                    click_schedule_button()
                    uploadedjpgs()
                else:
                    print(f"Recheck failed: Current URL ({current_url}) does not match {uploadpost_url}. Reloading page and resetting trackers...")
                    reset_trackers()  # Reset trackers on URL mismatch
                    last_url = current_url
                    driver.refresh()  # Reload page
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, "//textarea | //div[@contenteditable='true'] | //input[@placeholder='Write something...']"))
                    )
                    print("Navigated to upload post page after reload.")
                time.sleep(2)
            except KeyboardInterrupt:
                print("Script interrupted by user. Closing browser...")
                raise
            except Exception as e:
                print(f"Error during URL recheck or operations: {str(e)}")
                # Check for overlay
                overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
                if overlay:
                    print("Detected overlay blocking interaction. Reloading page and resetting trackers...")
                    reset_trackers()
                    driver.refresh()
                    time.sleep(2)
                    continue
                # Check if URL changed during error
                current_url = driver.current_url
                if current_url != last_url:
                    print(f"URL changed from {last_url} to {current_url} during error. Resetting trackers and reloading.")
                    reset_trackers()
                    last_url = current_url
                    driver.refresh()
                    time.sleep(2)
                time.sleep(2)  # Continue looping even if an error occurs
                
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            raise  # Re-raise KeyboardInterrupt to handle in main
        print(f"An error occurred: {str(e)}")
        print("Browser will remain open for inspection.")
        raise

def reset_trackers():
    """Reset all function trackers to their initial state, excluding update_calendar."""
    # ---- Caption writers ----
    writecaption_ocr.last_written_caption = None
    if hasattr(writecaption_element, 'last_written_caption'):
        writecaption_element.last_written_caption = None
    writecaption_element.has_written = False

    # ---- set_webschedule_v2 (NEW) ----
    set_webschedule_v2.has_set = False  # ADD THIS LINE

    # ---- toggleaddphoto ----
    toggleaddphoto.is_toggled = False

    # ---- toggleschedule ----
    toggleschedule.is_toggled = False

    # ---- selectmedia ----
    selectmedia.has_uploaded = False

    # ---- selectgroups ----
    selectgroups.is_dropdown_opened = False
    selectgroups.is_see_more_clicked = False
    selectgroups.groups_selected = False
    selectgroups.is_page_selected = False

    print(
        "Reset all function trackers: "
        "last_written_caption (ocr & element), "
        "has_written (writecaption_element), "
        "has_set (set_webschedule_v2), "
        "is_toggled (toggleaddphoto), is_toggled (toggleschedule), "
        "has_uploaded, is_dropdown_opened, is_see_more_clicked, "
        "groups_selected, is_page_selected"
    )

def manage_group_switch():
    """
    Manages the group selection history in uploadgroups.json and schedules in {type}schedules.json
    based on the group_switch and schedule_date fields in pageandgroupauthors.json.
    - If group_switch is 'switch', moves current_selected groups to last_selected and clears current_selected.
    - If group_switch is 'no', clears last_selected data.
    - If schedule_date is 'resumetocurrentdate', transfers data from {type}schedules.json to {type}schedulesrecords.json (appending, not overwriting) if it has actual records, clears {type}schedules.json by writing {}, then calls update_timeschedule().
    - If schedule_date is 'continuefromlastdate', clears {type}schedules.json and retrieves the most recent schedule from {type}schedulesrecords.json to write to {type}schedules.json.
    - If schedule_date is 'none' or invalid, skips schedule-related operations.
    """
    # JSON file paths
    config_json_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    upload_json_path = r"C:\xampp\htdocs\serenum\files\groups\uploadgroups.json"

    # Read pageandgroupauthors.json to get group_switch, author, and schedule_date
    group_switch = 'no'
    author = None
    schedule_date = 'none'
    type_value = None
    if os.path.exists(config_json_path) and os.path.getsize(config_json_path) > 0:
        try:
            with open(config_json_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                group_switch = config_data.get('group_switch', 'no').lower()
                author = config_data.get('author', None)
                schedule_date = config_data.get('schedule_date', 'none').lower()
                type_value = config_data.get('type', None)
                print(f"Read from {config_json_path}: group_switch={group_switch}, author={author}, schedule_date={schedule_date}, type={type_value}")
        except Exception as e:
            print(f"Error reading JSON file {config_json_path}: {str(e)}")
            group_switch = 'no'
            schedule_date = 'none'
            print("Defaulting group_switch to 'no' and schedule_date to 'none' due to error.")
    else:
        print(f"JSON file {config_json_path} does not exist or is empty. Defaulting group_switch to 'no' and schedule_date to 'none'.")

    # Validate group_switch and schedule_date values
    if group_switch not in ['switch', 'no']:
        print(f"Invalid group_switch value: '{group_switch}'. Defaulting to 'no'.")
        group_switch = 'no'
    if schedule_date not in ['resumetocurrentdate', 'continuefromlastdate', 'none']:
        print(f"Invalid schedule_date value: '{schedule_date}'. Defaulting to 'none'.")
        schedule_date = 'none'
    if not author or not type_value:
        print(f"Error: 'author' or 'type' missing in {config_json_path}. Cannot proceed with schedule management.")
        return False

    # Paths for schedules.json and schedulesrecords.json
    schedules_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}schedules.json"
    schedules_records_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}schedulesrecords.json"
    print(f"Schedules path: {schedules_path}")
    print(f"Schedules records path: {schedules_records_path}")

    # Handle schedule_date logic
    if schedule_date == 'none':
        print(f"schedule_date is 'none'. Skipping schedule-related operations.")
    elif schedule_date == 'resumetocurrentdate':
        print(f"schedule_date is 'resumetocurrentdate'. Processing {schedules_path}.")
        # Check if schedules.json exists and has data to transfer
        schedules_data = {}
        schedules_has_data = False
        if os.path.exists(schedules_path) and os.path.getsize(schedules_path) > 0:
            try:
                with open(schedules_path, 'r', encoding='utf-8') as f:
                    schedules_data = json.load(f)
                    # Check if schedules_data has actual records (not just {})
                    if schedules_data and (schedules_data.get('last_schedule') or schedules_data.get('next_schedule')):
                        schedules_has_data = True
                        print(f"Read schedules.json: {schedules_data}")
                    else:
                        print(f"{schedules_path} contains no actual records: {schedules_data}")
            except Exception as e:
                print(f"Error reading {schedules_path}: {str(e)}")
                schedules_data = {}
        
        if schedules_has_data:
            # Read existing schedulesrecords.json
            records_data = []
            if os.path.exists(schedules_records_path) and os.path.getsize(schedules_records_path) > 0:
                try:
                    with open(schedules_records_path, 'r', encoding='utf-8') as f:
                        records_data = json.load(f)
                        if not isinstance(records_data, list):
                            print(f"Error: {schedules_records_path} is not a list. Initializing as empty list.")
                            records_data = []
                except Exception as e:
                    print(f"Error reading {schedules_records_path}: {str(e)}")
                    records_data = []
            
            # Check for duplicates by comparing schedules_data with each record in records_data
            is_duplicate = False
            for record in records_data:
                if record == schedules_data:  # Deep comparison of JSON objects
                    is_duplicate = True
                    print(f"Duplicate found in {schedules_records_path}: {schedules_data}. Skipping append.")
                    break
            
            if not is_duplicate:
                # Append schedules_data to records_data
                records_data.append(schedules_data)
                print(f"Appending to schedulesrecords.json: {schedules_data}")
                
                # Write to schedulesrecords.json
                try:
                    os.makedirs(os.path.dirname(schedules_records_path), exist_ok=True)
                    with open(schedules_records_path, 'w', encoding='utf-8') as f:
                        json.dump(records_data, f, indent=4)
                    print(f"Successfully appended data to {schedules_records_path}")
                except Exception as e:
                    print(f"Error writing to {schedules_records_path}: {str(e)}")
                    return False
            else:
                print(f"Skipping write to {schedules_records_path} due to duplicate record.")
        
        # Clear schedules.json by writing an empty dictionary
        try:
            os.makedirs(os.path.dirname(schedules_path), exist_ok=True)
            with open(schedules_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
            print(f"Successfully cleared {schedules_path}")
        except Exception as e:
            print(f"Error clearing {schedules_path}: {str(e)}")
            return False
        
        # Call update_timeschedule (ensure this function is defined)
        print("Calling update_timeschedule()")
        try:
            update_timeschedule()  # Ensure this function exists
        except NameError:
            print("Error: update_timeschedule() is not defined. Please define this function.")
            return False
    
    elif schedule_date == 'continuefromlastdate':
        print(f"schedule_date is 'continuefromlastdate'. Clearing {schedules_path} and restoring most recent data from {schedules_records_path}.")
        
        # Clear schedules.json by writing an empty dictionary
        try:
            os.makedirs(os.path.dirname(schedules_path), exist_ok=True)
            with open(schedules_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
            print(f"Successfully cleared {schedules_path}")
        except Exception as e:
            print(f"Error clearing {schedules_path}: {str(e)}")
            return False
        
        # Read schedulesrecords.json
        records_data = []
        if os.path.exists(schedules_records_path) and os.path.getsize(schedules_records_path) > 0:
            try:
                with open(schedules_records_path, 'r', encoding='utf-8') as f:
                    records_data = json.load(f)
                    if not isinstance(records_data, list):
                        print(f"Error: {schedules_records_path} is not a list. Cannot restore data.")
                        return False
            except Exception as e:
                print(f"Error reading {schedules_records_path}: {str(e)}")
                return False
            
            if records_data:
                # Find the most recent schedule based on next_schedule date
                most_recent_schedule = None
                latest_date = None
                for record in records_data:
                    next_schedule = record.get('next_schedule', {})
                    if next_schedule and 'date' in next_schedule:
                        try:
                            record_date = datetime.strptime(next_schedule['date'], "%d/%m/%Y")
                            if latest_date is None or record_date > latest_date:
                                latest_date = record_date
                                most_recent_schedule = record
                        except ValueError:
                            print(f"Invalid date format in record: {next_schedule.get('date')}")
                            continue
                
                if most_recent_schedule:
                    # Write the most recent schedule to schedules.json
                    try:
                        with open(schedules_path, 'w', encoding='utf-8') as f:
                            json.dump(most_recent_schedule, f, indent=4)
                        print(f"Successfully restored most recent schedule to {schedules_path}: {most_recent_schedule}")
                    except Exception as e:
                        print(f"Error writing to {schedules_path}: {str(e)}")
                        return False
                else:
                    print(f"No valid records with next_schedule found in {schedules_records_path}. {schedules_path} remains empty.")
            else:
                print(f"{schedules_records_path} is empty. No data to restore. {schedules_path} remains empty.")
                update_calendar_free()
        else:
            print(f"{schedules_records_path} does not exist or is empty. No data to restore. {schedules_path} remains empty.")
            update_calendar_free()

    # Handle group_switch logic for uploadgroups.json
    json_exists = os.path.exists(upload_json_path) and os.path.getsize(upload_json_path) > 0
    upload_data = {
        "groups_selected": {
            "last_selected": [],
            "current_selected": {"1st": "", "2nd": "", "3rd": ""},
            "status": "no groups selected"
        }
    }
    
    if json_exists:
        try:
            with open(upload_json_path, 'r', encoding='utf-8') as f:
                upload_data = json.load(f)
                print(f"Read uploadgroups.json: {upload_data}")
        except Exception as e:
            print(f"Error reading JSON file {upload_json_path}: {str(e)}")
            print("Using default upload_data structure due to error.")

    # Extract current_selected groups
    current_selected = [
        upload_data.get('groups_selected', {}).get('current_selected', {}).get('1st', ''),
        upload_data.get('groups_selected', {}).get('current_selected', {}).get('2nd', ''),
        upload_data.get('groups_selected', {}).get('current_selected', {}).get('3rd', '')
    ]
    current_selected = [name for name in current_selected if name]  # Filter out empty strings
    print(f"Current selected groups: {current_selected}")

    # Handle group_switch logic
    if group_switch == 'switch':
        print("group_switch is 'switch'. Moving current_selected to last_selected and clearing current_selected.")
        last_selected = upload_data.get('groups_selected', {}).get('last_selected', [])
        last_selected = list(set(last_selected + current_selected))  # Merge and remove duplicates
        upload_data['groups_selected']['last_selected'] = last_selected
        upload_data['groups_selected']['current_selected'] = {"1st": "", "2nd": "", "3rd": ""}
        print(f"Updated last_selected: {last_selected}")
        print("Cleared current_selected.")
    else:  # group_switch == 'no'
        print("group_switch is 'no'. Clearing last_selected.")
        upload_data['groups_selected']['last_selected'] = []
        print("last_selected cleared.")

    # Write updated data back to uploadgroups.json
    try:
        os.makedirs(os.path.dirname(upload_json_path), exist_ok=True)
        with open(upload_json_path, 'w', encoding='utf-8') as f:
            json.dump(upload_data, f, indent=4)
        print(f"Successfully updated {upload_json_path} with group_switch action: {group_switch}")
        return True
    except Exception as e:
        print(f"Error writing to JSON file {upload_json_path}: {str(e)}")
        return False

def resetgroupswitchandscheduledate():
    """
    Resets the group_switch to 'no' and schedule_date to 'none' in pageandgroupauthors.json.
    """
    config_json_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    
    # Read existing pageandgroupauthors.json
    config_data = {}
    if os.path.exists(config_json_path) and os.path.getsize(config_json_path) > 0:
        try:
            with open(config_json_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                print(f"Read from {config_json_path}: {config_data}")
        except Exception as e:
            print(f"Error reading JSON file {config_json_path}: {str(e)}")
            print("Initializing with empty config_data due to error.")
    
    # Update fields
    config_data['group_switch'] = 'no'
    config_data['schedule_date'] = 'none'
    print(f"Updated config_data: group_switch='no', schedule_date='none'")
    
    # Write back to pageandgroupauthors.json
    try:
        os.makedirs(os.path.dirname(config_json_path), exist_ok=True)
        with open(config_json_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        print(f"Successfully updated {config_json_path} with group_switch='no' and schedule_date='none'")
        return True
    except Exception as e:
        print(f"Error writing to JSON file {config_json_path}: {str(e)}")
        return False

def selectgroups():
    """Locate and click the dropdown element associated with 'Post to' text, check pageandgroupauthors.json for page, group, and group_types fields, select or unselect page profile under 'Post to Facebook and Instagram' based on page field, and based on group and group_types fields: if group is 'include' and group_types is 'uk', select the three groups with the highest member counts containing 'british', 'uk', 'england', or 'united kingdom' (not in last_selected and not containing 'usa' or 'australia'); if group_types is 'others', select groups not containing these UK terms or containing both UK terms and 'usa' or 'australia'; if group is 'none', unselect all groups; verify selections, save to JSON, and click Save."""
    global driver, wait
    
    # Initialize trackers if not already set
    if not hasattr(selectgroups, 'is_dropdown_opened'):
        selectgroups.is_dropdown_opened = False
    if not hasattr(selectgroups, 'is_see_more_clicked'):
        selectgroups.is_see_more_clicked = False
    if not hasattr(selectgroups, 'groups_selected'):
        selectgroups.groups_selected = False
    if not hasattr(selectgroups, 'is_page_selected'):
        selectgroups.is_page_selected = False
    if not hasattr(selectgroups, 'failed_attempts'):
        selectgroups.failed_attempts = 0

    # JSON file path for groups
    json_path = r"C:\xampp\htdocs\serenum\files\groups\uploadgroups.json"

    # Check if JSON exists and read last_selected
    last_selected = []
    json_exists = os.path.exists(json_path) and os.path.getsize(json_path) > 0
    if json_exists:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                last_selected = data.get('groups_selected', {}).get('last_selected', [])
                print(f"Read last_selected from JSON: {last_selected}")
        except Exception as e:
            print(f"Error reading JSON file {json_path}: {str(e)}")
            last_selected = []

    # Check if function should retry or skip
    if selectgroups.is_dropdown_opened or selectgroups.is_see_more_clicked or selectgroups.groups_selected:
        selectgroups.failed_attempts += 1
        if selectgroups.failed_attempts >= 3:
            print("selectgroups has failed too many times (3 attempts). Skipping to prevent blocking other functions.")
            return False
        print(f"Retry attempt {selectgroups.failed_attempts} due to prior state (is_dropdown_opened={selectgroups.is_dropdown_opened}, is_see_more_clicked={selectgroups.is_see_more_clicked}, groups_selected={selectgroups.groups_selected})")

    # Check pageandgroupauthors.json for page, group, and group_types fields
    page_config = 'none'
    group_config = 'none'
    group_types = 'others'  # Default to 'others' if not specified
    if os.path.exists(JSON_CONFIG_PATH) and os.path.getsize(JSON_CONFIG_PATH) > 0:
        try:
            with open(JSON_CONFIG_PATH, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                page_config = config_data.get('page', 'none')
                group_config = config_data.get('group', 'none')
                group_types = config_data.get('group_types', 'others').lower()
                print(f"Read config from {JSON_CONFIG_PATH}: page={page_config}, group={group_config}, group_types={group_types}")
        except Exception as e:
            print(f"Error reading JSON file {JSON_CONFIG_PATH}: {str(e)}")
            page_config = 'none'
            group_config = 'none'
            group_types = 'others'
    else:
        print(f"JSON file {JSON_CONFIG_PATH} does not exist or is empty. Defaulting page to 'none', group to 'none', group_types to 'others'.")

    # Validate group_types
    if group_types not in ['uk', 'others']:
        print(f"Invalid group_types value: '{group_types}'. Defaulting to 'others'.")
        group_types = 'others'

    # Define UK-related keywords and exclusionary country names
    uk_keywords = ['british', 'uk', 'england', 'united kingdom']
    exclude_countries = ['usa', 'australia']

    # Handle dropdown opening
    if selectgroups.is_dropdown_opened:
        print("Dropdown already opened. Skipping dropdown click operation.")
    else:
        try:
            # Locate the container wrapping 'Post to' text
            post_to_container = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to')]"
                ))
            )
            print("Found 'Post to' container.")

            # Find the dropdown element within or near the container
            dropdown = None
            for attempt in range(3):
                try:
                    dropdown = wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to')]//following::select | "
                            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to')]//following::*[@role='combobox'] | "
                            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to')]//following::*[@aria-haspopup='listbox'] | "
                            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to')]//following::div[contains(@class, 'dropdown') or contains(@class, 'select')] | "
                            "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to')]//following::button[contains(@aria-label, 'dropdown') or contains(@class, 'dropdown')]"
                        ))
                    )
                    print("Found dropdown element associated with 'Post to'.")
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} to locate dropdown failed: {str(e)}")
                    if attempt == 2:
                        print("Failed to locate dropdown after 3 attempts. Checking for overlay...")
                        overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
                        if overlay:
                            print("Detected overlay. Attempting to dismiss...")
                            try:
                                close_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Close') or contains(text(), 'Close') or contains(@class, 'close')]")
                                close_button.click()
                                time.sleep(1)
                                print("Overlay dismissed. Retrying dropdown location...")
                                continue
                            except:
                                print("Could not dismiss overlay. Skipping dropdown click.")
                                return False
                    time.sleep(1)

            if not dropdown:
                print("No dropdown found after retries. Proceeding without opening dropdown.")
                return False

            # Scroll to the dropdown and click
            for attempt in range(3):
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                    time.sleep(0.5)
                    dropdown.click()
                    print("Clicked dropdown to open the window.")
                    selectgroups.is_dropdown_opened = True
                    print("Updated tracker: is_dropdown_opened set to True")
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} to click dropdown failed: {str(e)}")
                    if attempt == 2:
                        print("Failed to click dropdown after 3 attempts. Proceeding without opening dropdown.")
                        return False
                    time.sleep(1)
            
            time.sleep(3)  # Pause to ensure dropdown opens
        except Exception as e:
            print(f"Failed to process dropdown operation: {str(e)}")
            return False

    # Handle page profile selection
    if selectgroups.is_page_selected and page_config == 'none':
        print("Page profile already selected but page config is 'none'. Attempting to unselect.")
        try:
            dropdown_content = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'dropdown') or contains(@class, 'menu') or @role='menu' or @role='listbox']"
                    "[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to facebook and instagram')]"
                ))
            )
            print("Found dropdown content with 'Post to Facebook and Instagram'.")

            page_profile = None
            for attempt in range(3):
                try:
                    page_profile = wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            ".//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to facebook and instagram')]//following::div[contains(@class, 'page') or contains(@class, 'profile') or @role='option' or contains(@class, 'item')][not(contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'instagram') and not(contains(@class, 'instagram')))] | "
                            ".//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to facebook and instagram')]//following::li[contains(@class, 'page') or contains(@class, 'profile') or @role='option'][not(contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'instagram') and not(contains(@class, 'instagram')))]"
                        )),
                        dropdown_content
                    )
                    tag = page_profile.tag_name
                    class_attr = page_profile.get_attribute('class') or ''
                    role = page_profile.get_attribute('role') or ''
                    text = page_profile.text.strip()[:100]
                    print(f"Found page profile: Tag={tag}, Class={class_attr}, Role={role}, Text='{text}'")
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} to locate page profile failed: {str(e)}")
                    if attempt == 2:
                        print("Failed to locate page profile after 3 attempts. Proceeding to group handling.")
                        break
                    time.sleep(1)

            if not page_profile:
                print("No page profile found. Proceeding to group handling.")
            else:
                is_selected = False
                try:
                    aria_checked = page_profile.get_attribute('aria-checked')
                    if aria_checked and aria_checked.lower() == 'true':
                        is_selected = True
                    else:
                        checkbox = page_profile.find_elements(By.XPATH, ".//input[@type='checkbox']")
                        if checkbox and checkbox[0].is_selected():
                            is_selected = True
                        else:
                            class_attr = page_profile.get_attribute('class') or ''
                            if any(sel_class in class_attr for sel_class in ['selected', 'checked', 'active', 'x1yztbdb', 'x1e558r4']):
                                is_selected = True
                            else:
                                checkmark = page_profile.find_elements(By.XPATH, ".//*[contains(@class, 'checkmark') or contains(@class, 'selected') or contains(@class, 'icon')]")
                                if checkmark:
                                    is_selected = True
                except Exception as sel_e:
                    print(f"Error checking page selection: {sel_e}")

                if is_selected:
                    try:
                        clickable = page_profile.find_elements(By.XPATH, ".//input[@type='checkbox']") or \
                                   page_profile.find_elements(By.XPATH, ".//label | .//div[@role='checkbox'] | .//div[@data-testid or contains(@class, 'clickable') or contains(@class, 'selectable')]") or \
                                   [page_profile]
                        clickable = clickable[0]
                        tag = clickable.tag_name
                        class_attr = clickable.get_attribute('class') or ''
                        role = clickable.get_attribute('role') or ''
                        data_testid = clickable.get_attribute('data-testid') or ''
                        print(f"Attempting to unselect page profile: {text}, Tag={tag}, Class={class_attr}, Role={role}, Data-testid={data_testid}")

                        for attempt in range(3):
                            try:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clickable)
                                time.sleep(1.0)
                                driver.execute_script("arguments[0].click();", clickable)
                                time.sleep(1.5)

                                is_selected_now = False
                                aria_checked = page_profile.get_attribute('aria-checked')
                                if aria_checked and aria_checked.lower() == 'true':
                                    is_selected_now = True
                                else:
                                    checkbox = page_profile.find_elements(By.XPATH, ".//input[@type='checkbox']")
                                    if checkbox and checkbox[0].is_selected():
                                        is_selected_now = True
                                    else:
                                        class_attr = page_profile.get_attribute('class') or ''
                                        if any(sel_class in class_attr for sel_class in ['selected', 'checked', 'active', 'x1yztbdb', 'x1e558r4']):
                                            is_selected_now = True
                                        else:
                                            checkmark = page_profile.find_elements(By.XPATH, ".//*[contains(@class, 'checkmark') or contains(@class, 'selected') or contains(@class, 'icon')]")
                                            if checkmark:
                                                is_selected_now = True

                                if not is_selected_now:
                                    print(f"Unselected page profile: {text} (Verified)")
                                    selectgroups.is_page_selected = False
                                    print("Updated tracker: is_page_selected set to False")
                                    break
                                else:
                                    print(f"Attempt {attempt + 1} failed to verify unselection for page profile: {text}")
                            except Exception as click_e:
                                print(f"Attempt {attempt + 1} failed to unselect page profile {text}: {str(click_e)}")
                                if attempt == 2:
                                    print(f"Failed to unselect page profile after retries: {text}")
                    except Exception as e:
                        print(f"Failed to process unselection for page profile {text}: {str(e)}")
                else:
                    print(f"Page profile {text} is not selected. No unselection needed.")
                    selectgroups.is_page_selected = False
                    print("Updated tracker: is_page_selected set to False")
        except Exception as e:
            print(f"Failed to locate or process page profile for unselection: {str(e)}")
            print("Proceeding to group handling despite unselection failure.")
    elif page_config == 'include' and not selectgroups.is_page_selected:
        print("Page config is 'include'. Attempting to select page profile.")
        try:
            dropdown_content = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'dropdown') or contains(@class, 'menu') or @role='menu' or @role='listbox']"
                    "[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to facebook and instagram')]"
                ))
            )
            print("Found dropdown content with 'Post to Facebook and Instagram'.")

            page_profile = None
            for attempt in range(3):
                try:
                    page_profile = wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            ".//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to facebook and instagram')]//following::div[contains(@class, 'page') or contains(@class, 'profile') or @role='option' or contains(@class, 'item')][not(contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'instagram') and not(contains(@class, 'instagram')))] | "
                            ".//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to facebook and instagram')]//following::li[contains(@class, 'page') or contains(@class, 'profile') or @role='option'][not(contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'instagram') and not(contains(@class, 'instagram')))]"
                        )),
                        dropdown_content
                    )
                    tag = page_profile.tag_name
                    class_attr = page_profile.get_attribute('class') or ''
                    role = page_profile.get_attribute('role') or ''
                    text = page_profile.text.strip()[:100]
                    print(f"Found page profile: Tag={tag}, Class={class_attr}, Role={role}, Text='{text}'")
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} to locate page profile failed: {str(e)}")
                    if attempt == 2:
                        print("Failed to locate page profile after 3 attempts. Proceeding to group handling.")
                        break
                    time.sleep(1)

            if page_profile:
                for attempt in range(3):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", page_profile)
                        time.sleep(0.5)
                        driver.execute_script("arguments[0].click();", page_profile)
                        print(f"Selected page profile: {text}")
                        selectgroups.is_page_selected = True
                        print("Updated tracker: is_page_selected set to True")
                        break
                    except Exception as e:
                        print(f"Attempt {attempt + 1} to click page profile failed: {str(e)}")
                        if attempt == 2:
                            print("Failed to click page profile after 3 attempts.")
                    time.sleep(1)
                
                time.sleep(1)  # Pause to ensure selection
        except Exception as e:
            print(f"Failed to locate or select page profile under 'Post to Facebook and Instagram': {str(e)}")
            print("Proceeding to group handling despite page selection failure.")
    else:
        print(f"Page config is '{page_config}' and is_page_selected is {selectgroups.is_page_selected}. No page selection or unselection needed.")

    # Handle group selection
    if group_config == 'none':
        print("Group config is 'none'. Attempting to unselect all groups.")
        if selectgroups.is_see_more_clicked:
            print("'See more groups' already clicked. Skipping click operation.")
        else:
            try:
                see_more_groups = None
                for attempt in range(3):
                    try:
                        see_more_groups = wait.until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'see more groups')] | "
                                "//*[contains(@aria-label, 'See more groups') or contains(@aria-label, 'see more groups')]"
                            ))
                        )
                        print("Found 'See more groups' element.")
                        break
                    except Exception as e:
                        print(f"Attempt {attempt + 1} to locate 'See more groups' failed: {str(e)}")
                        if attempt == 2:
                            print("Failed to locate 'See more groups' after 3 attempts. Checking for overlay...")
                            overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
                            if overlay:
                                print("Detected overlay. Attempting to dismiss...")
                                try:
                                    close_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Close') or contains(text(), 'Close') or contains(@class, 'close')]")
                                    close_button.click()
                                    time.sleep(1)
                                    print("Overlay dismissed. Retrying...")
                                    continue
                                except:
                                    print("Could not dismiss overlay. Skipping 'See more groups' click.")
                                    return False
                        time.sleep(1)

                if not see_more_groups:
                    print("No 'See more groups' element found. Proceeding without opening group popup.")
                    return False

                for attempt in range(3):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", see_more_groups)
                        time.sleep(0.5)
                        see_more_groups.click()
                        print("Clicked 'See more groups' to open its window.")
                        selectgroups.is_see_more_clicked = True
                        print("Updated tracker: is_see_more_clicked set to True")
                        break
                    except Exception as e:
                        print(f"Attempt {attempt + 1} to click 'See more groups' failed: {str(e)}")
                        if attempt == 2:
                            print("Failed to click 'See more groups' after 3 attempts.")
                            return False
                        time.sleep(1)
                
                time.sleep(4)  # Pause to allow the popup to fully load
            except Exception as e:
                print(f"Failed to process 'See more groups' operation: {str(e)}")
                return False

        try:
            popup_window = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//div[contains(@class, 'modal') or @role='dialog' or contains(@class, 'sheet') or contains(@class, 'popover')]"
                    "[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'publish to facebook groups') or "
                    "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'choose up to three groups')]"
                ))
            )
            print("Found 'Publish to Facebook groups' popup window.")

            group_elements = popup_window.find_elements(By.XPATH, 
                ".//div[@data-testid='group_picker_item'] | "
                ".//div[contains(@class, 'group') or contains(@class, 'group-item') or contains(@class, 'item') or @role='option' or @role='listitem' or contains(@class, 'clickable') or contains(@class, 'selectable')] | "
                ".//li[contains(@class, 'group') or contains(@class, 'item') or @role='option' or @role='listitem'] | "
                ".//div[descendant::*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'public group') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'private group')]]"
            )
            
            selected_groups = []
            group_element_map = {}
            seen_texts = set()
            for i, elem in enumerate(group_elements, 1):
                try:
                    text = elem.text.strip() or elem.get_attribute('aria-label') or ''
                    lines = text.split('\n')
                    group_name = lines[0].strip() if lines else text
                    if (group_name and 
                        group_name.lower() not in seen_texts and
                        not any(phrase in group_name.lower() for phrase in ['publish to facebook groups', 'choose up to three groups', 'close', 'done', 'cancel'])):
                        seen_texts.add(group_name.lower())
                        group_element_map[group_name] = elem
                        
                        is_selected = False
                        try:
                            aria_checked = elem.get_attribute('aria-checked')
                            if aria_checked and aria_checked.lower() == 'true':
                                is_selected = True
                            else:
                                checkbox = elem.find_elements(By.XPATH, ".//input[@type='checkbox']")
                                if checkbox and checkbox[0].is_selected():
                                    is_selected = True
                                else:
                                    class_attr = elem.get_attribute('class') or ''
                                    if any(sel_class in class_attr for sel_class in ['selected', 'checked', 'active', 'x1yztbdb', 'x1e558r4']):
                                        is_selected = True
                                    else:
                                        checkmark = elem.find_elements(By.XPATH, ".//*[contains(@class, 'checkmark') or contains(@class, 'selected') or contains(@class, 'icon')]")
                                        if checkmark:
                                            is_selected = True
                        except Exception as sel_e:
                            print(f"Error checking selection for group {i}: {sel_e}")
                        
                        if is_selected:
                            selected_groups.append(group_name)
                            print(f"Group {i}: {group_name} (Selected)")
                except Exception as e:
                    print(f"Group {i}: Error extracting text - {str(e)}")

            print(f"Number of selected groups: {len(selected_groups)}")
            if selected_groups:
                print(f"Selected groups to unselect: {selected_groups}")

            for group_name in selected_groups:
                elem = group_element_map.get(group_name)
                if elem:
                    try:
                        clickable = elem.find_elements(By.XPATH, ".//input[@type='checkbox']") or \
                                   elem.find_elements(By.XPATH, ".//label | .//div[@role='checkbox'] | .//div[@data-testid or contains(@class, 'clickable') or contains(@class, 'selectable')]") or \
                                   [elem]
                        clickable = clickable[0]
                        
                        tag = clickable.tag_name
                        class_attr = clickable.get_attribute('class') or ''
                        role = clickable.get_attribute('role') or ''
                        data_testid = clickable.get_attribute('data-testid') or ''
                        print(f"Attempting to unselect group: {group_name}, Tag={tag}, Class={class_attr}, Role={role}, Data-testid={data_testid}")

                        for attempt in range(3):
                            try:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clickable)
                                time.sleep(1.0)
                                driver.execute_script("arguments[0].click();", clickable)
                                time.sleep(1.5)
                                
                                is_selected_now = False
                                aria_checked = elem.get_attribute('aria-checked')
                                if aria_checked and aria_checked.lower() == 'true':
                                    is_selected_now = True
                                else:
                                    checkbox = elem.find_elements(By.XPATH, ".//input[@type='checkbox']")
                                    if checkbox and checkbox[0].is_selected():
                                        is_selected_now = True
                                    else:
                                        class_attr = elem.get_attribute('class') or ''
                                        if any(sel_class in class_attr for sel_class in ['selected', 'checked', 'active', 'x1yztbdb', 'x1e558r4']):
                                            is_selected_now = True
                                        else:
                                            checkmark = elem.find_elements(By.XPATH, ".//*[contains(@class, 'checkmark') or contains(@class, 'selected') or contains(@class, 'icon')]")
                                            if checkmark:
                                                is_selected_now = True
                                
                                if not is_selected_now:
                                    print(f"Unselected group: {group_name} (Verified)")
                                    break
                                else:
                                    print(f"Attempt {attempt + 1} failed to verify unselection for group: {group_name}")
                            except Exception as click_e:
                                print(f"Attempt {attempt + 1} failed to unselect group {group_name}: {str(click_e)}")
                                if attempt == 2:
                                    print(f"Failed to unselect group after retries: {group_name}")
                    except Exception as e:
                        print(f"Failed to process unselection for group {group_name}: {str(e)}")

            try:
                save_button = None
                for attempt in range(3):
                    try:
                        save_button = wait.until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                ".//*[text()='Save'][not(contains(@class, 'x1q0g3np') or contains(@class, 'x1i10hfl'))] | "
                                ".//*[contains(@aria-label, 'Save')][not(contains(@class, 'x1q0g3np') or contains(@class, 'x1i10hfl'))] | "
                                ".//*[text()='Cancel']//following::*[text()='Save'][1] | "
                                ".//div[@role='button' and (text()='Save' or contains(@aria-label, 'Save'))][not(contains(@class, 'x1q0g3np') or contains(@class, 'x1i10hfl'))]"
                            )),
                            popup_window
                        )
                        tag = save_button.tag_name
                        class_attr = save_button.get_attribute('class') or ''
                        role = save_button.get_attribute('role') or ''
                        aria_label = save_button.get_attribute('aria-label') or ''
                        aria_disabled = save_button.get_attribute('aria-disabled') or ''
                        text = save_button.text.strip()[:100]
                        print(f"Found 'Save' button (Attempt {attempt + 1}): Tag={tag}, Class={class_attr}, Role={role}, Aria-label={aria_label}, Aria-disabled={aria_disabled}, Text='{text}'")
                        break
                    except (TimeoutException, StaleElementReferenceException) as e:
                        print(f"Attempt {attempt + 1} to locate 'Save' button failed: {str(e)}")
                        if attempt == 2:
                            print("Failed to locate 'Save' button after retries.")
                            return False
                        time.sleep(1)

                if save_button and aria_disabled.lower() == 'true':
                    print("Save button is disabled. Cannot proceed with click.")
                    return False
                
                for attempt in range(3):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
                        time.sleep(0.7)
                        driver.execute_script("arguments[0].click();", save_button)
                        print(f"Clicked 'Save' button to confirm no group selections (Attempt {attempt + 1}).")
                        break
                    except Exception as click_e:
                        print(f"Attempt {attempt + 1} to click 'Save' button failed: {str(click_e)}")
                        if attempt == 2:
                            print("Failed to click 'Save' button after retries.")
                            return False
                
                try:
                    time.sleep(3)
                    popup_still_present = driver.find_elements(By.XPATH, 
                        "//div[contains(@class, 'modal') or @role='dialog' or contains(@class, 'sheet') or contains(@class, 'popover')]"
                        "[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'publish to facebook groups') or "
                        "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'choose up to three groups')]"
                    )
                    if not popup_still_present:
                        print("Popup window closed successfully.")
                    else:
                        print("Popup window did not close after clicking Save.")
                        return False
                except Exception as e:
                    print(f"Error verifying popup closure: {str(e)}")
                    return False
                
                json_data = {
                    "groups_selected": {
                        "last_selected": last_selected,
                        "current_selected": {
                            "1st": "",
                            "2nd": "",
                            "3rd": ""
                        },
                        "status": "no groups selected"
                    }
                }
                try:
                    if not json_exists:
                        print(f"JSON file does not exist. Creating {json_path}")
                        os.makedirs(os.path.dirname(json_path), exist_ok=True)
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(json_data, f, indent=4)
                        print("Created JSON file with no groups selected.")
                    else:
                        with open(json_path, 'r', encoding='utf-8') as f:
                            existing_data = json.load(f)
                        existing_data['groups_selected']['current_selected'] = json_data['groups_selected']['current_selected']
                        existing_data['groups_selected']['status'] = "no groups selected"
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(existing_data, f, indent=4)
                        print("Updated JSON file with no groups selected.")
                except Exception as e:
                    print(f"Error writing to JSON file: {str(e)}")

                selectgroups.groups_selected = True
                selectgroups.failed_attempts = 0  # Reset failed attempts on success
                print("Updated tracker: groups_selected set to True, failed_attempts reset to 0")
                return True

            except Exception as e:
                print(f"Failed to locate or click 'Save' button: {str(e)}")
                return False

        except Exception as e:
            print(f"Failed to locate popup window or process groups: {str(e)}")
            return False

    elif group_config == 'include':
        print(f"Group config is 'include' with group_types '{group_types}'. Proceeding with group selection.")
        if selectgroups.is_see_more_clicked:
            print("'See more groups' already clicked. Skipping click operation.")
        else:
            try:
                see_more_groups = None
                for attempt in range(3):
                    try:
                        see_more_groups = wait.until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'see more groups')] | "
                                "//*[contains(@aria-label, 'See more groups') or contains(@aria-label, 'see more groups')]"
                            ))
                        )
                        print("Found 'See more groups' element.")
                        break
                    except Exception as e:
                        print(f"Attempt {attempt + 1} to locate 'See more groups' failed: {str(e)}")
                        if attempt == 2:
                            print("Failed to locate 'See more groups' after 3 attempts. Checking for overlay...")
                            overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
                            if overlay:
                                print("Detected overlay. Attempting to dismiss...")
                                try:
                                    close_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Close') or contains(text(), 'Close') or contains(@class, 'close')]")
                                    close_button.click()
                                    time.sleep(1)
                                    print("Overlay dismissed. Retrying...")
                                    continue
                                except:
                                    print("Could not dismiss overlay. Skipping 'See more groups' click.")
                                    return False
                        time.sleep(1)

                if not see_more_groups:
                    print("No 'See more groups' element found. Proceeding without opening group popup.")
                    return False

                for attempt in range(3):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", see_more_groups)
                        time.sleep(0.5)
                        see_more_groups.click()
                        print("Clicked 'See more groups' to open its window.")
                        selectgroups.is_see_more_clicked = True
                        print("Updated tracker: is_see_more_clicked set to True")
                        break
                    except Exception as e:
                        print(f"Attempt {attempt + 1} to click 'See more groups' failed: {str(e)}")
                        if attempt == 2:
                            print("Failed to click 'See more groups' after 3 attempts.")
                            return False
                        time.sleep(1)
                
                time.sleep(4)  # Pause to allow the popup to fully load
            except Exception as e:
                print(f"Failed to process 'See more groups' operation: {str(e)}")
                return False

        if selectgroups.groups_selected:
            print("Groups already selected. Skipping selection operation.")
            selectgroups.failed_attempts = 0  # Reset failed attempts if groups already selected
            print("Updated tracker: failed_attempts reset to 0")
            return True

        try:
            popup_window = wait.until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//div[contains(@class, 'modal') or @role='dialog' or contains(@class, 'sheet') or contains(@class, 'popover')]"
                    "[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'publish to facebook groups') or "
                    "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'choose up to three groups')]"
                ))
            )
            print("Found 'Publish to Facebook groups' popup window.")

            group_elements = popup_window.find_elements(By.XPATH, 
                ".//div[@data-testid='group_picker_item'] | "
                ".//div[contains(@class, 'group') or contains(@class, 'group-item') or contains(@class, 'item') or @role='option' or @role='listitem' or contains(@class, 'clickable') or contains(@class, 'selectable')] | "
                ".//li[contains(@class, 'group') or contains(@class, 'item') or @role='option' or @role='listitem'] | "
                ".//div[descendant::*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'public group') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'private group')]]"
            )
            
            group_data = []
            group_element_map = {}
            selected_groups = []
            seen_texts = set()
            for i, elem in enumerate(group_elements, 1):
                try:
                    text = elem.text.strip() or elem.get_attribute('aria-label') or ''
                    lines = text.split('\n')
                    group_name = lines[0].strip() if lines else text
                    member_count = 0
                    if len(lines) > 1:
                        member_text = lines[1].strip()
                        match = re.search(r'(\d+[\d,]*)\s*members', member_text)
                        if match:
                            member_count = int(match.group(1).replace(',', ''))
                    
                    if (group_name and 
                        group_name.lower() not in seen_texts and
                        not any(phrase in group_name.lower() for phrase in ['publish to facebook groups', 'choose up to three groups', 'close', 'done', 'cancel'])):
                        seen_texts.add(group_name.lower())
                        group_data.append((group_name, member_count, elem))
                        group_element_map[group_name] = elem
                        
                        is_selected = False
                        try:
                            aria_checked = elem.get_attribute('aria-checked')
                            if aria_checked and aria_checked.lower() == 'true':
                                is_selected = True
                            else:
                                checkbox = elem.find_elements(By.XPATH, ".//input[@type='checkbox']")
                                if checkbox and checkbox[0].is_selected():
                                    is_selected = True
                                else:
                                    class_attr = elem.get_attribute('class') or ''
                                    if any(sel_class in class_attr for sel_class in ['selected', 'checked', 'active', 'x1yztbdb', 'x1e558r4']):
                                        is_selected = True
                                    else:
                                        checkmark = elem.find_elements(By.XPATH, ".//*[contains(@class, 'checkmark') or contains(@class, 'selected') or contains(@class, 'icon')]")
                                        if checkmark:
                                            is_selected = True
                        except Exception as sel_e:
                            print(f"Error checking selection for group {i}: {sel_e}")
                        
                        if is_selected:
                            selected_groups.append(group_name)
                            print(f"Group {i}: {group_name} ({member_count} members, Selected)")
                        else:
                            print(f"Group {i}: {group_name} ({member_count} members)")
                except Exception as e:
                    print(f"Group {i}: Error extracting text - {str(e)}")
            
            group_count = len(group_data)
            print(f"Total groups found in popup: {group_count}")
            print(f"Number of selected groups: {len(selected_groups)}")

            filtered_group_data = []
            if group_types == 'uk':
                print("Filtering groups containing UK keywords (british, uk, england, united kingdom) and excluding groups with 'usa' or 'australia'")
                for group_name, member_count, elem in group_data:
                    name_lower = group_name.lower()
                    has_uk_keyword = any(keyword in name_lower for keyword in uk_keywords)
                    has_exclude_country = any(country in name_lower for country in exclude_countries)
                    if has_uk_keyword and not has_exclude_country:
                        filtered_group_data.append((group_name, member_count, elem))
            else:  # group_types == 'others'
                print("Filtering groups: excluding pure UK groups (british, uk, england, united kingdom without usa or australia), including groups with both UK keywords and 'usa' or 'australia', or no UK keywords")
                for group_name, member_count, elem in group_data:
                    name_lower = group_name.lower()
                    has_uk_keyword = any(keyword in name_lower for keyword in uk_keywords)
                    has_exclude_country = any(country in name_lower for country in exclude_countries)
                    if not has_uk_keyword or (has_uk_keyword and has_exclude_country):
                        filtered_group_data.append((group_name, member_count, elem))
            
            print(f"Number of filtered groups ({group_types}): {len(filtered_group_data)}")
            if filtered_group_data:
                print(f"Filtered groups ({group_types}):")
                for i, (name, count, _) in enumerate(filtered_group_data, 1):
                    print(f"{i}. {name}: {count} members")

            filtered_group_data.sort(key=lambda x: x[1], reverse=True)
            print(f"Filtered groups sorted by member count ({group_types}):")
            for i, (name, count, _) in enumerate(filtered_group_data, 1):
                print(f"{i}. {name}: {count} members")

            target_groups = []
            for group_name, _, _ in filtered_group_data:
                if group_name not in last_selected and len(target_groups) < 3:
                    target_groups.append(group_name)
            
            if not target_groups:
                print(f"No eligible {group_types} groups available (all filtered groups in last_selected).")
                return False
            
            print(f"Target groups to select (not in last_selected, {group_types}): {target_groups}")

            current_selected = []
            for group_name in selected_groups:
                if group_name in target_groups:
                    current_selected.append(group_name)
                    print(f"Keeping pre-selected group in top 3: {group_name}")
                else:
                    elem = group_element_map.get(group_name)
                    if elem:
                        try:
                            clickable = elem.find_elements(By.XPATH, ".//input[@type='checkbox']") or \
                                       elem.find_elements(By.XPATH, ".//label | .//div[@role='checkbox'] | .//div[@data-testid or contains(@class, 'clickable') or contains(@class, 'selectable')]") or \
                                       [elem]
                            clickable = clickable[0]
                            
                            tag = clickable.tag_name
                            class_attr = clickable.get_attribute('class') or ''
                            role = clickable.get_attribute('role') or ''
                            data_testid = clickable.get_attribute('data-testid') or ''
                            print(f"Attempting to unselect group: {group_name}, Tag={tag}, Class={class_attr}, Role={role}, Data-testid={data_testid}")

                            for attempt in range(3):
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clickable)
                                    time.sleep(1.0)
                                    driver.execute_script("arguments[0].click();", clickable)
                                    time.sleep(1.5)
                                    
                                    is_selected_now = False
                                    aria_checked = elem.get_attribute('aria-checked')
                                    if aria_checked and aria_checked.lower() == 'true':
                                        is_selected_now = True
                                    else:
                                        checkbox = elem.find_elements(By.XPATH, ".//input[@type='checkbox']")
                                        if checkbox and checkbox[0].is_selected():
                                            is_selected_now = True
                                        else:
                                            class_attr = elem.get_attribute('class') or ''
                                            if any(sel_class in class_attr for sel_class in ['selected', 'checked', 'active', 'x1yztbdb', 'x1e558r4']):
                                                is_selected_now = True
                                            else:
                                                checkmark = elem.find_elements(By.XPATH, ".//*[contains(@class, 'checkmark') or contains(@class, 'selected') or contains(@class, 'icon')]")
                                                if checkmark:
                                                    is_selected_now = True
                                    
                                    if not is_selected_now:
                                        print(f"Unselected group: {group_name} (Verified)")
                                        break
                                    else:
                                        print(f"Attempt {attempt + 1} failed to verify unselection for group: {group_name}")
                                except Exception as click_e:
                                    print(f"Attempt {attempt + 1} failed to unselect group {group_name}: {str(click_e)}")
                                    if attempt == 2:
                                        print(f"Failed to unselect group after retries: {group_name}")
                        except Exception as e:
                            print(f"Failed to process unselection for group {group_name}: {str(e)}")

            newly_selected = []
            for group_name in target_groups:
                if group_name in current_selected:
                    continue
                elem = group_element_map.get(group_name)
                if not elem:
                    continue
                try:
                    clickable = elem.find_elements(By.XPATH, ".//input[@type='checkbox']") or \
                               elem.find_elements(By.XPATH, ".//label | .//div[@role='checkbox'] | .//div[@data-testid or contains(@class, 'clickable') or contains(@class, 'selectable')]") or \
                               [elem]
                    clickable = clickable[0]
                    
                    tag = clickable.tag_name
                    class_attr = clickable.get_attribute('class') or ''
                    role = clickable.get_attribute('role') or ''
                    data_testid = clickable.get_attribute('data-testid') or ''
                    print(f"Attempting to click group: {group_name}, Tag={tag}, Class={class_attr}, Role={role}, Data-testid={data_testid}")

                    for attempt in range(3):
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clickable)
                            time.sleep(1.0)
                            driver.execute_script("arguments[0].click();", clickable)
                            time.sleep(1.5)
                            
                            is_selected_now = False
                            aria_checked = elem.get_attribute('aria-checked')
                            if aria_checked and aria_checked.lower() == 'true':
                                is_selected_now = True
                            else:
                                checkbox = elem.find_elements(By.XPATH, ".//input[@type='checkbox']")
                                if checkbox and checkbox[0].is_selected():
                                    is_selected_now = True
                                else:
                                    class_attr = elem.get_attribute('class') or ''
                                    if any(sel_class in class_attr for sel_class in ['selected', 'checked', 'active', 'x1yztbdb', 'x1e558r4']):
                                        is_selected_now = True
                                    else:
                                        checkmark = elem.find_elements(By.XPATH, ".//*[contains(@class, 'checkmark') or contains(@class, 'selected') or contains(@class, 'icon')]")
                                        if checkmark:
                                            is_selected_now = True
                            
                            if is_selected_now:
                                newly_selected.append(group_name)
                                current_selected.append(group_name)
                                print(f"Selected group: {group_name} (Verified)")
                                break
                            else:
                                print(f"Attempt {attempt + 1} failed to verify selection for group: {group_name}")
                        except Exception as click_e:
                            print(f"Attempt {attempt + 1} failed to click group {group_name}: {str(click_e)}")
                            if attempt == 2:
                                print(f"Failed to select group after retries: {group_name}")
                except Exception as e:
                    print(f"Failed to process group {group_name}: {str(e)}")
            
            if newly_selected:
                print(f"Newly selected groups: {', '.join(newly_selected)}")
            else:
                print("No additional groups were selected.")
            
            print(f"Final number of selected groups: {len(current_selected)}")
            if current_selected:
                print(f"Final selected groups: {', '.join(current_selected)}")

            json_data = {
                "groups_selected": {
                    "last_selected": last_selected,
                    "current_selected": {
                        "1st": current_selected[0] if len(current_selected) > 0 else "",
                        "2nd": current_selected[1] if len(current_selected) > 1 else "",
                        "3rd": current_selected[2] if len(current_selected) > 2 else ""
                    },
                    "status": f"selection verified ({group_types})"
                }
            }

            try:
                if not json_exists:
                    print(f"JSON file does not exist. Creating {json_path}")
                    os.makedirs(os.path.dirname(json_path), exist_ok=True)
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=4)
                    print(f"Created JSON file with current_selected: {json_data['groups_selected']['current_selected']}")
                else:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                    existing_data['groups_selected']['current_selected'] = json_data['groups_selected']['current_selected']
                    existing_data['groups_selected']['status'] = f"selection verified ({group_types})"
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(existing_data, f, indent=4)
                    print(f"Updated JSON file with current_selected: {json_data['groups_selected']['current_selected']}")
            except Exception as e:
                print(f"Error writing to JSON file: {str(e)}")

            try:
                save_button = None
                for attempt in range(3):
                    try:
                        save_button = wait.until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                ".//*[text()='Save'][not(contains(@class, 'x1q0g3np') or contains(@class, 'x1i10hfl'))] | "
                                ".//*[contains(@aria-label, 'Save')][not(contains(@class, 'x1q0g3np') or contains(@class, 'x1i10hfl'))] | "
                                ".//*[text()='Cancel']//following::*[text()='Save'][1] | "
                                ".//div[@role='button' and (text()='Save' or contains(@aria-label, 'Save'))][not(contains(@class, 'x1q0g3np') or contains(@class, 'x1i10hfl'))]"
                            )),
                            popup_window
                        )
                        tag = save_button.tag_name
                        class_attr = save_button.get_attribute('class') or ''
                        role = save_button.get_attribute('role') or ''
                        aria_label = save_button.get_attribute('aria-label') or ''
                        aria_disabled = save_button.get_attribute('aria-disabled') or ''
                        text = save_button.text.strip()[:100]
                        print(f"Found 'Save' button (Attempt {attempt + 1}): Tag={tag}, Class={class_attr}, Role={role}, Aria-label={aria_label}, Aria-disabled={aria_disabled}, Text='{text}'")
                        break
                    except (TimeoutException, StaleElementReferenceException) as e:
                        print(f"Attempt {attempt + 1} to locate 'Save' button failed: {str(e)}")
                        if attempt == 2:
                            print("Failed to locate 'Save' button after retries.")
                            return False
                        time.sleep(1)

                if save_button and aria_disabled.lower() == 'true':
                    print("Save button is disabled. Cannot proceed with click.")
                    return False
                
                for attempt in range(3):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
                        time.sleep(0.7)
                        driver.execute_script("arguments[0].click();", save_button)
                        print(f"Clicked 'Save' button to confirm group selections (Attempt {attempt + 1}).")
                        break
                    except Exception as click_e:
                        print(f"Attempt {attempt + 1} to click 'Save' button failed: {str(click_e)}")
                        if attempt == 2:
                            print("Failed to click 'Save' button after retries.")
                            return False
                
                try:
                    time.sleep(1)
                    popup_still_present = driver.find_elements(By.XPATH, 
                        "//div[contains(@class, 'modal') or @role='dialog' or contains(@class, 'sheet') or contains(@class, 'popover')]"
                        "[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'publish to facebook groups') or "
                        "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'choose up to three groups')]"
                    )
                    if not popup_still_present:
                        print("Popup window closed successfully.")
                    else:
                        print("Popup window did not close after clicking Save.")
                        return False
                except Exception as e:
                    print(f"Error verifying popup closure: {str(e)}")
                    return False
                
            except Exception as e:
                print(f"Failed to locate or click 'Save' button: {str(e)}")
                return False

            if group_count == 0:
                print("No group elements found in the popup.")
                return False
            
            selectgroups.groups_selected = True
            selectgroups.failed_attempts = 0  # Reset failed attempts on success
            print("Updated tracker: groups_selected set to True, failed_attempts reset to 0")
            return True

        except Exception as e:
            print(f"Failed to locate popup window or process groups: {str(e)}")
            return False
    else:
        print(f"Invalid group config: '{group_config}'. Defaulting to no group selection.")
        return False



def update_calendar_free():
    """Update the calendar and write to JSON, unconditionally."""

    # Get current date and time
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    current_time_12hour = now.strftime("%I:%M %p").lower()
    current_time_24hour = now.strftime("%H:%M")
    current_date = datetime.strptime(f"{current_day:02d}/{current_month:02d}/{current_year}", "%d/%m/%Y")
    
    print(f"Current date and time: {current_date.strftime('%d/%m/%Y')} {current_time_12hour} ({current_time_24hour})")
    
    # Read pageandgroupauthors.json
    pageauthors_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    print(f"Reading pageandgroupauthors.json from {pageauthors_path}")
    try:
        with open(pageauthors_path, 'r') as f:
            pageauthors = json.load(f)
    except FileNotFoundError:
        print(f"Error: pageandgroupauthors.json not found at {pageauthors_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: pageandgroupauthors.json contains invalid JSON")
        return
    
    author = pageauthors['author']
    type_value = pageauthors['type']
    print(f"Author: {author}, Type: {type_value}")
    
    # Read timeorders.json
    timeorders_path = r"C:\xampp\htdocs\serenum\timeorders.json"
    print(f"Reading timeorders.json from {timeorders_path}")
    try:
        with open(timeorders_path, 'r') as f:
            timeorders_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: timeorders.json not found at {timeorders_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: timeorders.json contains invalid JSON")
        return
    
    # Select time slots based on type
    if type_value not in timeorders_data:
        print(f"Error: Type '{type_value}' not found in timeorders.json")
        return
    timeorders = timeorders_data[type_value]
    print(f"Time slots loaded from timeorders.json for type '{type_value}':")
    for t in timeorders:
        print(f"  - {t['12hours']} ({t['24hours']})")
    
    # Sort timeorders by 24-hour format for consistent ordering
    sorted_timeorders = sorted(timeorders, key=lambda x: x["24hours"])
    
    # Find ALL time slots after current time for TODAY
    time_ahead_today = []
    current_time = datetime.strptime(current_time_24hour, "%H:%M")
    current_datetime = datetime.combine(current_date, current_time.time())
    
    print(f"Searching for time slots after {current_time_24hour}")
    for t in sorted_timeorders:
        slot_time = datetime.strptime(t["24hours"], "%H:%M")
        delta = slot_time - current_time
        minutes_distance = int(delta.total_seconds() / 60)
        
        # TODAY: Collect all slots >= current time AND before midnight (exclude 00:00)
        if minutes_distance >= 0 and t["24hours"] != "00:00":
            slot = {
                "id": f"{current_day:02d}_{t['24hours'].replace(':', '')}",
                "12hours": t["12hours"],
                "24hours": t["24hours"],
                "minutes_distance": minutes_distance,
                "consideration": f"passed {t['12hours']}" if minutes_distance >= 50 else f"skip {t['12hours']}"
            }
            time_ahead_today.append(slot)
            print(f"Slot TODAY: {t['12hours']} ({t['24hours']}): id={slot['id']}, minutes_distance={minutes_distance}, consideration={slot['consideration']}")
    
    # Calculate next month and year
    next_month = current_month + 1 if current_month < 12 else 1
    next_year = current_year if current_month < 12 else current_year + 1
    
    # Create calendar data structure
    calendar_data = {
        "calendars": [
            {
                "year": current_year,
                "month": calendar.month_name[current_month],
                "days": [
                    {
                        "week": week_idx + 1,
                        "days": [
                            {
                                "day": {
                                    "date": f"{day:02d}/{current_month:02d}/{current_year}" if day != 0 else None,
                                    "time_12hour": current_time_12hour if day == current_day else "00:00 pm" if day != 0 else None,
                                    "time_24hour": current_time_24hour if day == current_day else "00:00" if day != 0 else None,
                                    "time_ahead": (
                                        time_ahead_today if day == current_day else
                                        [
                                            {
                                                "id": f"{day:02d}_{t['24hours'].replace(':', '')}",
                                                "12hours": t["12hours"],
                                                "24hours": t["24hours"],
                                                "minutes_distance": int((
                                                    datetime.strptime(
                                                        f"{day:02d}/{current_month:02d}/{current_year} {t['24hours']}",
                                                        "%d/%m/%Y %H:%M"
                                                    ) - current_datetime
                                                ).total_seconds() / 60),
                                                "consideration": f"passed {t['12hours']}"
                                            } for t in sorted_timeorders
                                        ] if day != 0 else []
                                    )
                                } if day != 0 and day >= current_day else {"day": None}
                            } for day in week
                        ]
                    } for week_idx, week in enumerate(calendar.monthcalendar(current_year, current_month))
                    if any(day >= current_day or day == 0 for day in week)
                ]
            },
            {
                "year": next_year,
                "month": calendar.month_name[next_month],
                "days": [
                    {
                        "week": week_idx + 1,
                        "days": [
                            {
                                "day": {
                                    "date": f"{day:02d}/{next_month:02d}/{next_year}" if day != 0 else None,
                                    "time_12hour": "00:00 pm" if day != 0 else None,
                                    "time_24hour": "00:00" if day != 0 else None,
                                    "time_ahead": [
                                        {
                                            "id": f"{day:02d}_{t['24hours'].replace(':', '')}",
                                            "12hours": t["12hours"],
                                            "24hours": t["24hours"],
                                            "minutes_distance": int((
                                                datetime.strptime(
                                                    f"{day:02d}/{next_month:02d}/{next_year} {t['24hours']}",
                                                    "%d/%m/%Y %H:%M"
                                                ) - current_datetime
                                            ).total_seconds() / 60),
                                            "consideration": f"passed {t['12hours']}"
                                        } for t in sorted_timeorders
                                    ] if day != 0 else []
                                } if day != 0 else {"day": None}
                            } for day in week
                        ]
                    } for week_idx, week in enumerate(calendar.monthcalendar(next_year, next_month))
                ]
            }
        ]
    }
    
    # Define output path with author and type
    output_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}calendar.json"
    print(f"Writing calendar data to {output_path}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write to JSON file
    with open(output_path, 'w') as f:
        json.dump(calendar_data, f, indent=4)
    print(f"Calendar data successfully written to {output_path}")
    
    # Call schedule_time
    update_timeschedule()

def update_calendar():
    """Update the calendar and write to JSON, conditional on driverprogress.json status."""
    check_schedule_time()
    # Check driverprogress.json for condition
    driver_progress_path = r"C:\xampp\htdocs\serenum\driverprogress.json"
    try:
        with open(driver_progress_path, 'r') as f:
            progress_data = json.load(f)
        if not (progress_data.get("driver") == "started" and progress_data.get("scheduled") == "successfully"):
            print(f"Skipping update_calendar: driverprogress.json does not match required condition (driver: started, scheduled: successfully). Current: {progress_data}")
            return
        print("driverprogress.json condition met: {'driver': 'started', 'scheduled': 'successfully'}")
    except FileNotFoundError:
        print(f"Error: {driver_progress_path} not found. Skipping update_calendar.")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: {driver_progress_path} contains invalid JSON. Skipping update_calendar.")
        return
    except Exception as e:
        print(f"Error reading {driver_progress_path}: {str(e)}. Skipping update_calendar.")
        return

    # Get current date and time
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    current_time_12hour = now.strftime("%I:%M %p").lower()
    current_time_24hour = now.strftime("%H:%M")
    current_date = datetime.strptime(f"{current_day:02d}/{current_month:02d}/{current_year}", "%d/%m/%Y")
    
    print(f"Current date and time: {current_date.strftime('%d/%m/%Y')} {current_time_12hour} ({current_time_24hour})")
    
    # Read pageandgroupauthors.json
    pageauthors_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    print(f"Reading pageandgroupauthors.json from {pageauthors_path}")
    try:
        with open(pageauthors_path, 'r') as f:
            pageauthors = json.load(f)
    except FileNotFoundError:
        print(f"Error: pageandgroupauthors.json not found at {pageauthors_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: pageandgroupauthors.json contains invalid JSON")
        return
    
    author = pageauthors['author']
    type_value = pageauthors['type']
    print(f"Author: {author}, Type: {type_value}")
    
    # Read timeorders.json
    timeorders_path = r"C:\xampp\htdocs\serenum\timeorders.json"
    print(f"Reading timeorders.json from {timeorders_path}")
    try:
        with open(timeorders_path, 'r') as f:
            timeorders_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: timeorders.json not found at {timeorders_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: timeorders.json contains invalid JSON")
        return
    
    # Select time slots based on type
    if type_value not in timeorders_data:
        print(f"Error: Type '{type_value}' not found in timeorders.json")
        return
    timeorders = timeorders_data[type_value]
    print(f"Time slots loaded from timeorders.json for type '{type_value}':")
    for t in timeorders:
        print(f"  - {t['12hours']} ({t['24hours']})")
    
    # Sort timeorders by 24-hour format for consistent ordering
    sorted_timeorders = sorted(timeorders, key=lambda x: x["24hours"])
    
    # Find ALL time slots after current time for TODAY
    time_ahead_today = []
    current_time = datetime.strptime(current_time_24hour, "%H:%M")
    current_datetime = datetime.combine(current_date, current_time.time())
    
    print(f"Searching for time slots after {current_time_24hour}")
    for t in sorted_timeorders:
        slot_time = datetime.strptime(t["24hours"], "%H:%M")
        delta = slot_time - current_time
        minutes_distance = int(delta.total_seconds() / 60)
        
        # TODAY: Collect all slots >= current time AND before midnight (exclude 00:00)
        if minutes_distance >= 0 and t["24hours"] != "00:00":
            slot = {
                "id": f"{current_day:02d}_{t['24hours'].replace(':', '')}",
                "12hours": t["12hours"],
                "24hours": t["24hours"],
                "minutes_distance": minutes_distance,
                "consideration": f"passed {t['12hours']}" if minutes_distance >= 50 else f"skip {t['12hours']}"
            }
            time_ahead_today.append(slot)
            print(f"Slot TODAY: {t['12hours']} ({t['24hours']}): id={slot['id']}, minutes_distance={minutes_distance}, consideration={slot['consideration']}")
    
    # Calculate next month and year
    next_month = current_month + 1 if current_month < 12 else 1
    next_year = current_year if current_month < 12 else current_year + 1
    
    # Create calendar data structure
    calendar_data = {
        "calendars": [
            {
                "year": current_year,
                "month": calendar.month_name[current_month],
                "days": [
                    {
                        "week": week_idx + 1,
                        "days": [
                            {
                                "day": {
                                    "date": f"{day:02d}/{current_month:02d}/{current_year}" if day != 0 else None,
                                    "time_12hour": current_time_12hour if day == current_day else "00:00 pm" if day != 0 else None,
                                    "time_24hour": current_time_24hour if day == current_day else "00:00" if day != 0 else None,
                                    "time_ahead": (
                                        time_ahead_today if day == current_day else
                                        [
                                            {
                                                "id": f"{day:02d}_{t['24hours'].replace(':', '')}",
                                                "12hours": t["12hours"],
                                                "24hours": t["24hours"],
                                                "minutes_distance": int((
                                                    datetime.strptime(
                                                        f"{day:02d}/{current_month:02d}/{current_year} {t['24hours']}",
                                                        "%d/%m/%Y %H:%M"
                                                    ) - current_datetime
                                                ).total_seconds() / 60),
                                                "consideration": f"passed {t['12hours']}"
                                            } for t in sorted_timeorders
                                        ] if day != 0 else []
                                    )
                                } if day != 0 and day >= current_day else {"day": None}
                            } for day in week
                        ]
                    } for week_idx, week in enumerate(calendar.monthcalendar(current_year, current_month))
                    if any(day >= current_day or day == 0 for day in week)
                ]
            },
            {
                "year": next_year,
                "month": calendar.month_name[next_month],
                "days": [
                    {
                        "week": week_idx + 1,
                        "days": [
                            {
                                "day": {
                                    "date": f"{day:02d}/{next_month:02d}/{next_year}" if day != 0 else None,
                                    "time_12hour": "00:00 pm" if day != 0 else None,
                                    "time_24hour": "00:00" if day != 0 else None,
                                    "time_ahead": [
                                        {
                                            "id": f"{day:02d}_{t['24hours'].replace(':', '')}",
                                            "12hours": t["12hours"],
                                            "24hours": t["24hours"],
                                            "minutes_distance": int((
                                                datetime.strptime(
                                                    f"{day:02d}/{next_month:02d}/{next_year} {t['24hours']}",
                                                    "%d/%m/%Y %H:%M"
                                                ) - current_datetime
                                            ).total_seconds() / 60),
                                            "consideration": f"passed {t['12hours']}"
                                        } for t in sorted_timeorders
                                    ] if day != 0 else []
                                } if day != 0 else {"day": None}
                            } for day in week
                        ]
                    } for week_idx, week in enumerate(calendar.monthcalendar(next_year, next_month))
                ]
            }
        ]
    }
    
    # Define output path with author and type
    output_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}calendar.json"
    print(f"Writing calendar data to {output_path}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write to JSON file
    with open(output_path, 'w') as f:
        json.dump(calendar_data, f, indent=4)
    print(f"Calendar data successfully written to {output_path}")
    
    # Call schedule_time
    update_timeschedule()
def update_timeschedule():
    """Determine the next schedule time and write to schedules.json."""
    # Get current date and time
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    current_time_24hour = now.strftime("%H:%M")
    current_time_12hour = now.strftime("%I:%M %p").lower()
    current_date = now.strftime("%d/%m/%Y")
    
    print(f"Current date and time: {current_date} {current_time_12hour} ({current_time_24hour})")
    
    # Read pageandgroupauthors.json to get author and type
    pageauthors_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    print(f"Reading pageandgroupauthors.json from {pageauthors_path}")
    try:
        with open(pageauthors_path, 'r') as f:
            pageauthors = json.load(f)
    except FileNotFoundError:
        print(f"Error: pageandgroupauthors.json not found at {pageauthors_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: pageandgroupauthors.json contains invalid JSON")
        return
    
    author = pageauthors['author']
    type_value = pageauthors['type']
    print(f"Author: {author}, Type: {type_value}")
    
    # Read calendar.json based on author and type
    calendar_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}calendar.json"
    print(f"Reading calendar.json from {calendar_path}")
    try:
        with open(calendar_path, 'r') as f:
            calendar_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: calendar.json not found at {calendar_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: calendar.json contains invalid JSON")
        return
    
    # Read existing schedules.json to get the last recorded slot and previous next_schedule
    schedules_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}schedules.json"
    last_schedule = None
    previous_next_schedule = None
    if os.path.exists(schedules_path):
        try:
            with open(schedules_path, 'r') as f:
                existing_data = json.load(f)
                if isinstance(existing_data, dict):
                    if 'last_schedule' in existing_data:
                        last_schedule = existing_data['last_schedule']
                        print(f"Previous slot (last_schedule): {last_schedule}")
                    if 'next_schedule' in existing_data:
                        previous_next_schedule = existing_data['next_schedule']
                        print(f"Previous next_schedule: {previous_next_schedule}")
                    else:
                        print(f"Error: 'next_schedule' field missing in schedules.json")
                else:
                    print(f"Error: Invalid format in schedules.json, expected dict with 'last_schedule' and 'next_schedule'")
        except json.decoder.JSONDecodeError:
            print(f"schedules.json is empty or contains invalid JSON, treating as non-existent")
    
    # Read timeorders.json
    timeorders_path = r"C:\xampp\htdocs\serenum\timeorders.json"
    print(f"Reading timeorders.json from {timeorders_path}")
    try:
        with open(timeorders_path, 'r') as f:
            timeorders_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: timeorders.json not found at {timeorders_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: timeorders.json contains invalid JSON")
        return
    
    # Select time slots based on type
    if type_value not in timeorders_data:
        print(f"Error: Type '{type_value}' not found in timeorders.json")
        return
    timeorders = timeorders_data[type_value]
    print(f"Time orders for {type_value}: {timeorders}")
    
    # Sort timeorders by 24-hour format
    sorted_timeorders = sorted(timeorders, key=lambda x: x["24hours"])
    
    # Find the next "passed" time slot
    current_time = datetime.strptime(current_time_24hour, "%H:%M")
    current_datetime = datetime.combine(datetime.strptime(current_date, "%d/%m/%Y"), current_time.time())
    
    next_slot = None
    found_last_slot = False if last_schedule else True
    found_previous_next_slot = False if previous_next_schedule else True
    last_schedule_date = None
    last_schedule_time = None
    previous_next_schedule_date = None
    previous_next_schedule_time = None
    
    if last_schedule:
        try:
            last_schedule_date = datetime.strptime(last_schedule["date"], "%d/%m/%Y")
            last_schedule_time = datetime.strptime(last_schedule["time_24hour"], "%H:%M")
        except ValueError:
            print(f"Invalid date or time format in last_schedule: {last_schedule}")
            found_last_slot = True  # Treat invalid last_schedule as if it doesn't exist
    
    if previous_next_schedule:
        try:
            previous_next_schedule_date = datetime.strptime(previous_next_schedule["date"], "%d/%m/%Y")
            previous_next_schedule_time = datetime.strptime(previous_next_schedule["time_24hour"], "%H:%M")
        except ValueError:
            print(f"Invalid date or time format in previous_next_schedule: {previous_next_schedule}")
            found_previous_next_slot = True  # Treat invalid previous_next_schedule as if it doesn't exist
    
    # Iterate through calendar to find the next valid slot
    for cal in calendar_data["calendars"]:
        for week in cal["days"]:
            for day_entry in week["days"]:
                day = day_entry.get("day")
                if not day or (day.get("day") is None and not day.get("date")):
                    continue
                
                date = day.get("date")
                if not date:
                    continue
                
                try:
                    slot_date = datetime.strptime(date, "%d/%m/%Y")
                except ValueError:
                    print(f"Invalid date format in calendar: {date}")
                    continue
                
                # Skip dates before today
                if slot_date.date() < current_datetime.date():
                    continue
                
                # Process time slots for the date
                for slot in day.get("time_ahead", []):
                    print(f"Checking slot: {slot}")
                    # Validate slot time
                    if slot["24hours"] not in [t["24hours"] for t in sorted_timeorders]:
                        print(f"Slot {slot['24hours']} not in timeorders, skipping")
                        continue
                    
                    # Only consider slots marked as "passed"
                    if "passed" not in slot["consideration"].lower():
                        print(f"Slot {slot['24hours']} not marked as 'passed', skipping")
                        continue
                    
                    # For today, ensure the slot is at least 50 minutes ahead
                    if slot_date.date() == current_datetime.date():
                        try:
                            slot_time = datetime.strptime(slot["24hours"], "%H:%M")
                            delta = slot_time - current_time
                            minutes_distance = int(delta.total_seconds() / 60)
                            if minutes_distance < 50:
                                print(f"Slot {slot['24hours']} is {minutes_distance} minutes away, too soon, skipping")
                                continue
                        except ValueError:
                            print(f"Invalid time format in slot: {slot['24hours']}")
                            continue
                    
                    # If last_schedule exists, check if we need to skip until after it
                    if last_schedule and not found_last_slot:
                        if (last_schedule["date"] == date and 
                            last_schedule["time_24hour"] == slot["24hours"] and 
                            last_schedule["id"] == slot["id"]):
                            found_last_slot = True
                            print(f"Found last_schedule match: {slot}")
                            continue
                        # If no match, check if we've passed last_schedule's date/time
                        slot_time = datetime.strptime(slot["24hours"], "%H:%M")
                        if (slot_date.date() > last_schedule_date.date() or 
                            (slot_date.date() == last_schedule_date.date() and slot_time > last_schedule_time)):
                            found_last_slot = True
                            print(f"Passed last_schedule date/time, proceeding with slot: {slot}")
                    
                    # If previous_next_schedule exists, check if we need to skip it
                    if previous_next_schedule and not found_previous_next_slot:
                        if (previous_next_schedule["date"] == date and 
                            previous_next_schedule["time_24hour"] == slot["24hours"] and 
                            previous_next_schedule["id"] == slot["id"]):
                            found_previous_next_slot = True
                            print(f"Found previous_next_schedule match: {slot}")
                            continue
                        # If no match, check if we've passed previous_next_schedule's date/time
                        slot_time = datetime.strptime(slot["24hours"], "%H:%M")
                        if (slot_date.date() > previous_next_schedule_date.date() or 
                            (slot_date.date() == previous_next_schedule_date.date() and slot_time > previous_next_schedule_time)):
                            found_previous_next_slot = True
                            print(f"Passed previous_next_schedule date/time, proceeding with slot: {slot}")
                    
                    # Select this slot only if we've passed both last_schedule and previous_next_schedule
                    if found_last_slot and found_previous_next_slot:
                        next_slot = {
                            "id": slot["id"],
                            "date": date,
                            "time_12hour": slot["12hours"],
                            "time_24hour": slot["24hours"]
                        }
                        print(f"Found next passed slot: {next_slot['time_12hour']} ({next_slot['time_24hour']}) on {next_slot['date']}, id={next_slot['id']}")
                        break
                
                if next_slot:
                    break
            if next_slot:
                break
        if next_slot:
            break
    
    # If no next slot is found
    if not next_slot:
        print("No further passed time slots found in the calendar")
        return
    
    # Prepare the output JSON with last_schedule set to previous next_schedule
    output_data = {
        "last_schedule": previous_next_schedule if previous_next_schedule else last_schedule,  # Use previous next_schedule
        "next_schedule": next_slot  # Update to the new next_slot
    }
    
    # Write the new data to schedules.json
    output_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}schedules.json"
    print(f"Writing to schedules.json at {output_path}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the output data
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"Successfully wrote previous and current slots to {output_path}")
def check_schedule_time():
    """Check if the next schedule in schedules.json is behind the current time."""
    # Get current date and time
    now = datetime.now()
    current_time_24hour = now.strftime("%H:%M")
    current_date = now.strftime("%d/%m/%Y")
    current_datetime = datetime.strptime(f"{current_date} {current_time_24hour}", "%d/%m/%Y %H:%M")
    
    print(f"Current date and time: {current_date} {current_time_24hour}")
    
    # Read pageandgroupauthors.json to get author and type
    pageauthors_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    print(f"Reading pageandgroupauthors.json from {pageauthors_path}")
    try:
        with open(pageauthors_path, 'r') as f:
            pageauthors = json.load(f)
    except FileNotFoundError:
        print(f"Error: pageandgroupauthors.json not found at {pageauthors_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: pageandgroupauthors.json contains invalid JSON")
        return
    
    author = pageauthors['author']
    type_value = pageauthors['type']
    print(f"Author: {author}, Type: {type_value}")
    
    # Read schedules.json based on author and type
    schedules_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}schedules.json"
    print(f"Reading schedules.json from {schedules_path}")
    if not os.path.exists(schedules_path):
        print(f"Error: schedules.json not found at {schedules_path}")
        update_calendar_free()
        return
    
    try:
        with open(schedules_path, 'r') as f:
            schedules_data = json.load(f)
    except json.decoder.JSONDecodeError:
        print(f"Error: schedules.json contains invalid JSON")
        return
    
    # Check for next_schedule
    if 'next_schedule' not in schedules_data:
        print(f"Error: 'next_schedule' field missing in schedules.json")
        update_calendar_free()
        return
    
    next_schedule = schedules_data['next_schedule']
    if not next_schedule:
        print("No next schedule found in schedules.json")
        return
    
    # Extract next schedule date and time
    try:
        next_schedule_date = next_schedule['date']
        next_schedule_time = next_schedule['time_24hour']
        next_schedule_datetime = datetime.strptime(f"{next_schedule_date} {next_schedule_time}", "%d/%m/%Y %H:%M")
    except (KeyError, ValueError) as e:
        print(f"Error: Invalid date or time format in next_schedule: {next_schedule}. Error: {str(e)}")
        return
    
    # Compare with current time
    if next_schedule_datetime < current_datetime:
        print(f"Next schedule is behind the current time: {next_schedule_date} {next_schedule_time} is earlier than {current_date} {current_time_24hour}")
        update_timeschedule()
    else:
        print(f"Next schedule is valid: {next_schedule_date} {next_schedule_time} is not behind {current_date} {current_time_24hour}")





def markjpgs():
    # Load configuration from JSON
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        processpathfrom = config.get('processpathfrom', 'freshjpgs')  # Default to 'freshjpgs'
        freshjpgs_directory = config['inputpath'].replace('authorvalue', author)
        output_dir = config['outputpath'].replace('authorvalue', author)
    except Exception as e:
        print(f"Failed to load or parse {JSON_CONFIG_PATH}: {e}")
        return

    # Verify that output path ends with the author folder
    if not output_dir.endswith(author):
        print(f"Error: outputpath ({output_dir}) does not end with author folder '{author}'")
        return

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except Exception as e:
            print(f"Failed to create output directory {output_dir}: {e}")
            return

    # Supported image extensions
    image_extensions = {'.jpg', '.png', '.jpeg', '.bmp', '.gif', '.tiff'}
    directory = None

    if processpathfrom == 'uploadedjpgs':
        # Construct base path for uploadedjpgs
        base_uploaded_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}"
        if not os.path.exists(base_uploaded_path):
            print(f"Base uploaded jpgs directory does not exist: {base_uploaded_path}")
            # Fall back to freshjpgs
            processpathfrom = 'freshjpgs'
            directory = freshjpgs_directory
        else:
            # Find valid date folders
            date_folders = []
            for f in os.listdir(base_uploaded_path):
                if os.path.isdir(os.path.join(base_uploaded_path, f)):
                    try:
                        # Test if folder name matches DD-Month-YYYY format
                        datetime.strptime(f, "%d-%B-%Y")
                        date_folders.append(f)
                    except ValueError:
                        print(f"Skipping invalid date folder: {f}")
                        continue

            if not date_folders:
                print(f"No valid date folders found in {base_uploaded_path}")
                # Check base author folder for files
                base_files = [f for f in os.listdir(base_uploaded_path) if f.lower().endswith(tuple(image_extensions))]
                if base_files:
                    # Create oldest date folder (today's date)
                    oldest_date_folder = datetime.now().strftime("%d-%B-%Y")
                    oldest_date_path = os.path.join(base_uploaded_path, oldest_date_folder)
                    os.makedirs(oldest_date_path, exist_ok=True)
                    print(f"Created oldest date folder: {oldest_date_path}")
                    # Move files to oldest date folder
                    for file in base_files:
                        src = os.path.join(base_uploaded_path, file)
                        dst = os.path.join(oldest_date_path, file)
                        shutil.move(src, dst)
                        print(f"Moved {file} to {oldest_date_path}")
                    date_folders.append(oldest_date_folder)
                else:
                    print(f"No valid image files found in base folder {base_uploaded_path}")
                    # Fall back to freshjpgs
                    processpathfrom = 'freshjpgs'
                    directory = freshjpgs_directory
            else:
                # Sort folders by date (oldest first)
                try:
                    date_folders.sort(key=lambda x: datetime.strptime(x, "%d-%B-%Y"))
                except ValueError as e:
                    print(f"Error sorting date folders in {base_uploaded_path}: {e}")
                    # Fall back to freshjpgs
                    processpathfrom = 'freshjpgs'
                    directory = freshjpgs_directory

                # Process folders from oldest to newest until a folder with >20 images is found
                for date_folder in date_folders:
                    directory = os.path.join(base_uploaded_path, date_folder)
                    if not os.path.exists(directory):
                        print(f"Directory does not exist: {directory}")
                        continue
                    # Check for valid image files
                    image_files = [f for f in os.listdir(directory) if f.lower().endswith(tuple(image_extensions))]
                    if len(image_files) > 20:
                        print(f"Processing directory with {len(image_files)} images: {directory}")
                        break  # Found a folder with >20 images, proceed with this directory
                    else:
                        print(f"Directory {directory} has {len(image_files)} images (<=20), moving to next date folder")
                        directory = None

                if not directory:
                    print(f"No date folder in {base_uploaded_path} has more than 20 images")
                    # Check base author folder for files
                    base_files = [f for f in os.listdir(base_uploaded_path) if f.lower().endswith(tuple(image_extensions))]
                    if base_files:
                        # Use the oldest date folder or create a new one
                        oldest_date_folder = date_folders[0] if date_folders else datetime.now().strftime("%d-%B-%Y")
                        oldest_date_path = os.path.join(base_uploaded_path, oldest_date_folder)
                        os.makedirs(oldest_date_path, exist_ok=True)
                        print(f"Using/created oldest date folder: {oldest_date_path}")
                        # Move files to oldest date folder
                        for file in base_files:
                            src = os.path.join(base_uploaded_path, file)
                            dst = os.path.join(oldest_date_path, file)
                            shutil.move(src, dst)
                            print(f"Moved {file} to {oldest_date_path}")
                        # Recount files in the oldest date folder
                        directory = oldest_date_path
                        image_files = [f for f in os.listdir(directory) if f.lower().endswith(tuple(image_extensions))]
                        if len(image_files) > 20:
                            print(f"Processing directory with {len(image_files)} images after moving files: {directory}")
                        else:
                            print(f"Directory {directory} has {len(image_files)} images (<=20) after moving files")
                            # Fall back to freshjpgs
                            processpathfrom = 'freshjpgs'
                            directory = freshjpgs_directory
                    else:
                        print(f"No valid image files found in base folder {base_uploaded_path}")
                        # Fall back to freshjpgs
                        processpathfrom = 'freshjpgs'
                        directory = freshjpgs_directory

    if processpathfrom == 'freshjpgs':
        directory = freshjpgs_directory
        # Verify input directory ends with author
        if not directory.endswith(author):
            print(f"Error: input directory ({directory}) does not end with author folder '{author}'")
            return

    if not directory or not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return

    # Get all image files in the directory
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(tuple(image_extensions))]

    if not image_files:
        print(f"No valid image files found in {directory}")
        return

    # Find existing card_N.jpg files and extract numbers
    existing_numbers = []
    for file in image_files:
        match = re.match(r'card_(\d+)\.jpg$', file.lower())
        if match:
            existing_numbers.append(int(match.group(1)))

    # Determine the highest number for renaming
    if existing_numbers:
        highest_num = max(existing_numbers)
    else:
        highest_num = 0

    # Find isolated numbers (before any gap)
    existing_numbers.sort()
    isolated_numbers = []
    for i in range(len(existing_numbers) - 1):
        if existing_numbers[i + 1] - existing_numbers[i] > 1:
            isolated_numbers.extend(existing_numbers[:i + 1])
            break

    # Start numbering from the highest number + 1
    next_num = highest_num + 1 if existing_numbers else 1

    # Track all card numbers (existing and new) to find the lowest later
    all_card_numbers = [n for n in existing_numbers if n not in isolated_numbers]

    # Rename isolated numbers to the end
    for num in sorted(isolated_numbers):
        old_name = f'card_{num}.jpg'
        new_name = f'card_{next_num}.jpg'
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)

        # Ensure no overwrite
        while os.path.exists(new_path):
            next_num += 1
            new_name = f'card_{next_num}.jpg'
            new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed {old_name} to {new_name}")
        all_card_numbers.append(next_num)
        next_num += 1

    # Find unnumbered .jpg files
    non_card_jpgs = []
    for file in image_files:
        if file.lower().endswith('.jpg') and not re.match(r'card_(\d+)\.jpg$', file.lower()):
            non_card_jpgs.append(file)

    # Sort alphabetically for consistent ordering
    non_card_jpgs.sort()

    # Rename unnumbered .jpg files
    for file in non_card_jpgs:
        old_path = os.path.join(directory, file)
        new_name = f'card_{next_num}.jpg'
        new_path = os.path.join(directory, new_name)

        # Ensure no overwrite
        while os.path.exists(new_path):
            next_num += 1
            new_name = f'card_{next_num}.jpg'
            new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed {file} to {new_name}")
        all_card_numbers.append(next_num)
        next_num += 1

    # Convert and rename non-.jpg image files
    non_jpg_images = []
    for file in image_files:
        if file.lower().endswith(tuple(image_extensions - {'.jpg'})):
            non_jpg_images.append(file)

    # Sort alphabetically for consistent ordering
    non_jpg_images.sort()

    for file in non_jpg_images:
        old_path = os.path.join(directory, file)
        new_name = f'card_{next_num}.jpg'
        new_path = os.path.join(directory, new_name)

        # Ensure no overwrite
        while os.path.exists(new_path):
            next_num += 1
            new_name = f'card_{next_num}.jpg'
            new_path = os.path.join(directory, new_name)

        # Convert image to .jpg
        try:
            with Image.open(old_path) as img:
                # Convert to RGB if necessary (e.g., for PNG with transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                img.save(new_path, 'JPEG', quality=95)
            print(f"Converted and renamed {file} to {new_name}")
            # Remove original non-.jpg file
            os.remove(old_path)
            all_card_numbers.append(next_num)
            next_num += 1
        except Exception as e:
            print(f"Failed to convert {file}: {e}")

    # Find the lowest card number after all operations
    if all_card_numbers:
        lowest_num = min(all_card_numbers)
        lowest_card = f'card_{lowest_num}.jpg'
        lowest_card_path = os.path.join(directory, lowest_card)

        # Check if any card_N.jpg files exist in output_dir
        output_files = [f for f in os.listdir(output_dir) if re.match(r'card_(\d+)\.jpg$', f.lower())]
        json_path = os.path.join(output_dir, 'next_jpgcard.json')
        output_card_path = os.path.join(output_dir, 'card_x.jpg')

        # Write JSON and copy/rename only if card_x.jpg doesn't exist
        if not os.path.exists(output_card_path):
            # Copy the lowest card to output_dir
            try:
                temp_copy_path = os.path.join(output_dir, lowest_card)
                shutil.move(lowest_card_path, temp_copy_path)
                print(f"Copied {lowest_card} to {output_dir}")

                # Rename the copied file to card_x.jpg
                os.rename(temp_copy_path, output_card_path)
                print(f"Renamed {lowest_card} to card_x.jpg in {output_dir}")

                # Write JSON only if no card_N.jpg files exist in output_dir
                if not output_files:
                    try:
                        timestamp = datetime.now(pytz.timezone('Africa/Lagos')).isoformat()
                        with open(json_path, 'w') as json_file:
                            json.dump({
                                'next_jpgcard': lowest_card,
                                'changed_to': 'card_x.jpg',
                                'timestamp': timestamp
                            }, json_file, indent=4)
                        print(f"Wrote {lowest_card} (changed to card_x.jpg) with timestamp {timestamp} to {json_path}")
                    except Exception as e:
                        print(f"Failed to write JSON file: {e}")
            except Exception as e:
                print(f"Failed to copy or rename {lowest_card}: {e}")
        else:
            print(f"Skipped copying and renaming {lowest_card} as card_x.jpg already exists in {output_dir}")
    else:
        print("No card_N.jpg files found after processing.")



def toggleaddphoto():
    """
    Uses OCR to locate and click the 'Add photo' or 'Add photo/video' button.
    Tracks whether the button has already been toggled via function attribute.
    """
    # ---- STATE TRACKER ----
    if hasattr(toggleaddphoto, 'is_toggled') and toggleaddphoto.is_toggled:
        print("'Add photo/video' button already toggled. Skipping.")
        return

    print("Searching for 'Add photo' or 'Add photo/video' text content")
    try:
        retry_count = 0
        max_retries = 3
        save_path = r"C:\xampp\htdocs\serenum\files\gui"

        while retry_count < max_retries:
            # Capture screenshot
            screenshot = ImageGrab.grab()
            screenshot_cv = cv2.cvtColor(np.array(screenshot, dtype=np.uint8), cv2.COLOR_RGB2BGR)

            # Save screenshot
            os.makedirs(save_path, exist_ok=True)
            screenshot_file = os.path.join(save_path, "windowstext.png")
            cv2.imwrite(screenshot_file, screenshot_cv)
            print(f"Screenshot captured and saved as '{screenshot_file}'")

            # Image processing
            gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            resized = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            thresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 2)

            # OCR
            data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT, config='--psm 3')
            print("OCR data keys:", data.keys())
            print("All detected text with positions:")
            for i, text in enumerate(data["text"]):
                if text.strip():
                    print(f"Index {i}: '{text}' (Confidence: {data['conf'][i]}, Left: {data['left'][i]}, Top: {data['top'][i]})")

            # Search for target phrases
            text_lower = [t.lower() for t in data["text"]]
            texts_index = None
            detected_phrase = None

            # Case 1: "Add" + "photo/video"
            for i, text in enumerate(text_lower):
                if text == "add":
                    if i + 1 < len(text_lower) and text_lower[i + 1] == "photo/video":
                        texts_index = i
                        detected_phrase = "add photo/video"
                        break
                    if i + 1 < len(text_lower) and text_lower[i + 1] == "photo":
                        texts_index = i
                        detected_phrase = "add photo"
                        if i + 2 < len(text_lower) and text_lower[i + 2] == "video":
                            detected_phrase = "add photo/video"
                        break

            # Case 2: "addphoto" as single token
            if texts_index is None:
                for i, text in enumerate(text_lower):
                    if text == "addphoto":
                        texts_index = i
                        detected_phrase = "addphoto"
                        break

            # Proceed if valid phrase found
            if texts_index is not None and text_lower[texts_index] != "addvideo":
                x = data["left"][texts_index] // 1.5
                y = data["top"][texts_index] // 1.5
                w = data["width"][texts_index] // 1.5
                h = data["height"][texts_index] // 1.5
                center_x = x + w // 2
                center_y = y + h // 2

                print(f"Detected: {detected_phrase}")
                print(f"Coordinates: left={x}, top={y}, width={w}, height={h}")
                print(f"Moving to: ({center_x}, {center_y})")

                pyautogui.moveTo(center_x, center_y)
                time.sleep(0.1)
                pyautogui.click()
                print("Clicked on 'Add photo' or 'Add photo/video'")

                # SET TRACKER: Mark as toggled
                toggleaddphoto.is_toggled = True

                time.sleep(3)
                selectmedia()
                return  # Success → exit

            else:
                retry_count += 1
                print(f"Retry {retry_count}/{max_retries}: No 'Add photo' or 'Add photo/video' found")
                if retry_count == max_retries:
                    loading_index = next((i for i, t in enumerate(text_lower) if "loading" in t), None)
                    if loading_index is not None:
                        print("Detected 'loading' text, retrying with new screenshot")
                        time.sleep(1)
                        continue
                    print("Max retries reached. Button not found.")
                    return
                time.sleep(1)

    except Exception as e:
        print(f"An error occurred in toggleaddphoto(): {e}")

def selectmedia():
    """Select media by COPYING the file path and PASTING it (faster & more reliable)."""
    # Initialize tracker if not already set
    if not hasattr(selectmedia, 'has_uploaded'):
        selectmedia.has_uploaded = False

    # Check if media has already been selected
    if selectmedia.has_uploaded:
        print("Media path already entered and submitted. Skipping operation.")
        return

    try:
        # Load configuration to get author and construct file path
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        file_path = f"C:\\xampp\\htdocs\\serenum\\files\\next jpg\\{author}\\card_x.jpg"

        # Ensure the file exists before attempting to input the path
        if not os.path.exists(file_path):
            print(f"❌ Media file does not exist: {file_path}")
            return

        print(f"📁 Preparing to COPY-PASTE: {file_path}")
        
        # **COPY PATH TO CLIPBOARD** (faster than typing)
        import pyperclip
        pyperclip.copy(file_path)
        print(f"✅ COPIED TO CLIPBOARD: {file_path}")
        
        # **PASTE PATH** (Ctrl+V)
        pyautogui.hotkey('ctrl', 'v')
        print("✅ PASTED PATH (Ctrl+V)")
        
        # **PRESS ENTER**
        pyautogui.press("enter")
        print("✅ PRESSED ENTER")

        # Update tracker to indicate media has been selected
        selectmedia.has_uploaded = True
        print("✅ Updated tracker: has_uploaded set to True")

        time.sleep(3)  # Pause to allow file dialog to process
        confirmselectedmedia()

    except Exception as e:
        print(f"❌ Failed to select media: {str(e)}")
        selectmedia.has_uploaded = True  # Mark as done even on error
        raise
def confirmselectedmedia():
    """
    Confirm media selection with progressive patience:
    Retry #1 → 2s, #2 → 3s, #3 → 4s, #5 → 10s
    Max 5 retries. Resets on success or full failure.
    """
    screen_width, screen_height = pyautogui.size()
    top = (0, 0, screen_width, screen_height)
    
    # Initialize retry tracker
    if not hasattr(confirmselectedmedia, 'retry_count'):
        confirmselectedmedia.retry_count = 0
    
    MAX_RETRIES = 5
    
    # === FAILURE: All retries used ===
    if confirmselectedmedia.retry_count >= MAX_RETRIES:
        print("BREAKDOWN REPORT: All 5 retries exhausted - MEDIA SELECTION FAILED")
        print(f"   Total retries attempted: {MAX_RETRIES}")
        print(f"   editmedia.png NOT FOUND after all attempts")
        print(f"   RECOMMENDED ACTION: Manual intervention required")
        
        # Reset for next post
        confirmselectedmedia.retry_count = 0
        if hasattr(selectmedia, 'has_uploaded'):
            selectmedia.has_uploaded = False
        return False
    
    # === INCREMENT & LOG RETRY ===
    confirmselectedmedia.retry_count += 1
    attempt = confirmselectedmedia.retry_count
    print(f"RETRY #{attempt}/{MAX_RETRIES} - Looking for editmedia.png...")

    # === PROGRESSIVE WAIT TIMES ===
    wait_times = {1: 2, 2: 3, 3: 4, 4: 6, 5: 10}
    wait_sec = wait_times.get(attempt, 4)

    # === SEARCH FOR editmedia.png ===
    try:
        editmedia = pyautogui.locateOnScreen(
            f'{GUI_PATH}\\cropandfilter.png',
            confidence=0.8,
            region=top,
            grayscale=True  # Faster + more robust
        )
        if editmedia:
            x, y = pyautogui.center(editmedia)
            print(f"MEDIA CONFIRMED SELECTED on retry #{attempt}")
            print(f"   Clicked at ({x}, {y})")
            
            # Reset on SUCCESS
            confirmselectedmedia.retry_count = 0
            return True
    except Exception as e:
        print(f"   Search error on retry #{attempt}: {e}")

    # === NOT FOUND → WAIT & RETRY ===
    print(f"   editmedia.png NOT FOUND → waiting {wait_sec} sec before retry...")
    time.sleep(wait_sec)
    
    # Recursive call (safe: max depth 5)
    return confirmselectedmedia() 

    
    # SINGLE confirm_fileisready call
def confirm_fileisready():
    file_name = pyautogui.locateOnScreen(f'{GUI_PATH}\\file_name.png', confidence=0.8)
    pc = pyautogui.locateOnScreen(f'{GUI_PATH}\\pc.png', confidence=0.8)
    new_folder = pyautogui.locateOnScreen(f'{GUI_PATH}\\new_folder.png', confidence=0.8)
    customised_files = pyautogui.locateOnScreen(f'{GUI_PATH}\\customised_files.png', confidence=0.8)
    
    if file_name or pc or new_folder or customised_files:
        print("✅ File dialog confirmed - selecting media")
        selectmedia()
        print("✅ File selected")
        return True
    else:
        print("❌ File dialog not confirmed - closing")
        pyautogui.hotkey('alt', 'f4')
        return False



def writecaption_ocr():
    """Enter a random caption using GUI automation with OCR text detection, 
    constructing the JSON path using author and group_types from pageandgroupauthors.json."""
    try:
        # Load configuration from JSON
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        group_types = config.get('group_types', 'others').lower()  # Default to 'others' if not found
        print(f"Read from {JSON_CONFIG_PATH}: author='{author}', group_types='{group_types}'")
        
        # Validate group_types
        if group_types not in ['uk', 'others']:
            print(f"Invalid group_types value: '{group_types}'. Defaulting to 'others'.")
            group_types = 'others'
        
        # Construct the path to the author's captions JSON file using author and group_types
        json_path = f"C:\\xampp\\htdocs\\serenum\\files\\captions\\{author}({group_types}).json"
        print(f"Constructed JSON path: {json_path}")
        
        # Check if the JSON file exists
        if not os.path.exists(json_path):
            raise Exception(f"JSON file not found at {json_path}")
        
        # Load captions from the author's JSON file
        with open(json_path, 'r') as file:
            captions = json.load(file)
        
        # Select a random caption
        selected_caption = random.choice(captions)['description']
        print(f"Selected random caption for author '{author}' (group_types '{group_types}', GUI): '{selected_caption}'")
        
        # Static variable to store the last written caption
        if not hasattr(writecaption_ocr, 'last_written_caption'):
            writecaption_ocr.last_written_caption = None
        
        # OCR-based text detection
        print("Searching for 'text' to locate input field")
        retry_count = 0
        max_retries = 3
        save_path = r"C:\xampp\htdocs\serenum\files\gui"
        
        while retry_count < max_retries:
            # Capture screenshot
            screenshot = ImageGrab.grab()
            screenshot_cv = cv2.cvtColor(np.array(screenshot, dtype=np.uint8), cv2.COLOR_RGB2BGR)
            
            # Save screenshot
            os.makedirs(save_path, exist_ok=True)
            screenshot_file = os.path.join(save_path, "caption_text_area.png")
            cv2.imwrite(screenshot_file, screenshot_cv)
            print(f"Screenshot captured and saved as '{screenshot_file}'")
            
            # Image processing
            gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            resized = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            thresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # OCR with improved configuration
            data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT, config='--psm 3')
            print("OCR data keys:", data.keys())
            print("All detected text with positions:")
            for i, text in enumerate(data["text"]):
                if text.strip():
                    print(f"Index {i}: '{text}' (Confidence: {data['conf'][i]}, Left: {data['left'][i]}, Top: {data['top'][i]})")
            
            # Search for "text"
            text_lower = [t.lower() for t in data["text"]]
            text_index = None
            for i, text in enumerate(text_lower):
                if text == "text":
                    text_index = i
                    break
            
            if text_index is not None:
                # Get coordinates (adjust for resizing)
                x = data["left"][text_index] // 1.5
                y = data["top"][text_index] // 1.5
                w = data["width"][text_index] // 1.5
                h = data["height"][text_index] // 1.5
                center_x = x + w // 2
                center_y = y + h // 2
                print(f"Detected: 'text'")
                print(f"Coordinates: left={x}, top={y}, width={w}, height={h}")
                print(f"Moving to: ({center_x}, {center_y})")
                
                # Click the detected text location (slightly offset to target input field)
                pyautogui.moveTo(center_x, center_y + 50)  # Offset to click inside the input field
                time.sleep(0.1)
                pyautogui.click()
                print("✅ Clicked on 'text' input field")
                time.sleep(1)
                
                # Proceed with caption input logic
                # Get current text in text field using GUI
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.5)
                current_text = pyperclip.paste().strip()
                print(f"Current text in field (GUI): '{current_text}'")
                
                # EXACT SAME LOGIC FOR TEXT VALIDATION & WRITING
                if not current_text or (current_text != selected_caption and current_text != writecaption_ocr.last_written_caption):
                    # Clear the text field (Ctrl+A, Delete)
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('delete')
                    time.sleep(0.5)
                    
                    # Enter the selected caption
                    pyautogui.write(selected_caption)
                    print(f"Entered text into post field (GUI): '{selected_caption}'")
                    
                    # Save the written caption to the static variable
                    writecaption_ocr.last_written_caption = selected_caption
                    print(f"Saved caption to last_written_caption (GUI): '{selected_caption}'")
                    time.sleep(1)
                
                elif current_text == selected_caption or current_text == writecaption_ocr.last_written_caption:
                    print(f"Text '{current_text}' is already correct in the text field (GUI). Skipping write operation.")
                    if current_text == selected_caption:
                        writecaption_ocr.last_written_caption = selected_caption
                        print(f"Updated last_written_caption to match current text (GUI): '{selected_caption}'")
                    return True
                
                else:
                    print(f"Text field contains different text (GUI): '{current_text}'. Replacing with saved caption.")
                    if writecaption_ocr.last_written_caption:
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.hotkey('delete')
                        time.sleep(0.5)
                        pyautogui.write(writecaption_ocr.last_written_caption)
                        print(f"Replaced text with last written caption (GUI): '{writecaption_ocr.last_written_caption}'")
                        time.sleep(1)
                    else:
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.hotkey('delete')
                        time.sleep(0.5)
                        pyautogui.write(selected_caption)
                        writecaption_ocr.last_written_caption = selected_caption
                        print(f"No previous caption saved. Entered new caption (GUI): '{selected_caption}'")
                        time.sleep(1)
                
                return True
            
            else:
                retry_count += 1
                print(f"Retry {retry_count}/{max_retries}: No 'text' found")
                if retry_count == max_retries:
                    print("Max retries reached. No 'text' input field found.")
                    return False
                time.sleep(1)  # Wait before retrying
        
        return False
    
    except Exception as e:
        print(f"Failed to enter text (GUI): {str(e)}")
        return False

def writecaption_element():
    """
    Finds the Facebook post composer by writing a *real* random caption
    from the same JSON file that writecaption_ocr() uses.
    Returns the working WebElement or None.

    NEW: 
      - Uses `writecaption_element.has_written` (like toggleaddphoto.is_toggled)
      - Skips entire process if caption already written this session
      - Reset via reset_trackers()
    """
    # ---- EARLY EXIT: Already written this session ----
    if getattr(writecaption_element, 'has_written', False):
        print("\n=== CAPTION ALREADY WRITTEN THIS SESSION. SKIPPING. ===")
        return None

    print("\n=== LOCATING POST COMPOSER (via real caption test) ===")

    # --------------------------------------------------------------------- #
    # 0. Load caption (same as writecaption_ocr)
    # --------------------------------------------------------------------- #
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author       = config['author']
        group_types  = config.get('group_types', 'others').lower()
        if group_types not in ['uk', 'others']:
            group_types = 'others'
        json_path = f"C:\\xampp\\htdocs\\serenum\\files\\captions\\{author}({group_types}).json"

        if not os.path.exists(json_path):
            raise FileNotFoundError(json_path)

        with open(json_path, 'r') as f:
            captions = json.load(f)

        selected_caption = random.choice(captions)['description']
        print(f"Loaded caption for author '{author}' (group '{group_types}'): '{selected_caption}'")

    except Exception as e:
        print(f"Could not load caption JSON: {e}")
        return None

    # --------------------------------------------------------------------- #
    # 1. Get candidates
    # --------------------------------------------------------------------- #
    xpath = """
        //div[
            (@contenteditable='true' or @contenteditable='plaintext-only')
            and
            (
                contains(@class, 'notranslate') or
                contains(@class, 'textinput') or
                contains(@class, 'composer') or
                contains(@data-text, 'true') or
                contains(@aria-label, 'Text') or
                contains(@role, 'textbox')
            )
        ]
    """
    try:
        candidates = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        print(f"Found {len(candidates)} candidate(s).")
    except Exception:
        print("No candidates found.")
        return None

    # --------------------------------------------------------------------- #
    # 2. Test each candidate (with "already-written" check)
    # --------------------------------------------------------------------- #
    working_element = None
    for i, el in enumerate(candidates):
        try:
            if not el.is_displayed():
                print(f"  [{i}] Skipped – not visible")
                continue

            size = el.size
            w, h = size.get('width', 0), size.get('height', 0)
            print(f"  [{i}] Size: {w}x{h}")

            # ---- READ CURRENT CONTENT BEFORE TOUCHING ----
            current_text = driver.execute_script(
                "return arguments[0].textContent || arguments[0].innerText || '';", el
            ).strip()

            # Normalize for comparison
            norm_caption = selected_caption.strip().lower()
            norm_current = current_text.strip().lower()

            if norm_current == norm_caption:
                print(f"  [{i}] Caption already present – using this element.")
                working_element = el
                writecaption_element.last_written_caption = selected_caption
                writecaption_element.has_written = True  # MARK AS DONE
                break

            # ---- CLICK & WRITE (ONLY IF NOT ALREADY THERE) ----
            el.click()
            time.sleep(0.3)
            ActionChains(driver).send_keys(selected_caption).perform()
            time.sleep(1.0)

            # Read back what we just wrote
            current_text = driver.execute_script(
                "return arguments[0].textContent || arguments[0].innerText || '';", el
            ).strip()

            print(f"     Wrote caption  Got back: '{current_text}'")

            if selected_caption.lower() in current_text.lower():
                print(f"     SUCCESS! This is the real composer.")
                working_element = el
                writecaption_element.last_written_caption = selected_caption
                writecaption_element.has_written = True  # MARK AS DONE
                break
            else:
                print(f"     Failed – caption did not appear.")
                # Clear failed attempt
                driver.execute_script("arguments[0].textContent = '';", el)

        except Exception as e:
            print(f"  [{i}] Error: {e}")

    # --------------------------------------------------------------------- #
    # 3. Return result
    # --------------------------------------------------------------------- #
    if working_element:
        final_size = working_element.size
        print(f"\nCOMPOSER FOUND! Using candidate with size {final_size}")
        return working_element
    else:
        print("\nNo candidate accepted the caption. Composer not found.")
        writecaption_ocr()
        return None
    
         


def extract_texts(return_time_value=None, additional_texts=None):
    """Extract all visible text from the current webpage, construct a time value in the format 'Time: HH:MM',
    and check for additional specified text values.
    
    Args:
        return_time_value (callable, optional): A callback function to receive the time value.
        additional_texts (list, optional): A list of text values to check for in the extracted texts.
    Returns:
        tuple: A tuple containing:
            - extractedtexts (list): List of all extracted non-empty text from the webpage.
            - time_value (str or None): The constructed time value in 'Time: HH:MM' format, or None if not found.
            - found_texts (list): List of additional text values that were found in the extracted texts.
    """
    global driver
    try:
        # Get all elements that contain text
        elements = driver.find_elements(By.XPATH, "//*[text()]")
        extractedtexts = []
        time_components = []
        found_texts = []

        # Collect all non-empty text and time-related components
        for element in elements:
            text = element.text.strip()
            if text:  # Only add non-empty text
                extractedtexts.append(text)
                # Collect potential time-related components
                if text == 'Time input' or text == ':' or text.isdigit():
                    time_components.append(text)
                # Check for additional specified texts
                if additional_texts and text in additional_texts:
                    found_texts.append(text)
        
        # Look for the pattern 'Time input', hours, ':', minutes
        time_value = None
        for i in range(len(time_components) - 3):
            if (time_components[i] == 'Time input' and 
                time_components[i+1].isdigit() and 
                len(time_components[i+1]) <= 2 and  # Ensure hours is 1 or 2 digits
                time_components[i+2] == ':' and 
                time_components[i+3].isdigit() and 
                len(time_components[i+3]) <= 2):    # Ensure minutes is 1 or 2 digits
                hours = time_components[i+1].zfill(2)  # Pad with leading zero if needed
                minutes = time_components[i+3].zfill(2)  # Pad with leading zero if needed
                time_value = f"Time: {hours}:{minutes}"
                break
        
        if time_value:
            print("Time value:", time_value)
            # Pass the time value to the callback function if provided
            if callable(return_time_value):
                return_time_value(time_value)
        else:
            print("Time components not found or incomplete.")
        
        if additional_texts:
            print()
            #print(f"Additional texts checked: {additional_texts}")
            #print(f"Found texts: {found_texts}")
        else:
            print("No additional texts provided for checking.")

        return extractedtexts, time_value, found_texts
    except Exception as e:
        print(f"Error extracting texts: {str(e)}")
        return [], None, []
def toggleschedule():
    """Toggle the 'Set date and time' button or checkbox for scheduling a post, with tracker to avoid redundant clicks."""
    try:
        # Initialize tracker if not already set
        if not hasattr(toggleschedule, 'is_toggled'):
            toggleschedule.is_toggled = False

        # Check if the schedule was already toggled
        if toggleschedule.is_toggled:
            print("Schedule toggle already activated. Skipping click operation.")
            return

        # Wait for and locate the scheduling toggle
        scheduling_toggle = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'set date and time')]//input[@type='checkbox'] | "
                "//div[contains(@aria-label, 'Set date and time') or contains(text(), 'Set date and time')]//following-sibling::div[@role='switch'] | "
                "//span[contains(text(), 'Set date and time')]/following::input[1]"
            ))
        )
        
        # If it's a checkbox, check if it's already selected
        if scheduling_toggle.tag_name == 'input' and scheduling_toggle.get_attribute('type') == 'checkbox':
            if not scheduling_toggle.is_selected():
                scheduling_toggle.click()
                print("Toggled 'Set date and time' checkbox on.")
            else:
                print("'Set date and time' is already enabled.")
        else:
            # For switch-like elements, click the switch
            scheduling_toggle.click()
            print("Clicked 'Set date and time' toggle.")
        
        # Update tracker to indicate the schedule has been toggled
        toggleschedule.is_toggled = True
        print("Updated tracker: is_toggled set to True")
        
        time.sleep(2)  # Pause to allow any UI updates after toggling
        
    except Exception as e:
        print(f"Failed to toggle schedule button: {str(e)}")
        try:
            # Alternative locator for scheduling toggle
            scheduling_toggle = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "[aria-label*='Schedule'] input[type='checkbox'], [data-testid*='schedule-toggle']"
                ))
            )
            # Check if it's a checkbox and its state
            if scheduling_toggle.tag_name == 'input' and scheduling_toggle.get_attribute('type') == 'checkbox':
                if not scheduling_toggle.is_selected():
                    scheduling_toggle.click()
                    print("Toggled 'Set date and time' checkbox on using alternative locator.")
                else:
                    print("'Set date and time' is already enabled (alternative locator).")
            else:
                scheduling_toggle.click()
                print("Clicked 'Set date and time' toggle using alternative locator.")
            
            # Update tracker to indicate the section has been toggled
            toggleschedule.is_toggled = True
            print("Updated tracker: is_toggled set to True (alternative locator)")
            
            time.sleep(2)  # Pause to allow UI updates
            
        except Exception as e2:
            print(f"Alternative locator for schedule toggle failed: {str(e2)}")
            raise Exception("Could not locate or toggle schedule button")

def set_webschedule_v2():
    """
    Set schedule using {type}schedules.json.
    UI expects:
        • Date: mm/dd/yyyy  (e.g. 10/29/2025)
        • Time: 3 separate inputs → hours, minutes, meridiem (AM/PM)

    NEW:
      - `set_webschedule_v2.has_set` tracker prevents re-execution
      - Skips if already correct
      - Reset via reset_trackers()
    """
    # ---- EARLY EXIT: Already set this session ----
    if getattr(set_webschedule_v2, 'has_set', False):
        print("\n=== SCHEDULE ALREADY SET THIS SESSION. SKIPPING. ===")
        return

    print("\n=== SETTING WEB SCHEDULE ===")

    # ------------------------------------------------------------------ #
    # 1. Load config + target schedule
    # ------------------------------------------------------------------ #
    try:
        with open(JSON_CONFIG_PATH, 'r') as f:
            cfg = json.load(f)
        author     = cfg['author']
        type_value = cfg.get('type', '')
        sched_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}schedules.json"
    except Exception as e:
        print(f"Failed to load {JSON_CONFIG_PATH}: {e}")
        return

    try:
        with open(sched_path, 'r') as f:
            data = json.load(f)['next_schedule']
        target_date      = data['date']          # "29/10/2025" → we convert
        target_time_12h  = data['time_12hour']    # "07:00 AM"
        target_time_24h  = data['time_24hour']    # "07:00"
        if not all([target_date, target_time_12h, target_time_24h]):
            raise ValueError("Missing fields in schedules.json")
    except Exception as e:
        print(f"Failed to read {sched_path}: {e}")
        return

    # ------------------------------------------------------------------ #
    # 2. Parse JSON times
    # ------------------------------------------------------------------ #
    m12 = re.match(r"(\d{1,2}):(\d{2})\s*(AM|PM)", target_time_12h, re.I)
    m24 = re.match(r"(\d{1,2}):(\d{2})", target_time_24h)
    if not m12 or not m24:
        print("Invalid time format in JSON")
        return
    hour_12, minute_12, period = m12.groups()
    hour_24, minute_24         = m24.groups()
    print(f"Target → {target_date}  {target_time_12h} / {target_time_24h}")

    # ------------------------------------------------------------------ #
    # 3. Convert dd/mm/yyyy → mm/dd/yyyy (UI format)
    # ------------------------------------------------------------------ #
    def ui_date_mmddyyyy(ddmmyyyy: str) -> str:
        d, m, y = ddmmyyyy.split('/')
        return f"{m.zfill(2)}/{d.zfill(2)}/{y}"  # e.g. 10/29/2025
    ui_target_date = ui_date_mmddyyyy(target_date)
    print(f"UI date string → '{ui_target_date}'")

    # ------------------------------------------------------------------ #
    # 4. Wait for panel
    # ------------------------------------------------------------------ #
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'schedule')]")
            )
        )
        print("Schedule panel loaded.")
        time.sleep(2)
    except Exception as e:
        print(f"Panel not found: {e}")
        return

    # ------------------------------------------------------------------ #
    # 5. Locate ONLY the 4 inputs we need
    # ------------------------------------------------------------------ #
    date_input = hour_input = minute_input = meridiem_input = None
    inputs = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
    )
    print(f"Found {len(inputs)} <input> elements.")
    for idx, el in enumerate(inputs):
        ph = (el.get_attribute("placeholder") or "").lower()
        al = (el.get_attribute("aria-label") or "").lower()
        if "mm/dd/yyyy" in ph:
            date_input = el
            print(f"Date input [{idx}]: placeholder='{ph}' value='{el.get_attribute('value')}'")
        elif al == "hours":
            hour_input = el
            print(f"Hour input [{idx}]: aria-label='hours'")
        elif al == "minutes":
            minute_input = el
            print(f"Minute input [{idx}]: aria-label='minutes'")
        elif al == "meridiem":
            meridiem_input = el
            print(f"Meridiem input [{idx}]: aria-label='meridiem'")

    if not (date_input and hour_input and minute_input and meridiem_input):
        missing = [n for n, v in [("date", date_input), ("hour", hour_input),
                                  ("minute", minute_input), ("meridiem", meridiem_input)] if not v]
        print(f"Missing inputs: {', '.join(missing)}")
        return

    # ------------------------------------------------------------------ #
    # 6. Read current UI values
    # ------------------------------------------------------------------ #
    current_date = (date_input.get_attribute("value") or "").strip()
    print(f"Current UI date → '{current_date}'")
    _, extracted_time, _ = extract_texts()
    print(f"Current OCR time → '{extracted_time}'")

    # ------------------------------------------------------------------ #
    # 7. Skip if already correct
    # ------------------------------------------------------------------ #
    date_matches = (current_date == ui_target_date)
    expected_ocr = f"Time: {int(hour_12):d}:{minute_12}"
    time_matches = (extracted_time == expected_ocr or
                    extracted_time == f"Time: {hour_12}:{minute_12}")

    if date_matches and time_matches:
        print("Schedule already correct – marking as set.")
        set_webschedule_v2.has_set = True  # MARK AS DONE
        return

    # ------------------------------------------------------------------ #
    # 8. SET DATE (if needed)
    # ------------------------------------------------------------------ #
    if not date_matches:
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", date_input)
            date_input.click()
            time.sleep(0.3)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(0.2)
            ActionChains(driver).send_keys(ui_target_date).perform()
            date_input.send_keys(Keys.TAB)
            print(f"Date set → '{ui_target_date}'")
            time.sleep(1)
        except Exception as e:
            if "intercepted" in str(e).lower():
                print("Date click intercepted → reload")
                reset_trackers()
                driver.refresh()
                return
            print(f"Error setting date: {e}")
            return

    # ------------------------------------------------------------------ #
    # 9. SET TIME (if needed)
    # ------------------------------------------------------------------ #
    if not time_matches:
        # Hour
        try:
            hour_input.click()
            time.sleep(0.2)
            hour_input.clear()
            hour_input.send_keys(str(int(hour_12)))  # no leading zero
            print(f"Hour set → {int(hour_12)}")
            hour_input.send_keys(Keys.TAB)
            time.sleep(0.5)
        except Exception as e:
            if "intercepted" in str(e).lower():
                print("Hour click intercepted → reload")
                reset_trackers()
                driver.refresh()
                return
            print(f"Error setting hour: {e}")
            return

        # Minute
        try:
            minute_input.click()
            time.sleep(0.2)
            minute_input.clear()
            minute_input.send_keys(minute_12)
            print(f"Minute set → {minute_12}")
            minute_input.send_keys(Keys.TAB)
            time.sleep(0.5)
        except Exception as e:
            if "intercepted" in str(e).lower():
                print("Minute click intercepted → reload")
                reset_trackers()
                driver.refresh()
                return
            print(f"Error setting minute: {e}")
            return

        # Meridiem
        try:
            meridiem_input.click()
            time.sleep(0.2)
            ActionChains(driver).send_keys(period.upper()).send_keys(Keys.ENTER).perform()
            print(f"Meridiem set → {period.upper()}")
            time.sleep(0.5)
        except Exception as e:
            if "intercepted" in str(e).lower():
                print("Meridiem click intercepted → reload")
                reset_trackers()
                driver.refresh()
                return
            print(f"Error setting meridiem: {e}")
            return

    # ------------------------------------------------------------------ #
    # 10. FINAL VERIFICATION
    # ------------------------------------------------------------------ #
    final_date = (date_input.get_attribute("value") or "").strip()
    _, final_time_ocr, _ = extract_texts()

    # Verify date
    if final_date != ui_target_date:
        print(f"Date verification failed: UI='{final_date}' ≠ expected='{ui_target_date}'")
        return

    # Verify time
    expected_ocr = f"Time: {int(hour_12):d}:{minute_12}"
    if final_time_ocr not in (expected_ocr, f"Time: {hour_12}:{minute_12}"):
        print(f"Time verification failed: OCR='{final_time_ocr}' ≠ expected='{expected_ocr}'")
        return

    print("Schedule set & verified successfully!")
    set_webschedule_v2.has_set = True  # MARK AS DONE    







def click_schedule_button():
    try:
        # Wait for button to be enabled
        btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, 
                 "//button[contains(translate(., 'SCHEDULE', 'schedule'), 'schedule') and not(@disabled)] | "
                 "//div[@role='button' and contains(translate(., 'SCHEDULE', 'schedule'), 'schedule')]"
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", btn)
        print("SCHEDULED SUCCESSFULLY!")
        
        

        # Confirm
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(), 'scheduled')]")
            )
        )
        print("Success message confirmed.")
        
        

        # Write to driverprogress.json
        driver_progress_path = r"C:\xampp\htdocs\serenum\driverprogress.json"
        progress_data = {
            "driver": "started",
            "scheduled": "successfully"
        }
        try:
            with open(driver_progress_path, 'w') as f:
                json.dump(progress_data, f, indent=4)
            print(f"Updated {driver_progress_path} with driver: started, scheduled: successfully")
            uploadedjpgs()
            update_calendar()
        except Exception as e:
            print(f"Failed to write to {driver_progress_path}: {str(e)}")

        
        # Reload page to start a new process
        print("Reloading page to start a new scheduling process...")
        reset_trackers()
        driver.refresh()
        time.sleep(2)

    except Exception as e:
        if "element click intercepted" in str(e).lower():
            print("Element click intercepted in schedule button. Reloading page and resetting trackers...")
            reset_trackers()
            driver.refresh()
            raise Exception("Page reloaded due to click interception")
        # Check for overlay
        overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
        if overlay:
            print("Detected overlay blocking interaction. Reloading page and resetting trackers...")
            reset_trackers()
            driver.refresh()
            raise Exception("Page reloaded due to overlay")
        print(f"Failed to schedule: {str(e)}")
        raise
def uploadedjpgs():
    """Upload JPGs, organizing by date in subfolders."""
    # Load configuration from JSON
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        # Use outputpath from JSON as source_dir, replacing authorvalue
        source_dir = config['outputpath'].replace('authorvalue', author)
    except Exception as e:
        print(f"Failed to load or parse {JSON_CONFIG_PATH}: {e}")
        return

    # Get current date (without time) in DD-Month-YYYY format for folder naming
    current_date = datetime.now().strftime("%d-%B-%Y")

    # Construct destination directory with author and date
    dest_dir = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\{current_date}"
    source_file = 'card_x.jpg'

    # Create source directory if it doesn't exist
    if not os.path.exists(source_dir):
        try:
            os.makedirs(source_dir)
            print(f"Created source directory: {source_dir}")
        except Exception as e:
            print(f"Failed to create source directory {source_dir}: {e}")
            return

    # Create destination directory (with date) if it doesn't exist
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            print(f"Created destination directory: {dest_dir}")
        except Exception as e:
            print(f"Failed to create destination directory {dest_dir}: {e}")
            return

    # Check if source file exists
    source_path = os.path.join(source_dir, source_file)
    if not os.path.exists(source_path):
        print(f"Source file does not exist: {source_path}")
        return

    # Get all card_N.jpg files in the date-specific destination directory
    try:
        dest_files = [f for f in os.listdir(dest_dir) if re.match(r'card_(\d+)\.jpg$', f.lower())]
    except Exception as e:
        print(f"Failed to list files in destination directory {dest_dir}: {e}")
        return

    # Extract numbers from existing card_N.jpg files in the current date folder
    existing_numbers = []
    for file in dest_files:
        match = re.match(r'card_(\d+)\.jpg$', file.lower())
        if match:
            existing_numbers.append(int(match.group(1)))

    # Determine the next number for the current date folder
    next_num = max(existing_numbers) + 1 if existing_numbers else 1

    # Define destination file path with date folder
    dest_file = f'card_{next_num}.jpg'
    dest_path = os.path.join(dest_dir, dest_file)

    # Ensure no overwrite
    while os.path.exists(dest_path):
        next_num += 1
        dest_file = f'card_{next_num}.jpg'
        dest_path = os.path.join(dest_dir, dest_file)

    # Copy and rename the file
    try:
        shutil.move(source_path, dest_path)
        print(f"Copied and renamed {source_file} to {dest_file} in {dest_dir}")
    except Exception as e:
        print(f"Failed to copy or rename {source_file} to {dest_file}: {e}")
        

def main():
    try:
        # Initialize WebDriver
        driver, wait = initialize_driver(mode="headed")
        
        # Call update_calendar before launch_profile
        print("Calling update_calendar before launch_profile...")
        
        # Execute launch_profile (includes JSON rewrite and continuous URL checking)
        launch_profile()
        
    except KeyboardInterrupt:
        print("Main script interrupted by user. Closing browser...")
        if driver:
            try:
                driver.quit()
            except:
                pass
    except Exception as e:
        print(f"An error occurred in main: {str(e)}")
        print("Browser will remain open for inspection.")
        # Keep browser open, no automatic quit


if __name__ == "__main__":
   main()
   

