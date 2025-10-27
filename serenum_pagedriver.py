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


# Global driver and wait objects
driver = None
wait = None

# Global JSON configuration path
JSON_CONFIG_PATH = r'C:\xampp\htdocs\serenum\pageauthors.json'
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
    """Reset all function trackers to their initial state, excluding update_calendar."""
    writecaption.last_written_caption = None
    togglesharephotosandvideos.is_toggled = False
    toggleschedule.is_toggled = False
    selectmedia.has_uploaded = False
    print("Reset all function trackers: last_written_caption, is_toggled (togglesharephotosandvideos), is_toggled (toggleschedule), has_uploaded")

def update_calendar():
    """Update the calendar and write to JSON, conditional on driverprogress.json status."""
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
    timeorders_path = r"C:\xampp\htdocs\serenum	imeorders.json"
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
    timeorders_path = r"C:\xampp\htdocs\serenum	imeorders.json"
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
                    update_calendar()
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
                    markjpgs()
                    togglesharephotosandvideos()
                    writecaption()
                    toggleschedule()
                    set_schedule()
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
    # Load configuration from JSON
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        processpathfrom = config.get('processpathfrom', 'freshjpgs')  # Default to 'freshjpgs' if not specified
        # Replace 'authorvalue' placeholder with the actual author value
        if processpathfrom == 'freshjpgs':
            directory = config['inputpath'].replace('authorvalue', author)
        elif processpathfrom == 'uploadedjpgs':
            # Construct base path for uploadedjpgs
            base_uploaded_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}"
            if not os.path.exists(base_uploaded_path):
                print(f"Base uploaded jpgs directory does not exist: {base_uploaded_path}")
                return
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
                return
            # Sort folders by date (most recent first)
            try:
                date_folders.sort(key=lambda x: datetime.strptime(x, "%d-%B-%Y"), reverse=True)
                directory = os.path.join(base_uploaded_path, date_folders[0])
            except ValueError as e:
                print(f"Error sorting date folders in {base_uploaded_path}: {e}")
                return
        else:
            print(f"Invalid processpathfrom value: {processpathfrom}. Must be 'freshjpgs' or 'uploadedjpgs'.")
            return
        output_dir = config['outputpath'].replace('authorvalue', author)
    except Exception as e:
        print(f"Failed to load or parse {JSON_CONFIG_PATH}: {e}")
        return

    # Verify that output path ends with the author folder
    if not output_dir.endswith(author):
        print(f"Error: outputpath ({output_dir}) does not end with author folder '{author}'")
        return
    
    # For freshjpgs, verify input directory ends with author
    if processpathfrom == 'freshjpgs' and not directory.endswith(author):
        print(f"Error: input directory ({directory}) does not end with author folder '{author}'")
        return
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except Exception as e:
            print(f"Failed to create output directory {output_dir}: {e}")
            return
    
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
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


