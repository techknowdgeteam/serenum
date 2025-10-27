import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # ← ADD THIS LINEimport json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
from pytesseract import Output
import pytesseract
import pyperclip


# Global driver and wait objects
driver = None
wait = None

# Global JSON configuration path
JSON_CONFIG_PATH = r'C:\xampp\htdocs\serenum\files\pageauthors.json'
PYTESSERACT_PATH = r'C:\xampp\htdocs\serenum\pytesseract\tessdata'
GUI_PATH = r'C:\xampp\htdocs\serenum\files\gui'

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
    """Load URLs from the JSON file based on the author from pageauthors.json."""
    json_path = r"C:\xampp\htdocs\serenum\pageaccounts.json"
    pageauthors_path = r"C:\xampp\htdocs\serenum\files\pageauthors.json"
    
    try:
        # Load author from pageauthors.json
        with open(pageauthors_path, 'r') as author_file:
            author_data = json.load(author_file)
            author = author_data.get('author')
            if not author:
                raise Exception("No 'author' key found in pageauthors.json")
        
        # Load URLs from pageaccounts.json
        with open(json_path, 'r') as file:
            data = json.load(file)
            if author not in data:
                raise Exception(f"Author '{author}' not found in pageaccounts.json")
            return data[author]["schedule"][0]
    except Exception as e:
        print(f"Failed to load URLs from JSON: {str(e)}")
        raise



def reset_trackers():
    """Reset ALL function trackers to their initial state."""
    # Existing trackers
    writecaption.last_written_caption = None
    togglesharephotosandvideos.is_toggled = False
    selectmedia.has_uploaded = False
    update_calendar.has_run = False
    
    # NEW TRACKERS
    markjpgs.has_processed = False
    activatescroll.has_scrolled = False
    toggleschedule.has_toggled = False
    scheduledate.has_set_date = False
    scheduletime.has_set_time = False
    click_schedule_button.has_scheduled = False
    uploadedjpgs.has_uploaded = False
    
    print("🔄 RESET ALL FUNCTION TRACKERS:")
    print("  ✓ writecaption.last_written_caption = None")
    print("  ✓ togglesharephotosandvideos.is_toggled = False")
    print("  ✓ selectmedia.has_uploaded = False")
    print("  ✓ update_calendar.has_run = False")
    print("  ✓ markjpgs.has_processed = False")
    print("  ✓ activatescroll.has_scrolled = False")
    print("  ✓ toggleschedule.has_toggled = False")
    print("  ✓ scheduledate.has_set_date = False")
    print("  ✓ scheduletime.has_set_time = False")
    print("  ✓ click_schedule_button.has_scheduled = False")
    print("  ✓ uploadedjpgs.has_uploaded = False")

def update_calendar():
    """Update the calendar and write to JSON, with tracking to prevent running twice unless reset."""
    # Initialize tracker if not already set
    if not hasattr(update_calendar, 'has_run'):
        update_calendar.has_run = False

    # Check if update_calendar has already run
    if update_calendar.has_run:
        print("update_calendar already executed. Skipping operation.")
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
    
    # Read pageauthors.json
    pageauthors_path = r"C:\xampp\htdocs\serenum\files\pageauthors.json"
    print(f"Reading pageauthors.json from {pageauthors_path}")
    try:
        with open(pageauthors_path, 'r') as f:
            pageauthors = json.load(f)
    except FileNotFoundError:
        print(f"Error: pageauthors.json not found at {pageauthors_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: pageauthors.json contains invalid JSON")
        return
    
    author = pageauthors['author']
    type_value = pageauthors['type']
    print(f"Author: {author}, Type: {type_value}")
    
    # Read timeorders.json
    timeorders_path = r"C:\xampp\htdocs\serenum\files\timeorders.json"
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
    
    # Update tracker to indicate update_calendar has run
    update_calendar.has_run = True
    print("Updated tracker: update_calendar.has_run set to True")
    
    # Call schedule_time only if update_calendar was executed
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
    
    # Read pageauthors.json to get author and type
    pageauthors_path = r"C:\xampp\htdocs\serenum\files\pageauthors.json"
    print(f"Reading pageauthors.json from {pageauthors_path}")
    try:
        with open(pageauthors_path, 'r') as f:
            pageauthors = json.load(f)
    except FileNotFoundError:
        print(f"Error: pageauthors.json not found at {pageauthors_path}")
        return
    except json.decoder.JSONDecodeError:
        print(f"Error: pageauthors.json contains invalid JSON")
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
    timeorders_path = r"C:\xampp\htdocs\serenum\files\timeorders.json"
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
                    print(f"Recheck confirmed: URL is {uploadpost_url}. Proceeding to write caption, toggle schedule, interact with media, and select file.")
                    #update_calendar()
                    #markjpgs()
                    #togglesharephotosandvideos()
                    #writecaption()
                    toggleschedule()
                    scheduledate()
                    click_schedule_button()
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

def markjpgs():
    """Process and rename image files with tracker to prevent duplicate processing."""
    # Initialize tracker if not already set
    if not hasattr(markjpgs, 'has_processed'):
        markjpgs.has_processed = False

    # Check if markjpgs has already run
    if markjpgs.has_processed:
        print("markjpgs already executed. Skipping operation.")
        return

    # Load configuration from JSON
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        # Replace 'authorvalue' placeholder with the actual author value
        directory = config['inputpath'].replace('authorvalue', author)
        output_dir = config['outputpath'].replace('authorvalue', author)
    except Exception as e:
        print(f"Failed to load or parse {JSON_CONFIG_PATH}: {e}")
        markjpgs.has_processed = True  # Mark as done even on error
        return

    # Verify that paths end with the author folder
    if not directory.endswith(author) or not output_dir.endswith(author):
        print(f"Error: inputpath ({directory}) or outputpath ({output_dir}) does not end with author folder '{author}'")
        markjpgs.has_processed = True  # Mark as done even on error
        return
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except Exception as e:
            print(f"Failed to create output directory {output_dir}: {e}")
            markjpgs.has_processed = True  # Mark as done even on error
            return
    
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        markjpgs.has_processed = True  # Mark as done even on error
        return
    
    # Supported image extensions for conversion
    image_extensions = {'.png', '.jpeg', '.bmp', '.gif', '.tiff'}
    
    # Get all image files in the directory
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif', '.tiff'))]
    
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
            # Numbers before the gap are considered isolated
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
        if file.lower().endswith(tuple(image_extensions)):
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

    # UPDATE TRACKER - SUCCESS OR FAILURE
    markjpgs.has_processed = True
    print("✅ Updated tracker: markjpgs.has_processed = True")





def togglesharephotosandvideos():
    """Locates addmedia.png (primary) OR addmedia_icon.png (fallback), clicks once. FIXED: Single execution."""
    # Initialize tracker if not already set
    if not hasattr(togglesharephotosandvideos, 'is_toggled'):
        togglesharephotosandvideos.is_toggled = False

    # Check if already toggled
    if togglesharephotosandvideos.is_toggled:
        print("togglesharephotosandvideos already executed. Skipping operation.")
        return False

    # PRIMARY: Try addmedia.png first
    addmedia = pyautogui.locateOnScreen(f'{GUI_PATH}\\addmedia.png', confidence=0.8)
    if addmedia:
        print("✅ PRIMARY: addmedia.png found")
        center = pyautogui.center(addmedia)
        pyautogui.moveTo(center)
        time.sleep(0.1)
        pyautogui.click(center)
        print("✅ Toggled share media (PRIMARY)")
        
    # FALLBACK: If primary fails, try addmedia_icon.png
    else:
        print("⚠️ PRIMARY addmedia.png NOT found, trying FALLBACK...")
        addmedia_icon = pyautogui.locateOnScreen(f'{GUI_PATH}\\addmedia_icon.png', confidence=0.8)
        if addmedia_icon:
            print("✅ FALLBACK: addmedia_icon.png found")
            center = pyautogui.center(addmedia_icon)
            pyautogui.moveTo(center)
            time.sleep(0.1)
            pyautogui.click(center)
            print("✅ Toggled share media (FALLBACK)")
        else:
            print("❌ BOTH addmedia.png AND addmedia_icon.png NOT found")
            togglesharephotosandvideos.is_toggled = True
            return False

    # UPDATE TRACKER - CRITICAL (AFTER SUCCESSFUL CLICK)
    togglesharephotosandvideos.is_toggled = True
    print("✅ Updated tracker: togglesharephotosandvideos.is_toggled = True")
    
    time.sleep(2)
    
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
    
    confirm_fileisready()
    return True
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
            f'{GUI_PATH}\\editmedia.png',
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