def writecaption():
    """Enter a random caption using GUI automation with same variable tracking as writecaption(),
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
        if not hasattr(writecaption, 'last_written_caption'):
            writecaption.last_written_caption = None
        
        # GUI screen regions
        screen_width, screen_height = pyautogui.size()
        top = (0, 0, screen_width, screen_height)
        bottom = (0, screen_height // 2, screen_width, screen_height // 2)
        
        # Locate text area using GUI
        text = pyautogui.locateOnScreen(f'{GUI_PATH}\\text.png', confidence=0.8, region=top)
        
        if not text:
            print("Text area image not found")
            return False
        
        x, y = pyautogui.center(text)
        pyautogui.click(x, y + 50)
        print("Found text area, clicked text area")
        time.sleep(2)
        
        # Get current text in text field using GUI
        # Select all text (Ctrl+A)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        
        # Copy selected text to clipboard
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        
        # Get current text from clipboard
        current_text = pyperclip.paste().strip()
        print(f"Current text in field (GUI): '{current_text}'")
        
        # EXACT SAME LOGIC FOR TEXT VALIDATION & WRITING
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
        
        return True
        
    except Exception as e:
        print(f"Failed to enter text (GUI): {str(e)}")
        return False        






def togglesharephotosandvideos():
    """Locate the 'Photos and Videos' section and click on any input or button within its div, using a tracker to avoid redundant clicks."""
    try:
        # Initialize tracker if not already set
        if not hasattr(togglesharephotosandvideos, 'is_toggled'):
            togglesharephotosandvideos.is_toggled = False

        # Check if the section was already toggled
        if togglesharephotosandvideos.is_toggled:
            print("Photos and Videos section already toggled. Skipping click operation.")
            return

        # Wait for and locate the 'Photos and Videos' section
        media_section = wait.until(
            EC.presence_of_element_located((By.XPATH, 
                "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'photos and videos') or "
                "contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add media') or "
                "contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add photos/video') or "
                "contains(@aria-label, 'Photos and Videos') or contains(@aria-label, 'Add Media') or "
                "contains(@aria-label, 'Add Photos/Video') or contains(@data-testid, 'media-upload') or "
                "contains(@data-testid, 'composer-media')]"
            ))
        )
        # Log the outer HTML of the media section for debugging
        print("Located 'Photos and Videos' section. Outer HTML:", media_section.get_attribute('outerHTML')[:200], "...")
        
        # Find any clickable element within the media section
        media_element = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                ".//input[@type='file'] | .//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add') or "
                "contains(@aria-label, 'Add') or contains(@data-testid, 'media')] | "
                ".//div[@role='button' or contains(@class, 'media') or contains(@aria-label, 'Add') or contains(@data-testid, 'media')]"
            ))
        )
        media_element.click()
        print("Clicked input or button in 'Photos and Videos' section:", media_element.get_attribute('outerHTML')[:100], "...")
        
        # Update tracker to indicate the section has been toggled
        togglesharephotosandvideos.is_toggled = True
        print("Updated tracker: is_toggled set to True")
        
        time.sleep(2)  # Pause to allow any UI updates after clicking
        selectmedia()
        
    except Exception as e:
        print(f"Failed to locate or click in 'Photos and Videos' section: {str(e)}")
        try:
            # Alternative locator for media section
            media_section = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 
                    "div[aria-label*='Media' i], div[class*='media-upload' i], div[data-testid*='media' i], "
                    "button[aria-label*='Add Media' i], button[data-testid*='media' i], "
                    "div[aria-label*='Add Photos/Video' i]"
                ))
            )
            print("Located 'Photos and Videos' section using alternative locator. Outer HTML:", 
                  media_section.get_attribute('outerHTML')[:200], "...")
            
            # Find any clickable element within the alternative media section
            media_element = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "input[type='file'], button[class*='media' i], div[role='button'], "
                    "div[class*='media' i], button[data-testid*='media' i], div[aria-label*='Add' i]"
                ))
            )
            media_element.click()
            print("Clicked input or button in 'Photos and Videos' section using alternative locator:", 
                  media_element.get_attribute('outerHTML')[:100], "...")
            
            # Update tracker to indicate the section has been toggled
            togglesharephotosandvideos.is_toggled = True
            print("Updated tracker: is_toggled set to True (alternative locator)")
            
            
            time.sleep(2)  # Pause to allow UI updates
            selectmedia()
            
        except Exception as e2:
            print(f"Alternative locator for 'Photos and Videos' section failed: {str(e2)}")
            raise Exception("Could not locate or click input/button in 'Photos and Videos' section")

def selectmedia():
    """Select media by entering the file path and pressing Enter, with a tracker to ensure it runs only once per session."""
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
            print(f"Media file does not exist: {file_path}")
            return

        # Input the file path and press Enter
        pyautogui.write(file_path)
        pyautogui.press("enter")
        print(f"Entered media file path: {file_path} and pressed Enter")

        # Update tracker to indicate media has been selected
        selectmedia.has_uploaded = True
        print("Updated tracker: has_uploaded set to True")

        time.sleep(3)  # Pause to allow file dialog to process
        confirmselectedmedia()

    except Exception as e:
        print(f"Failed to select media: {str(e)}")
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
def set_schedule():
    """
    Set schedule by reading target date and time from {type_value}schedules.json.
    Checks if current UI date matches JSON date before setting.
    Relies on extract_texts for time verification, skipping UI time input checks.
    Skips verification if no changes are made.
    Constructs input path using author and type from JSON_CONFIG_PATH.
    Detects 24-hour vs 12-hour format and sets time accordingly.
    Reloads page on click interception.
    """
    # Load configuration from JSON_CONFIG_PATH
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        type_value = config.get('type', '')  # Get type from config, if available
        schedules_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}\\jsons\\{type_value}schedules.json"
    except Exception as e:
        print(f"Failed to load or parse {JSON_CONFIG_PATH}: {e}")
        return

    # Load target date and time from {type_value}schedules.json
    try:
        with open(schedules_path, 'r') as json_file:
            json_data = json.load(json_file)
        next_schedule = json_data.get('next_schedule', {})
        target_date = next_schedule.get('date', '')  # e.g., "01/11/2025"
        target_time_12h = next_schedule.get('time_12hour', '')  # e.g., "07:00 AM"
        target_time_24h = next_schedule.get('time_24hour', '')  # e.g., "07:00"
        
        if not target_date or not target_time_12h or not target_time_24h:
            raise Exception("Missing date, time_12hour, or time_24hour in schedules.json")
        
        # Parse 12-hour time (e.g., "07:00 AM" -> hour: "07", minute: "00", period: "AM")
        match_12h = re.match(r"(\d{1,2}):(\d{2})\s*(AM|PM)", target_time_12h, re.IGNORECASE)
        if not match_12h:
            raise Exception("Invalid 12-hour time format in schedules.json")
        hour_12h, minute_12h, period = match_12h.groups()
        
        # Parse 24-hour time (e.g., "07:00" -> hour: "07", minute: "00")
        match_24h = re.match(r"(\d{1,2}):(\d{2})", target_time_24h)
        if not match_24h:
            raise Exception("Invalid 24-hour time format in schedules.json")
        hour_24h, minute_24h = match_24h.groups()
        
        print(f"Target schedule: {target_date} at {target_time_12h} (12h) / {target_time_24h} (24h)")
    except Exception as e:
        print(f"Failed to read or parse {schedules_path}: {e}")
        return

    # --- FIXED COMPREHENSIVE DATE FORMAT GENERATOR ---
    def generate_all_date_formats(target_date):
        """Generate ALL possible date formats from target_date (dd/mm/yyyy) - BOTH PADDED & UNPADDED"""
        # Parse target_date (dd/mm/yyyy) -> day, month, year
        day, month, year = target_date.split('/')
        day_unpadded = day.lstrip('0')  # "01" -> "1"
        day_padded = day.zfill(2)       # "1" -> "01"
        month_padded = month.zfill(2)
        year_short = year[-2:]
        
        # Month names
        month_map = {
            '01': ('January', 'Jan'), '02': ('February', 'Feb'), '03': ('March', 'Mar'),
            '04': ('April', 'Apr'), '05': ('May', 'May'), '06': ('June', 'Jun'),
            '07': ('July', 'Jul'), '08': ('August', 'Aug'), '09': ('September', 'Sep'),
            '10': ('October', 'Oct'), '11': ('November', 'Nov'), '12': ('December', 'Dec')
        }
        full_month, short_month = month_map[month]
        
        date_formats = {}
        
        # Standard with slashes - BOTH padded & unpadded
        date_formats['dd/mm/yyyy'] = f"{day_padded}/{month_padded}/{year}"
        date_formats['d/mm/yyyy'] = f"{day_unpadded}/{month_padded}/{year}"
        date_formats['dd/mm/yy'] = f"{day_padded}/{month_padded}/{year_short}"
        date_formats['d/mm/yy'] = f"{day_unpadded}/{month_padded}/{year_short}"
        
        # Standard with dashes - BOTH padded & unpadded
        date_formats['dd-mm-yyyy'] = f"{day_padded}-{month_padded}-{year}"
        date_formats['d-mm-yyyy'] = f"{day_unpadded}-{month_padded}-{year}"
        date_formats['dd-mm-yy'] = f"{day_padded}-{month_padded}-{year_short}"
        date_formats['d-mm-yy'] = f"{day_unpadded}-{month_padded}-{year_short}"
        
        # With spaces - BOTH padded & unpadded
        date_formats['dd month yyyy'] = f"{day_padded} {full_month} {year}"
        date_formats['d month yyyy'] = f"{day_unpadded} {full_month} {year}"
        date_formats['dd mon yyyy'] = f"{day_padded} {short_month} {year}"
        date_formats['d mon yyyy'] = f"{day_unpadded} {short_month} {year}"
        date_formats['month dd, yyyy'] = f"{full_month} {day_padded}, {year}"
        date_formats['month d, yyyy'] = f"{full_month} {day_unpadded}, {year}"
        date_formats['mon dd yyyy'] = f"{short_month} {day_padded} {year}"
        date_formats['mon d yyyy'] = f"{short_month} {day_unpadded} {year}"
        
        # NO SPACE VARIANTS (for OCR) - BOTH padded & unpadded
        date_formats['dmonthyyyy'] = f"{day_unpadded}{full_month}{year}"
        date_formats['dmonyyyy'] = f"{day_unpadded}{short_month}{year}"
        date_formats['ddmonthyyyy'] = f"{day_padded}{full_month}{year}"
        date_formats['ddmonyyyy'] = f"{day_padded}{short_month}{year}"
        date_formats['monthdyyyy'] = f"{full_month}{day_unpadded}{year}"
        date_formats['monthddyyyy'] = f"{full_month}{day_padded}{year}"
        date_formats['mondyyyy'] = f"{short_month}{day_unpadded}{year}"
        date_formats['monddyyyy'] = f"{short_month}{day_padded}{year}"
        
        # Comma variants without space - BOTH padded & unpadded
        date_formats['monthd,yyyy'] = f"{full_month}{day_unpadded},{year}"
        date_formats['monthdd,yyyy'] = f"{full_month}{day_padded},{year}"
        date_formats['mond,yyyy'] = f"{short_month}{day_unpadded},{year}"
        date_formats['mondd,yyyy'] = f"{short_month}{day_padded},{year}"
        
        return date_formats

    try:
        # --- 1. Wait for schedule panel ---
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'schedule')]")
            )
        )
        print("Schedule panel loaded.")
        time.sleep(2)

        # --- 2. Get inputs ---
        inputs = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
        )
        print(f"Found {len(inputs)} inputs.")

        date_input = hour_input = minute_input = am_pm_input = None
        for i, inp in enumerate(inputs):
            ph = inp.get_attribute("placeholder") or ""
            al = inp.get_attribute("aria-label") or ""
            if "dd/mm/yyyy" in ph.lower():
                date_input = inp
                print(f"Date input at [{i}]: {ph}")
            elif "hour" in al.lower():
                hour_input = inp
                print(f"Hour input at [{i}]: {al}")
            elif "minute" in al.lower():
                minute_input = inp
                print(f"Minute input at [{i}]: {al}")
            elif "am" in al.lower() or "pm" in al.lower():
                am_pm_input = inp
                print(f"AM/PM input at [{i}]: {al}")

        if not all([date_input, hour_input, minute_input]):
            raise Exception("Missing date, hour, or minute inputs")

        # --- 3. Get existing date ---
        current_date = driver.execute_script("return arguments[0].value", date_input) or ""
        print(f"Current UI values - Date: '{current_date}'")

        # --- 4. Get existing time using extract_texts ---
        print("Extracting existing time...")
        extractedtexts, extracted_time, found_texts = extract_texts()
        print(f"Extracted time: '{extracted_time}', Found texts: {found_texts}")

        # --- 5. DETECT 24H vs 12H FORMAT ---
        print("Detecting time format (24h vs 12h)...")
        is_24h_format = True if not am_pm_input else False
        if is_24h_format:
            print("✓ Detected 24-hour format (no AM/PM selector found)")
        else:
            print("✓ Detected 12-hour format (AM/PM selector found)")

        # --- 6. CHECK IF VALUES MATCH JSON ---
        # Generate ALL possible formats for target date
        all_target_formats = generate_all_date_formats(target_date)
        print(f"Generated {len(all_target_formats)} possible target date formats")
        
        date_matches = False
        # Check if current_date matches ANY target format
        for fmt_name, fmt_value in all_target_formats.items():
            if current_date.strip() == fmt_value.strip():
                date_matches = True
                print(f"✓ Date already matches target date (format: {fmt_name})")
                break
        
        # Compare time using extract_texts
        time_matches = False
        if is_24h_format:
            expected_time = f"Time: {hour_24h}:{minute_24h}"
            if extracted_time == expected_time:
                time_matches = True
                print("✓ Time already matches target time (24h)")
        else:
            expected_time = f"Time: {hour_12h.lstrip('0')}:{minute_12h}"
            alternative_time = f"Time: {hour_12h}:{minute_12h}"
            if extracted_time in [expected_time, alternative_time]:
                time_matches = True
                print("✓ Time already matches target time (12h)")

        # Skip setting and verification if both date and time match
        if date_matches and time_matches:
            print("✓ Schedule already set correctly, skipping update and verification.")
            return

        # --- 7. SET DATE (if needed) ---
        if not date_matches:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", date_input)
                date_input.click()
                time.sleep(0.5)
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                print("Selected all text in date input.")
                time.sleep(0.5)
                ActionChains(driver).send_keys(target_date).perform()
                print(f"Pasted date: {target_date}")
                time.sleep(0.5)
                date_input.send_keys(Keys.TAB)
                print("Tabbed out of date input.")
                time.sleep(1)
            except Exception as e:
                if "element click intercepted" in str(e).lower():
                    print("Element click intercepted in date input. Reloading page and resetting trackers...")
                    reset_trackers()
                    driver.refresh()
                    raise Exception("Page reloaded due to click interception")
                raise

        # --- 8. SET TIME (if needed) ---
        if not time_matches:
            # Set hour
            try:
                hour_input.click()
                time.sleep(0.5)
                hour_input.clear()
                time.sleep(0.5)
                
                if is_24h_format:
                    hour_input.send_keys(hour_24h)
                    print(f"Set 24h hour: {hour_24h}")
                else:
                    hour_input.send_keys(hour_12h.lstrip('0'))
                    print(f"Set 12h hour: {hour_12h.lstrip('0')}")
                    if am_pm_input:
                        am_pm_input.click()
                        time.sleep(0.5)
                        ActionChains(driver).send_keys(period.upper()).send_keys(Keys.ENTER).perform()
                        print(f"Selected {period.upper()}")
                
                hour_input.send_keys(Keys.TAB)
                time.sleep(1)
            except Exception as e:
                if "element click intercepted" in str(e).lower():
                    print("Element click intercepted in hour input. Reloading page and resetting trackers...")
                    reset_trackers()
                    driver.refresh()
                    raise Exception("Page reloaded due to click interception")
                raise

            # Set minutes
            try:
                minute_input.click()
                time.sleep(0.5)
                minute_input.clear()
                time.sleep(0.5)
                minute_input.send_keys(minute_24h)
                print(f"Set minute: {minute_24h}")
                minute_input.send_keys(Keys.TAB)
                time.sleep(1)
            except Exception as e:
                if "element click intercepted" in str(e).lower():
                    print("Element click intercepted in minute input. Reloading page and resetting trackers...")
                    reset_trackers()
                    driver.refresh()
                    raise Exception("Page reloaded due to click interception")
                raise
        else:
            print("Time already correct, skipping time update.")

        # --- 9. Get new time using extract_texts ---
        print("Extracting new time...")
        extractedtexts, new_time, found_texts = extract_texts()
        print(f"After setting - Extracted time: '{new_time}', Found texts: {found_texts}")

        # --- 10. VERIFY ---
        time.sleep(1)  # Wait for UI to stabilize
        final_date = driver.execute_script("return arguments[0].value", date_input) or ""
        print(f"FINAL: Date='{final_date}', Time='{new_time}'")

        # Verify date - Check if final_date matches ANY target format
        date_verified = False
        for fmt_name, fmt_value in all_target_formats.items():
            if final_date.strip() == fmt_value.strip():
                date_verified = True
                print(f"✓ Date verified! (format: {fmt_name})")
                break
        
        if not date_verified:
            # Show all possible formats for debugging
            print("❌ Date verification failed. Expected formats:")
            for fmt_name, fmt_value in all_target_formats.items():
                print(f"  {fmt_name}: '{fmt_value}'")
            raise Exception(f"Date not set: '{final_date}' doesn't match any expected format")

        # Verify time
        if is_24h_format:
            expected_time = f"Time: {hour_24h}:{minute_24h}"
            if new_time != expected_time:
                raise Exception(f"Time not set (24h): '{new_time}' != '{expected_time}'")
        else:
            expected_time = f"Time: {hour_12h.lstrip('0')}:{minute_12h}"
            if new_time not in [expected_time, f"Time: {hour_12h}:{minute_12h}"]:
                raise Exception(f"Time not set (12h): '{new_time}' != '{expected_time}' or 'Time: {hour_12h}:{minute_12h}'")

        print("✓ Schedule set successfully!")

    except Exception as e:
        if "page reloaded" in str(e).lower():
            raise  # Let the exception propagate to trigger page reload in launch_profile
        print(f"Schedule failed: {e}")
        # Check for overlay
        overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
        if overlay:
            print("Detected overlay blocking interaction. Reloading page and resetting trackers...")
            reset_trackers()
            driver.refresh()
            raise Exception("Page reloaded due to overlay")
        raise
    

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
        uploadedjpgs()

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
    """Upload JPGs with tracker, organizing by date in subfolders."""
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
            uploadedjpgs.has_uploaded = True  # Mark as done even on error
            return

    # Create destination directory (with date) if it doesn't exist
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

    # Get all card_N.jpg files in the date-specific destination directory
    try:
        dest_files = [f for f in os.listdir(dest_dir) if re.match(r'card_(\d+)\.jpg$', f.lower())]
    except Exception as e:
        print(f"Failed to list files in destination directory {dest_dir}: {e}")
        uploadedjpgs.has_uploaded = True  # Mark as done even on error
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