def writecaption():
    """Enter a random caption using GUI automation with same variable tracking as writecaption()"""
    try:
        # Load configuration from JSON (SAME AS writecaption)
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        
        # Construct the path to the author's captions JSON file (SAME AS writecaption)
        json_path = f"C:\\xampp\\htdocs\\serenum\\files\\captions\\{author}.json"
        
        # Check if the JSON file exists (SAME AS writecaption)
        if not os.path.exists(json_path):
            raise Exception(f"JSON file not found at {json_path}")
        
        # Load captions from the author's JSON file (SAME AS writecaption)
        with open(json_path, 'r') as file:
            captions = json.load(file)
        
        # Select a random caption (SAME AS writecaption)
        selected_caption = random.choice(captions)['description']
        print(f"Selected random caption for author '{author}' (GUI): '{selected_caption}'")
        
        # Static variable to store the last written caption (SAME AS writecaption)
        if not hasattr(writecaption, 'last_written_caption'):
            writecaption.last_written_caption = None
        
        # GUI screen regions
        screen_width, screen_height = pyautogui.size()
        top = (0, 0, screen_width, screen_height)
        bottom = (0, screen_height // 2, screen_width, screen_height // 2)
        
        # Locate text area using GUI (MODIFIED TO USE SAME LOGIC)
        text = pyautogui.locateOnScreen(f'{GUI_PATH}\\text.png', confidence=0.8, region=top)
        
        if not text:
            print("Text area image not found")
            return False
        
        x, y = pyautogui.center(text)
        pyautogui.click(x, y + 50)
        print("Found text area, clicked text area")
        time.sleep(2)
        
        # Get current text in text field using GUI (FIXED: REMOVED USELESS pyautogui.position())
        # Select all text (Ctrl+A)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        
        # Copy selected text to clipboard
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        
        # Get current text from clipboard
        current_text = pyperclip.paste().strip()
        print(f"Current text in field (GUI): '{current_text}'")
        
        # EXACT SAME LOGIC AS writecaption FOR TEXT VALIDATION & WRITING
        if not current_text or (current_text != selected_caption and current_text != writecaption.last_written_caption):
            # Clear the text field (Ctrl+A, Delete)
            pyautogui.hotkey('ctrl', 'a')
            
            # Enter the selected caption
            pyautogui.write(selected_caption)
            print(f"Entered text into post field (GUI): '{selected_caption}'")
            
            # Save the written caption to the static variable
            writecaption.last_written_caption = selected_caption
            print(f"Saved caption to last_written_caption (GUI): '{selected_caption}'")
            time.sleep(1)
        
        elif current_text == selected_caption or current_text == writecaption.last_written_caption:
            print(f"Text '{current_text}' is already correct in the text field (GUI). Skipping write operation.")
            # Ensure the last written caption is saved if it matches
            if current_text == selected_caption:
                writecaption.last_written_caption = selected_caption
                print(f"Updated last_written_caption to match current text (GUI): '{selected_caption}'")
            return True
        
        else:
            print(f"Text field contains different text (GUI): '{current_text}'. Replacing with saved caption.")
            # Clear and replace with last written caption if available
            if writecaption.last_written_caption:
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.write(writecaption.last_written_caption)
                print(f"Replaced text with last written caption (GUI): '{writecaption.last_written_caption}'")
                time.sleep(1)
            else:
                # If no last written caption, use the selected caption
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.write(selected_caption)
                writecaption.last_written_caption = selected_caption
                print(f"No previous caption saved. Entered new caption (GUI): '{selected_caption}'")
                time.sleep(1)
        
        return True  # ← FIXED: Always returns True on success
        
    except Exception as e:
        print(f"Failed to enter text (GUI): {str(e)}")
        return False


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

def activatescroll():
    if not hasattr(activatescroll, 'has_scrolled'):
        activatescroll.has_scrolled = False

    if activatescroll.has_scrolled:
        print("activatescroll already done. Skip.")
        return True

    # **FIND & CLICK BUTTON**
    postdetails = pyautogui.locateOnScreen(f'{GUI_PATH}\\postdetails.png', confidence=0.8)
    
    if postdetails:
        x, y = pyautogui.center(postdetails)
        pyautogui.click(x, y)  # Your offset
        pyautogui.press('down', presses=7)
        return True
    else:
        print("Scroll didn't execute")
        return True  # ← Always True
    

def toggleschedule():
    time.sleep(1)
    activatescroll()
    time.sleep(1)
    """Finds toggleschedule.png → clicks → tracker."""
    if not hasattr(toggleschedule, 'has_toggled'):
        toggleschedule.has_toggled = False

    if toggleschedule.has_toggled:
        print("toggleschedule already done. Skip.")
        return True  # ← Changed to True

    print("🔍 Finding schedule button...")
    
    # **FIND & CLICK BUTTON**
    toggleschedule_img = pyautogui.locateOnScreen(f'{GUI_PATH}\\toggleschedule.png', confidence=0.8)
    
    if toggleschedule_img:
        x, y = pyautogui.center(toggleschedule_img)
        pyautogui.click(x + 80, y)  # Your offset
        time.sleep(2)
        toggleschedule.has_toggled = True
        print("✅ Schedule toggled")
        return True
    else:
        toggleschedule.has_toggled = True
        print("⚠️ Button not found but marked done")
        return True  # ← Always True
def unfocuscalendar():

    screen_width, screen_height = pyautogui.size()
    top = (0, 0, screen_width, screen_height)
    bottom = (0, screen_height // 2, screen_width, screen_height // 2)
    
    calendar = pyautogui.locateOnScreen(f'{GUI_PATH}\\calendar.png', confidence=0.8, region=top)
    
    if calendar:
        x, y = pyautogui.center(calendar)
        pyautogui.click(x, y)
        time.sleep(2)
        
        print("✅ un-focused calendar")
        return True
    else:
        print("⚠️ activatescroll failed but marked as done")
        return False
def scheduledate():
    """Locate and set date with tracker and verification loop - DETAILED VERIFICATION LOGS."""
    # Initialize tracker if not already set
    if not hasattr(scheduledate, 'has_set_date'):
        scheduledate.has_set_date = False

    if scheduledate.has_set_date:
        print("scheduledate already executed. Skipping operation.")
        return False

    print("SCANNING date.png FORMAT TEMPLATE...")
    
    # **LOAD GLOBAL JSON CONFIGURATION**
    JSON_CONFIG_PATH = r'C:\xampp\htdocs\serenum\files\pageauthors.json'
    
    try:
        with open(JSON_CONFIG_PATH, 'r') as f:
            config_data = json.load(f)
        author_value = config_data['author']
        type_value = config_data['type']
        print(f"CONFIG LOADED: author='{author_value}', type='{type_value}'")
    except Exception as e:
        print(f"ERROR LOADING CONFIG: {e}")
        scheduledate.has_set_date = True
        return False
    
    # **LOAD SCHEDULE JSON**
    schedule_json_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author_value}\\jsons\\{type_value}schedules.json"
    
    print(f"LOADING SCHEDULE: '{schedule_json_path}'")
    
    try:
        with open(schedule_json_path, 'r') as f:
            schedule_data = json.load(f)
        next_schedule = schedule_data['next_schedule']
        target_date = next_schedule['date']  # e.g., "01/11/2025"
        print(f"**JSON TARGET DATE**: '{target_date}'")
    except Exception as e:
        print(f"ERROR LOADING SCHEDULE JSON: {e}")
        scheduledate.has_set_date = True
        return False

    # Parse target date
    day_padded = target_date.split('/')[0]  # "01"
    day = str(int(day_padded))              # "1"
    month_num = target_date.split('/')[1]   # "11"
    year = target_date.split('/')[2]        # "2025"
    year_short = year[-2:]                  # "25"

    # Month mappings
    month_names = {
        '01': ('January', 'Jan'), '02': ('February', 'Feb'), '03': ('March', 'Mar'),
        '04': ('April', 'Apr'), '05': ('May', 'May'), '06': ('June', 'Jun'),
        '07': ('July', 'Jul'), '08': ('August', 'Aug'), '09': ('September', 'Sep'),
        '10': ('October', 'Oct'), '11': ('November', 'Nov'), '12': ('December', 'Dec')
    }
    full_month, short_month = month_names[month_num]

    # **EXPANDED DATE FORMATS - INCLUDING SPACED & CONCATENATED (NO SPACE) VARIANTS**
    date_formats = {
        # Standard
        'dd/mm/yyyy': target_date,
        'd/mm/yyyy': f"{day}/{month_num}/{year}",
        'dd/mm/yy': f"{day_padded}/{month_num}/{year_short}",
        'd/mm/yy': f"{day}/{month_num}/{year_short}",
        'dd-mm-yyyy': target_date.replace('/', '-'),
        'd-mm-yyyy': f"{day}-{month_num}-{year}",
        'dd-mm-yy': f"{day_padded}-{month_num}-{year_short}",
        'd-mm-yy': f"{day}-{month_num}-{year_short}",

        # With space
        'dd month yyyy': f"{day_padded} {full_month} {year}",
        'd month yyyy': f"{day} {full_month} {year}",
        'dd mon yyyy': f"{day_padded} {short_month} {year}",
        'd mon yyyy': f"{day} {short_month} {year}",
        'month dd, yyyy': f"{full_month} {day_padded}, {year}",
        'month d, yyyy': f"{full_month} {day}, {year}",
        'mon dd yyyy': f"{short_month} {day_padded} {year}",
        'mon d yyyy': f"{short_month} {day} {year}",

        # **NO SPACE VARIANTS (critical for OCR glue)**
        'dmonthyyyy': f"{day}{full_month}{year}",
        'dmonyyyy': f"{day}{short_month}{year}",
        'ddmonthyyyy': f"{day_padded}{full_month}{year}",
        'ddmonyyyy': f"{day_padded}{short_month}{year}",
        'monthdyyyy': f"{full_month}{day}{year}",
        'monthddyyyy': f"{full_month}{day_padded}{year}",
        'mondyyyy': f"{short_month}{day}{year}",
        'monddyyyy': f"{short_month}{day_padded}{year}",

        # Comma variants without space
        'monthd,yyyy': f"{full_month}{day},{year}",
        'monthdd,yyyy': f"{full_month}{day_padded},{year}",
        'mond,yyyy': f"{short_month}{day},{year}",
        'mondd,yyyy': f"{short_month}{day_padded},{year}",
    }

    # **PRECOMPUTE NORMALIZED VERSIONS FOR FAST MATCHING**
    normalized_targets = []
    for fmt_name, fmt_value in date_formats.items():
        # Remove all non-alphanum, lowercase
        clean = re.sub(r'[^a-zA-Z0-9]', '', fmt_value).lower()
        normalized_targets.append(clean)
        # Also store original for logging
        date_formats[fmt_name] = {'original': fmt_value, 'norm': clean}

    # **VERIFICATION LOOP - MAX 5 ATTEMPTS**
    max_attempts = 5
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\n**DATE ATTEMPT {attempt}/{max_attempts}**")
        
        # **Load date.png template**
        date_img = Image.open(f"{GUI_PATH}\\date.png")
        print("date.png FORMAT loaded")
        
        # **SET TESSDATA_PREFIX**
        import os
        os.environ['TESSDATA_PREFIX'] = PYTESSERACT_PATH
        
        # **OCR template**
        ocr_text = pytesseract.image_to_string(date_img, config='--psm 7')
        print(f"**TEMPLATE PNG OCR**: '{ocr_text.strip()}'")
        
        clean_text = re.sub(r'[^a-zA-Z0-9\s/.-]', '', ocr_text.strip())
        
        template_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'\d{1,2}\s+[A-Z]{3,9}\s+\d{2,4}',
            r'[A-Z]{3,9}\s+\d{1,2},?\s+\d{2,4}',
        ]
        
        has_date_format = any(re.search(p, clean_text, re.IGNORECASE) for p in template_patterns)
        if not has_date_format:
            print("PNG has NO date format!")
            scheduledate.has_set_date = True
            return False
        print("PNG CONFIRMED AS DATE FORMAT TEMPLATE")
        
        # **SCAN SCREEN**
        print("SCANNING SCREEN FOR ANY DATE...")
        screen_width, screen_height = pyautogui.size()
        screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        screen_text = pytesseract.image_to_string(screenshot, config='--psm 6')
        
        screen_patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',
            r'(\d{1,2})\s+([A-Z]{3,9})\s+(\d{2,4})',
            r'([A-Z]{3,9})\s+(\d{1,2}),?\s+(\d{2,4})',
        ]
        
        date_found = False
        for pattern in screen_patterns:
            matches = re.finditer(pattern, screen_text, re.IGNORECASE)
            for match in matches:
                screen_date = match.group(0)
                print(f"**SCREEN DATE FOUND**: '{screen_date}'")
                
                # **METHOD 1: OCR POSITION**
                print("   → Trying OCR position...")
                data = pytesseract.image_to_data(screenshot, output_type=Output.DICT)
                found_position = False
                for i, text in enumerate(data['text']):
                    if screen_date.lower() in text.lower() and int(data['conf'][i]) > 60:
                        x = data['left'][i]
                        y = data['top'][i]
                        width = data['width'][i]
                        height = data['height'][i]
                        
                        print(f"   → **OCR POSITION**: ({x}, {y}) {width}x{height}")
                        
                        # Capture before
                        date_region = screenshot.crop((x, y, x + width, y + height))
                        date_region.save(f"{GUI_PATH}\\captured_date_before.png")
                        print(f"   → **BEFORE PNG SAVED**")
                        
                        # Click & write
                        click_x = x + width//2 + 80
                        click_y = y + height//2
                        pyautogui.click(click_x, click_y)
                        time.sleep(0.5)
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.write(target_date)
                        time.sleep(0.5)
                        
                        # Unfocus
                        print("   → **UNFOCUSING**")
                        unfocuscalendar()
                        time.sleep(1)
                        scheduletime()
                        
                        # Verify region
                        verify_x = max(0, int(x - 30))
                        verify_y = max(0, int(y - 30))
                        verify_width = int(width + 100)
                        verify_height = int(height + 60)
                        
                        verification_screenshot = pyautogui.screenshot(region=(verify_x, verify_y, verify_width, verify_height))
                        verification_screenshot.save(f"{GUI_PATH}\\date_written.png")
                        
                        written_ocr = pytesseract.image_to_string(verification_screenshot, config='--psm 7')
                        written_clean = re.sub(r'[^a-zA-Z0-9]', '', written_ocr.strip()).lower()
                        
                        print(f"\n**VERIFICATION RESULTS:**")
                        print(f"   **JSON RECORD**: '{target_date}'")
                        print(f"   **CAPTURED OCR (clean)**: '{written_clean}'")
                        
                        # **SMART MATCHING - NO SPACES, CASE-INSENSITIVE**
                        matched = False
                        best_format = None
                        for fmt_name, fmt_data in date_formats.items():
                            norm_fmt = fmt_data['norm']
                            if (written_clean == norm_fmt or 
                                norm_fmt in written_clean or 
                                re.search(r'\b' + re.escape(norm_fmt) + r'\b', written_clean)):
                                print(f"   MATCH: {fmt_name} → '{fmt_data['original']}'")
                                matched = True
                                best_format = fmt_name
                                break
                        
                        if matched:
                            print(f"\n**DATE VERIFICATION SUCCESS**: {best_format}")
                            scheduledate.has_set_date = True
                            return True
                        else:
                            print(f"\n**NO MATCH** - Trying template...")
                            found_position = True
                            date_found = True
                            break
                
                if found_position:
                    break
                
                # **METHOD 2: TEMPLATE MATCH**
                print("   → Using date.png template...")
                try:
                    located = pyautogui.locateOnScreen(f"{GUI_PATH}\\date.png", confidence=0.7)
                    if located:
                        screen_x, screen_y, found_width, found_height = located
                        print(f"   → **TEMPLATE FOUND**: ({screen_x}, {screen_y}) {found_width}x{found_height}")
                        
                        # Write
                        pyautogui.click(screen_x + 80, screen_y)
                        time.sleep(0.5)
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.write(target_date)
                        time.sleep(0.5)
                        unfocuscalendar()
                        
                        # Verify
                        verify_x = max(0, int(screen_x - 30))
                        verify_y = max(0, int(screen_y - 30))
                        verify_width = int(found_width + 100)
                        verify_height = int(found_height + 60)
                        
                        verification_screenshot = pyautogui.screenshot(region=(verify_x, verify_y, verify_width, verify_height))
                        verification_screenshot.save(f"{GUI_PATH}\\date_written.png")
                        
                        written_ocr = pytesseract.image_to_string(verification_screenshot, config='--psm 7')
                        written_clean = re.sub(r'[^a-zA-Z0-9]', '', written_ocr.strip()).lower()
                        
                        print(f"\n**TEMPLATE VERIFICATION:**")
                        print(f"   **TARGET**: '{target_date}'")
                        print(f"   **OCR (clean)**: '{written_clean}'")
                        
                        matched = False
                        for fmt_name, fmt_data in date_formats.items():
                            norm_fmt = fmt_data['norm']
                            if (written_clean == norm_fmt or norm_fmt in written_clean):
                                print(f"   **TEMPLATE MATCH**: {fmt_name}")
                                matched = True
                                break
                        
                        if matched:
                            print("**DATE VERIFICATION SUCCESS VIA TEMPLATE!**")
                            scheduledate.has_set_date = True
                            return True
                        else:
                            print("**TEMPLATE VERIFICATION FAILED**")
                            date_found = True
                            break
                except Exception as e:
                    print(f"   → **TEMPLATE ERROR**: {e}")
                    continue
        
        if date_found:
            attempt += 1
            time.sleep(1.0)
            continue
        
        break
    
    scheduledate.has_set_date = True
    print(f"**DATE FAILED AFTER {max_attempts} ATTEMPTS**")
    return False 
def scheduletime():
    """Locate and set time with tracker - REGION LIMITED SEARCH with verification loop."""
    # Initialize tracker if not already set
    if not hasattr(scheduletime, 'has_set_time'):
        scheduletime.has_set_time = False

    if scheduletime.has_set_time:
        print("scheduletime already executed. Skipping operation.")
        return False

    print("🔍 SCANNING time.png FORMAT TEMPLATE...")
    
    # **LOAD GLOBAL JSON CONFIGURATION**
    JSON_CONFIG_PATH = r'C:\xampp\htdocs\serenum\files\pageauthors.json'
    
    try:
        with open(JSON_CONFIG_PATH, 'r') as f:
            config_data = json.load(f)
        author_value = config_data['author']
        type_value = config_data['type']
        print(f"📋 CONFIG LOADED: author='{author_value}', type='{type_value}'")
    except Exception as e:
        print(f"❌ ERROR LOADING CONFIG: {e}")
        scheduletime.has_set_time = True
        return False
    
    # **LOAD SCHEDULE JSON**
    schedule_json_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author_value}\\jsons\\{type_value}schedules.json"
    
    print(f"📂 LOADING SCHEDULE: '{schedule_json_path}'")
    
    try:
        with open(schedule_json_path, 'r') as f:
            schedule_data = json.load(f)
        next_schedule = schedule_data['next_schedule']
        target_time_12hr = next_schedule['time_12hour']  # "08:00 AM"
        target_time_24hr = next_schedule['time_24hour']  # "08:00"
        print(f"⏰ TARGET TIME: 12hr='{target_time_12hr}', 24hr='{target_time_24hr}'")
    except Exception as e:
        print(f"❌ ERROR LOADING SCHEDULE JSON: {e}")
        scheduletime.has_set_time = True
        return False
    
    # **VERIFICATION LOOP - MAX 5 ATTEMPTS**
    max_attempts = 5
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\n🔄 **TIME ATTEMPT {attempt}/{max_attempts}**")
        
        # **Load YOUR time.png file (FORMAT TEMPLATE ONLY)**
        time_img = Image.open(f"{GUI_PATH}\\time.png")
        print("📸 time.png FORMAT loaded")
        
        # **SET TESSDATA_PREFIX**
        import os
        os.environ['TESSDATA_PREFIX'] = PYTESSERACT_PATH
        
        # **OCR PNG to detect AM/PM format**
        ocr_text = pytesseract.image_to_string(time_img, config='--psm 7')
        print(f"🔤 PNG FORMAT: '{ocr_text.strip()}'")
        
        # **DETECT TIME FORMAT FROM PNG**
        clean_text = re.sub(r'[^a-zA-Z0-9:\s]', '', ocr_text.strip().upper())
        
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(AM|PM)',
            r'(\d{1,2}):(\d{2})',
        ]
        
        template_has_ampm = False
        for pattern in time_patterns:
            match = re.search(pattern, clean_text)
            if match:
                if 'AM' in match.group(0) or 'PM' in match.group(0):
                    template_has_ampm = True
                print(f"✅ PNG TIME FORMAT DETECTED: {'12-HOUR (AM/PM)' if template_has_ampm else '24-HOUR'}")
                break
        
        target_time_to_verify = target_time_12hr if template_has_ampm else target_time_24hr
        print(f"⏰ **VERIFYING AGAINST**: '{target_time_to_verify}'")
        
        # **SPECIFIC REGION SEARCH**
        REGION_LEFT = 400
        REGION_TOP = 200
        REGION_WIDTH = 600
        REGION_HEIGHT = 600
        
        print(f"\n🎯 **SEARCHING REGION:** ({REGION_LEFT},{REGION_TOP},{REGION_WIDTH},{REGION_HEIGHT})")
        
        region_screenshot = pyautogui.screenshot(region=(REGION_LEFT, REGION_TOP, REGION_WIDTH, REGION_HEIGHT))
        region_screenshot.save(f"{GUI_PATH}\\timeregion.png")
        
        region_text = pytesseract.image_to_string(region_screenshot, config='--psm 6')
        
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(AM|PM)',
            r'(\d{1,2}):(\d{2})',
        ]
        
        time_found = False
        for pattern in time_patterns:
            matches = re.finditer(pattern, region_text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                try:
                    if len(groups) >= 2:
                        hour, minute = groups[0], groups[1]
                        hour_num = int(hour)
                        minute_num = int(minute)
                        
                        if 0 <= hour_num <= 23 and 0 <= minute_num <= 59:
                            screen_time = match.group(0)
                            print(f"🕐 **TIME FIELD FOUND**: '{screen_time}'")
                            
                            # **METHOD 1: OCR POSITION**
                            print("   → Trying OCR position...")
                            data = pytesseract.image_to_data(region_screenshot, output_type=Output.DICT)
                            
                            for i, text in enumerate(data['text']):
                                text_lower = text.lower()
                                screen_time_lower = screen_time.lower()
                                time_only = screen_time_lower.replace(' am', '').replace(' pm', '')
                                
                                if (screen_time_lower in text_lower or time_only in text_lower) and data['conf'][i] > 60:
                                    time_x = REGION_LEFT + data['left'][i]
                                    time_y = REGION_TOP + data['top'][i]
                                    time_width = data['width'][i]
                                    time_height = data['height'][i]
                                    
                                    # **INPUT TIME**
                                    hh_center_x = time_x + time_width//4
                                    hh_center_y = time_y + time_height//2
                                    pyautogui.click(hh_center_x, hh_center_y)
                                    time.sleep(0.5)
                                    
                                    hh_to_type = target_time_12hr.split(':')[0].zfill(2) if template_has_ampm else target_time_24hr.split(':')[0].zfill(2)
                                    pyautogui.typewrite(hh_to_type)
                                    time.sleep(0.5)
                                    
                                    mm_center_x = hh_center_x + 27
                                    pyautogui.click(mm_center_x, hh_center_y)
                                    time.sleep(0.5)
                                    
                                    mm_to_type = target_time_12hr.split(':')[1].split()[0].zfill(2)
                                    pyautogui.typewrite(mm_to_type)
                                    time.sleep(0.5)
                                    
                                    if template_has_ampm:
                                        ampm_center_x = time_x + time_width * 3//4
                                        pyautogui.click(ampm_center_x, hh_center_y)
                                        time.sleep(0.5)
                                        ampm_to_type = target_time_12hr.split()[-1]
                                        pyautogui.typewrite(ampm_to_type)
                                        time.sleep(0.5)
                                    
                                    time.sleep(1.0)  # Wait for UI update
                                    
                                    # **VERIFICATION: CAPTURE WRITTEN TIME**
                                    time_region_written = pyautogui.screenshot(region=(time_x-20, time_y-20, time_width+40, time_height+40))
                                    time_region_written.save(f"{GUI_PATH}\\time_written.png")
                                    
                                    written_ocr = pytesseract.image_to_string(time_region_written, config='--psm 7')
                                    written_time = re.sub(r'[^a-zA-Z0-9:\s]', '', written_ocr.strip().upper())
                                    
                                    print(f"   → WRITTEN OCR: '{written_time}'")
                                    print(f"   → TARGET TIME: '{target_time_to_verify}'")
                                    
                                    if target_time_to_verify.upper() in written_time or written_time.strip() == target_time_to_verify.upper():
                                        print("✅ **TIME VERIFICATION: ACCURATE & SAME RECORD!** 🎉")
                                        scheduletime.has_set_time = True
                                        return True
                                    else:
                                        print("❌ **TIME VERIFICATION FAILED** - Restarting...")
                                        time_found = True
                                        break
                            
                            if time_found:
                                break
                            
                            # **METHOD 2: TEMPLATE BACKUP**
                            print("   → OCR failed, using time.png template...")
                            located = pyautogui.locateOnScreen(
                                f"{GUI_PATH}\\time.png", 
                                confidence=0.7,
                                region=(REGION_LEFT, REGION_TOP, REGION_WIDTH, REGION_HEIGHT)
                            )
                            
                            if located:
                                screen_x, screen_y, found_width, found_height = located
                                
                                hh_center_x = screen_x + found_width//4
                                hh_center_y = screen_y + found_height//2
                                pyautogui.click(hh_center_x, hh_center_y)
                                time.sleep(0.5)
                                
                                hh_to_type = target_time_12hr.split(':')[0].zfill(2) if template_has_ampm else target_time_24hr.split(':')[0].zfill(2)
                                pyautogui.typewrite(hh_to_type)
                                time.sleep(0.5)
                                
                                mm_center_x = hh_center_x + 27
                                pyautogui.click(mm_center_x, hh_center_y)
                                time.sleep(0.5)
                                
                                mm_to_type = target_time_12hr.split(':')[1].split()[0].zfill(2)
                                pyautogui.typewrite(mm_to_type)
                                time.sleep(0.5)
                                
                                if template_has_ampm:
                                    ampm_center_x = screen_x + found_width * 3//4
                                    pyautogui.click(ampm_center_x, hh_center_y)
                                    time.sleep(0.5)
                                    ampm_to_type = target_time_12hr.split()[-1]
                                    pyautogui.typewrite(ampm_to_type)
                                    time.sleep(0.5)
                                
                                time.sleep(1.0)
                                
                                # **VERIFICATION**
                                time_region_written = pyautogui.screenshot(region=(screen_x-20, screen_y-20, found_width+40, found_height+40))
                                time_region_written.save(f"{GUI_PATH}\\time_written.png")
                                
                                written_ocr = pytesseract.image_to_string(time_region_written, config='--psm 7')
                                written_time = re.sub(r'[^a-zA-Z0-9:\s]', '', written_ocr.strip().upper())
                                
                                print(f"   → WRITTEN OCR: '{written_time}'")
                                print(f"   → TARGET TIME: '{target_time_to_verify}'")
                                
                                if target_time_to_verify.upper() in written_time or written_time.strip() == target_time_to_verify.upper():
                                    print("✅ **TIME VERIFICATION: ACCURATE & SAME RECORD VIA TEMPLATE!** 🎉")
                                    scheduletime.has_set_time = True
                                    return True
                                else:
                                    print("❌ **TIME VERIFICATION FAILED VIA TEMPLATE** - Restarting...")
                                    time_found = True
                                    break
                            
                except Exception as e:
                    print(f"   → ERROR: {e}")
                    continue
        
        if time_found:
            attempt += 1
            time.sleep(1.0)
            continue
        
        break
    
    # MAX ATTEMPTS EXHAUSTED
    scheduletime.has_set_time = True
    print(f"❌ **TIME FAILED AFTER {max_attempts} ATTEMPTS**")
    return False



def click_schedule_button():
    """Click schedule button with tracker."""
    # Initialize tracker if not already set
    if not hasattr(click_schedule_button, 'has_scheduled'):
        click_schedule_button.has_scheduled = False

    # Check if click_schedule_button has already run
    if click_schedule_button.has_scheduled:
        print("click_schedule_button already executed. Skipping operation.")
        return

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
        uploadedjpgs()
        
        # Reload page to start a new process
        print("Reloading page to start a new scheduling process...")
        reset_trackers()
        driver.refresh()
        time.sleep(2)
        
        # UPDATE TRACKER - SUCCESS
        click_schedule_button.has_scheduled = True
        print("✅ Updated tracker: click_schedule_button.has_scheduled = True")

    except Exception as e:
        # MARK AS DONE EVEN ON ERROR
        click_schedule_button.has_scheduled = True
        print(f"⚠️ click_schedule_button failed but marked as done: {e}")
        
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
        print(f"Failed to schedule: {e}")
        raise
def uploadedjpgs():
    """Upload JPGs with tracker."""
    # Initialize tracker if not already set
    if not hasattr(uploadedjpgs, 'has_uploaded'):
        uploadedjpgs.has_uploaded = False

    # Check if uploadedjpgs has already run
    if uploadedjpgs.has_uploaded:
        print("uploadedjpgs already executed. Skipping operation.")
        return

    # Load configuration from JSON
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        # Use outputpath from JSON as source_dir, replacing authorvalue
        source_dir = config['outputpath'].replace('authorvalue', author)
    except Exception as e:
        print(f"Failed to load or parse {JSON_CONFIG_PATH}: {e}")
        uploadedjpgs.has_uploaded = True  # Mark as done even on error
        return

    # Construct destination directory with author value
    dest_dir = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}"
    source_file = 'card_x.jpg'

    # Create source directory if it doesn't exist
    if not os.path.exists(source_dir):
        try:
            os.makedirs(source_dir)
            print(f"Created source directory: {source_dir}")
        except Exception as e:
            print(f"Failed to create source directory {source_dir}: {e}")
            uploadedjpgs.has_uploaded = True  # Mark as done even on error
            return

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            print(f"Created destination directory: {dest_dir}")
        except Exception as e:
            print(f"Failed to create destination directory {dest_dir}: {e}")
            uploadedjpgs.has_uploaded = True  # Mark as done even on error
            return

    # Check if source file exists
    source_path = os.path.join(source_dir, source_file)
    if not os.path.exists(source_path):
        print(f"Source file does not exist: {source_path}")
        uploadedjpgs.has_uploaded = True  # Mark as done even on error
        return

    # Get all card_N.jpg files in the destination directory
    try:
        dest_files = [f for f in os.listdir(dest_dir) if re.match(r'card_(\d+)\.jpg$', f.lower())]
    except Exception as e:
        print(f"Failed to list files in destination directory {dest_dir}: {e}")
        uploadedjpgs.has_uploaded = True  # Mark as done even on error
        return

    # Extract numbers from existing card_N.jpg files
    existing_numbers = []
    for file in dest_files:
        match = re.match(r'card_(\d+)\.jpg$', file.lower())
        if match:
            existing_numbers.append(int(match.group(1)))

    # Determine the next number
    next_num = max(existing_numbers) + 1 if existing_numbers else 1

    # Define destination file path
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
        update_calendar()
        
        # UPDATE TRACKER - SUCCESS
        uploadedjpgs.has_uploaded = True
        print("✅ Updated tracker: uploadedjpgs.has_uploaded = True")
        
    except Exception as e:
        print(f"Failed to copy or rename {source_file} to {dest_file}: {e}")
        # MARK AS DONE EVEN ON ERROR
        uploadedjpgs.has_uploaded = True
        print("⚠️ uploadedjpgs failed but marked as done")


def main():
    try:
        # Initialize WebDriver
        driver, wait = initialize_driver(mode="headed")
        
        # Execute launch_profile (includes continuous URL checking, caption writing, schedule toggling, and media interaction)
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




