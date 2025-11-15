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
import random
import pytz
import re
from PIL import Image
import calendar
import json
import os
import time
from datetime import datetime, timedelta
import shutil
import psutil
import pyautogui
import pyperclip
import cv2
import pytesseract
from PIL import ImageGrab
import numpy as np
import logging
import random
from PIL import Image
import calendar
import json
import os
import time
from datetime import datetime, timedelta
import shutil
import pytz
import csv
import re
import requests 
from typing import Tuple, List
import os
import json
import numpy as np
from PIL import Image
from pathlib import Path
from PIL import ImageFilter
import imghdr
import traceback


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
    """Initialize Chrome WebDriver using a specific local profile (safe copy, offline)."""
    global driver, wait
    print("Closing existing Chrome instances...")
    closed_any = False
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if name and name.lower() in ['chrome.exe', 'chromedriver.exe']:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except psutil.TimeoutExpired:
                    proc.kill()
                closed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if closed_any:
        print("Closed Chrome process(es).")
    time.sleep(1)

    # --- Local Chrome & Driver paths ---
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver_path = r"C:\Users\PC\.wdm\drivers\chromedriver\win64\141.0.7390.122\chromedriver-win32\chromedriver.exe"

    if not os.path.exists(chrome_path):
        raise FileNotFoundError(f"Chrome not found at: {chrome_path}")
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"ChromeDriver not found at: {driver_path}")

    # --- Profile setup ---
    real_user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    source_profile = os.path.join(real_user_data, "Profile 1")  # Change if using "Default"
    selenium_profile = os.path.expanduser(r"~\.chrome_selenium_profile")

    if not os.path.exists(selenium_profile):
        print("Creating Selenium Chrome profile copy...")
        shutil.copytree(source_profile, selenium_profile, dirs_exist_ok=True)
    else:
        print("Using existing Selenium profile...")

    # --- Chrome Options ---
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument(f"--user-data-dir={selenium_profile}")
    chrome_options.add_argument("--profile-directory=Default")

    if mode == "headless":
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
    else:
        chrome_options.add_argument("--start-maximized")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # --- Start WebDriver ---
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 15)
    print("ChromeDriver initialized successfully with Profile 1 (offline mode).")
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
                reset_trackers()
                try:
                    overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
                    if overlay:
                        print("Detected overlay. Reloading page...")
                        driver.refresh()
                        time.sleep(2)
                        continue

                    url_input = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='url'] | //input[@placeholder*='URL'] | //input[@name='url']"))
                    )
                    url_input.clear()
                    url_input.send_keys(uploadpost_url)
                    print(f"Filled URL input with: {uploadpost_url}")

                    try:
                        submit_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //button[contains(text(), 'Go')] | //button[contains(text(), 'Navigate')]"))
                        )
                        submit_button.click()
                    except:
                        print("No submit button found. Navigating directly...")
                        driver.get(uploadpost_url)
                except:
                    print(f"No URL input field. Navigating directly to {uploadpost_url}.")
                    driver.get(uploadpost_url)
                
                print("Waiting 2 seconds before rechecking URL...")
                time.sleep(2)

        # Continuous rechecking loop
        last_url = driver.current_url
        while True:
            try:
                current_url = driver.current_url
                print("Checking if URL is correct...")

                if uploadpost_url in current_url:
                    if current_url != last_url:
                        print(f"URL changed: {last_url} → {current_url}. Resetting trackers.")
                        reset_trackers()
                        last_url = current_url

                    # Update progress JSON
                    driver_progress_path = r"C:\xampp\htdocs\serenum\driverprogress.json"
                    progress_data = {"driver": "started", "scheduled": "waiting"}
                    try:
                        with open(driver_progress_path, 'w') as f:
                            json.dump(progress_data, f, indent=4)
                        print(f"Updated {driver_progress_path}")
                    except Exception as e:
                        print(f"Failed to write progress: {e}")

                    print(f"URL correct. Proceeding with post actions...")
                    firstbatch()
                    secondbatch()
                else:
                    print(f"URL MISMATCH: {current_url} ≠ {uploadpost_url}")
                    print("Forcing navigation to correct URL...")
                    reset_trackers()
                    last_url = current_url

                    # CRITICAL FIX: Use driver.get() instead of refresh()
                    driver.get(uploadpost_url)
                    print(f"Navigated to: {uploadpost_url}")

                    # Wait for composer to load
                    try:
                        wait.until(
                            EC.presence_of_element_located((By.XPATH, "//textarea | //div[@contenteditable='true'] | //input[@placeholder='Write something...']"))
                        )
                        print("Upload composer loaded after forced navigation.")
                    except Exception as e:
                        print(f"Composer not ready after navigation: {e}. Will retry...")

                time.sleep(2)

            except KeyboardInterrupt:
                print("Script interrupted. Closing browser...")
                raise
            except Exception as e:
                print(f"Error in recheck loop: {str(e)}")
                overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
                if overlay:
                    print("Overlay detected. Refreshing...")
                    reset_trackers()
                    driver.refresh()
                    time.sleep(2)
                    continue

                current_url = driver.current_url
                if current_url != last_url:
                    print(f"URL changed during error: {last_url} → {current_url}. Resetting...")
                    reset_trackers()
                    last_url = current_url

                # If still wrong, force correct URL
                if uploadpost_url not in current_url:
                    print("Still on wrong URL. Forcing correct one...")
                    driver.get(uploadpost_url)

                time.sleep(2)

    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            raise
        print(f"Fatal error in launch_profile: {str(e)}")
        print("Browser remains open for debugging.")
        input("Press Enter to close...")  # Optional: pause before crash
        raise
        
def reset_trackers():
    """Reset all function trackers to their initial state, excluding update_calendar."""
    # ---- Caption writers ----
    writecaption_ocr.last_written_caption = None
    if hasattr(writecaption_element, 'last_written_caption'):
        writecaption_element.last_written_caption = None
    writecaption_element.has_written = False

    # ---- set_webschedule (NEW) ----
    set_webschedule.has_set = False  # ADD THIS LINE

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
        "has_set (set_webschedule), "
        "is_toggled (toggleaddphoto), is_toggled (toggleschedule), "
        "has_uploaded, is_dropdown_opened, is_see_more_clicked, "
        "groups_selected, is_page_selected"
    )
    
def manage_group_switch():
    """
    Handles **only** group switching:
      • switch → move current_selected → last_selected, clear current_selected
      • no     → clear last_selected
    """
    import os, json

    cfg_path   = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    upload_path = r"C:\xampp\htdocs\serenum\files\groups\uploadgroups.json"

    # ---------- read config ----------
    group_switch = "no"
    if os.path.exists(cfg_path) and os.path.getsize(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            group_switch = cfg.get("group_switch", "no").lower()
        except Exception as e:
            print(f"[group] config read error: {e}")

    if group_switch not in ("switch", "no"):
        group_switch = "no"

    # ---------- read / init uploadgroups ----------
    default = {
        "groups_selected": {
            "last_selected": [],
            "current_selected": {"1st": "", "2nd": "", "3rd": ""},
            "status": "no groups selected"
        }
    }

    data = default
    if os.path.exists(upload_path) and os.path.getsize(upload_path):
        try:
            with open(upload_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[group] uploadgroups read error: {e}")

    cur = [
        data.get("groups_selected", {}).get("current_selected", {}).get("1st", ""),
        data.get("groups_selected", {}).get("current_selected", {}).get("2nd", ""),
        data.get("groups_selected", {}).get("current_selected", {}).get("3rd", "")
    ]
    cur = [x for x in cur if x]

    # ---------- apply switch ----------
    if group_switch == "switch":
        last = data.get("groups_selected", {}).get("last_selected", [])
        last = list(set(last + cur))
        data["groups_selected"]["last_selected"] = last
        data["groups_selected"]["current_selected"] = {"1st": "", "2nd": "", "3rd": ""}
        print(f"[group] switched → last_selected = {last}")
    else:
        data["groups_selected"]["last_selected"] = []
        print("[group] cleared last_selected")

    # ---------- write back ----------
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    try:
        with open(upload_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("[group] uploadgroups.json updated")
        return True
    except Exception as e:
        print(f"[group] write error: {e}")
        return False
        


def fetch_urls() -> list[str]:
    """
    Launch headless Chrome, fetch JPG URLs, save to JSON,
    and PRINT status messages (hardcoded inside).
    """
    # ----- ALL HARDCODED PATHS & URL -----
    TARGET_URL = "https://jpgsvault.rf.gd/loadimagesurl.php?i=1"
    CHROME_BINARY = r"C:\xampp\htdocs\CIPHER\googlechrome\Google\Chrome\Application\chrome.exe"
    OUTPUT_FILE = r"C:\xampp\htdocs\serenum\files\fetchedjpgsurl.json"
    # -------------------------------------

    print("Starting headless Chrome...")
    print(f"Target URL: {TARGET_URL}")
    print(f"Output file: {OUTPUT_FILE}")

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-autofill")
    options.add_argument("--log-level=3")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    if os.path.exists(CHROME_BINARY):
        options.binary_location = CHROME_BINARY
        print("Using custom Chrome binary.")
    else:
        print("Custom Chrome binary not found. Using system default.")

    driver = None
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(driver_version="139.0.7258.128").install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        print("Navigating to page...")
        driver.get(TARGET_URL)
        driver.implicitly_wait(5)

        print("Extracting JPG URLs from <div class=\"url\">...")
        html = driver.page_source
        matches = re.findall(r'<div class="url">([^<]+)</div>', html)

        jpg_urls = []
        for url in matches:
            url = url.strip().replace("\\", "/")
            if url.lower().endswith(('.jpg', '.jpeg')) and url not in jpg_urls:
                jpg_urls.append(url)

        total = len(jpg_urls)
        print(f"Extracted {total} unique JPG URL(s).")

        # Save JSON
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        payload = {
            "source_url": TARGET_URL,
            "fetched_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "total_jpgs": total,
            "jpg_urls": jpg_urls
        }
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)


        return jpg_urls

    except Exception as e:
        print("FAILED: An error occurred.")
        print(f"Error: {e}")
        return []
    finally:
        if driver:
            driver.quit()
            print("Browser closed.")


def corruptedjpgs():
    """
    Scans ALL .jpg, .jpeg, .png, .gif files in:
      - files/jpgs/{author}/
      - files/next jpg/{author}/
      - files/uploaded jpgs/{author}/
      - files/downloaded/{author}/        ← NEW: deletes corrupted ones

    - Moves corrupted files from the first 3 → files/corruptedjpgs/{author}/
    - Deletes corrupted files from 'downloaded' folder (they're temporary)
    - Logs results in corrupted_jpgs.json
    """
    JSON_CONFIG_PATH = r'C:\xampp\htdocs\serenum\pageandgroupauthors.json'

    # ------------------------------------------------------------------ #
    # 1. Load author from config
    # ------------------------------------------------------------------ #
    try:
        with open(JSON_CONFIG_PATH, 'r', encoding='utf-8') as json_file:
            config = json.load(json_file)
        author = config.get('author', '').strip()
        if not author:
            print("Error: 'author' is missing or empty in config.")
            return
    except Exception as e:
        print(f"Failed to load or parse {JSON_CONFIG_PATH}: {e}")
        return

    # ------------------------------------------------------------------ #
    # 2. Define all directories to scan
    # ------------------------------------------------------------------ #
    base_root = r"C:\xampp\htdocs\serenum\files"
    directories_to_check = [
        os.path.join(base_root, "jpgs", author),
        os.path.join(base_root, "next jpg", author),
        os.path.join(base_root, "uploaded jpgs", author),
        os.path.join(base_root, "downloaded", author)  # ← NEW
    ]
    corrupted_dir = os.path.join(base_root, "corruptedjpgs", author)

    # ------------------------------------------------------------------ #
    # 3. Validate input directories
    # ------------------------------------------------------------------ #
    valid_dirs = []
    for dir_path in directories_to_check:
        if os.path.exists(dir_path):
            valid_dirs.append(dir_path)
        else:
            print(f"Directory not found (skipping): {dir_path}")

    if not valid_dirs:
        print("No valid directories found to scan.")
        return

    # Create corrupted directory (for moved files)
    if not os.path.exists(corrupted_dir):
        try:
            os.makedirs(corrupted_dir)
            print(f"Created corrupted directory: {corrupted_dir}")
        except Exception as e:
            print(f"Failed to create corrupted directory {corrupted_dir}: {e}")
            return

    # ------------------------------------------------------------------ #
    # 4. Supported image extensions
    # ------------------------------------------------------------------ #
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')
    moved_files: List[Tuple[str, str, str]] = []  # (filename, source_dir, dest_path)
    deleted_files: List[Tuple[str, str]] = []     # (filename, source_dir)

    print(f"\nScanning {len(valid_dirs)} directories for corrupted images...\n")

    # ------------------------------------------------------------------ #
    # 5. Scan each directory
    # ------------------------------------------------------------------ #
    for directory in valid_dirs:
        is_downloaded_folder = directory.endswith(os.path.join("downloaded", author))
        action = "DELETE" if is_downloaded_folder else "MOVE"

        print(f"Checking ({action}): {directory}")
        try:
            files = os.listdir(directory)
        except Exception as e:
            print(f"Could not read directory {directory}: {e}")
            continue

        image_files = [
            f for f in files
            if f.lower().endswith(IMAGE_EXTENSIONS)
            and os.path.isfile(os.path.join(directory, f))
        ]

        for file in image_files:
            file_path = os.path.join(directory, file)
            is_corrupted = False
            error_msg = ""

            # ------------------- Pillow Double Check -------------------
            try:
                with Image.open(file_path) as img:
                    img.verify()          # Structure check
                with Image.open(file_path) as img:
                    img.load()            # Full decode check
            except Exception as e:
                is_corrupted = True
                error_msg = str(e)

            # ------------------- Handle Corrupted -------------------
            if is_corrupted:
                print(f"  [CORRUPTED] {file} → {error_msg}")

                if is_downloaded_folder:
                    # DELETE from downloaded folder
                    try:
                        os.remove(file_path)
                        print(f"  [DELETED] {file_path}")
                        deleted_files.append((file, directory))
                    except Exception as del_e:
                        print(f"  [FAILED TO DELETE] {file}: {del_e}")
                else:
                    # MOVE to corrupted folder
                    dest_path = os.path.join(corrupted_dir, file)
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(corrupted_dir, f"{base}_{counter}{ext}")
                        counter += 1

                    try:
                        shutil.move(file_path, dest_path)
                        print(f"  [MOVED] → {dest_path}")
                        moved_files.append((file, directory, dest_path))
                    except Exception as move_e:
                        print(f"  [FAILED TO MOVE] {file}: {move_e}")
            else:
                print(f"  [OK] {file}")

    # ------------------------------------------------------------------ #
    # 6. Write summary JSON (NO DATETIME!)
    # ------------------------------------------------------------------ #
    json_path = os.path.join(corrupted_dir, 'corrupted_jpgs.json')
    try:
        summary = {
            "author": author,
            "scanned_directories": valid_dirs,
            "total_moved": len(moved_files),
            "total_deleted": len(deleted_files),
            "moved_files": [
                {
                    "filename": orig,
                    "from_directory": src_dir,
                    "moved_to": dest
                }
                for orig, src_dir, dest in moved_files
            ],
            "deleted_files": [
                {
                    "filename": orig,
                    "from_directory": src_dir
                }
                for orig, src_dir in deleted_files
            ],
            "note": (
                "Corrupted files in 'downloaded' folder are DELETED. "
                "Others are MOVED to corruptedjpgs folder. "
                "All .jpg/.jpeg/.png/.gif checked with Pillow verify() + load()."
            )
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

        total_corrupted = len(moved_files) + len(deleted_files)

        print("\n" + "="*80)
        print(f"SUMMARY: {total_corrupted} corrupted file(s) found and cleaned.")
        print(f"   • Moved: {len(moved_files)} → {corrupted_dir}")
        print(f"   • Deleted: {len(deleted_files)} (from downloaded folder)")
        print(f"Log saved: {json_path}")
        print("="*80)

        if moved_files:
            print("\nMoved corrupted files (first 10):")
            for orig, _, dest in moved_files[:10]:
                print(f"   {orig} → {os.path.basename(dest)}")
            if len(moved_files) > 10:
                print(f"   ... and {len(moved_files) - 10} more.")

        if deleted_files:
            print("\nDeleted corrupted files from downloaded (first 10):")
            for orig, _ in deleted_files[:10]:
                print(f"   {orig}")
            if len(deleted_files) > 10:
                print(f"   ... and {len(deleted_files) - 10} more.")

        if total_corrupted == 0:
            print("\nNo corrupted files found. All images are valid!")

    except Exception as e:
        print(f"Failed to write summary JSON: {e}")

def crop_and_moveto_jpgs():
    """
    Moves images from 'downloaded' to 'jpgfolders'.
    If borders detected → crop them + fixed 10/40px top/bottom.
    If no borders → move as-is.
    Always MOVES (not copies) to save space.
    Detailed logs.
    """
    # === CONFIGURATION ===
    json_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    base_dir = r"C:\xampp\htdocs\serenum\files"
    threshold = 40
    crop_top = 10
    crop_bottom = 40
    # =====================

    import os
    import json
    import numpy as np
    from PIL import Image
    import shutil

    def process_image(src_path, dst_path, threshold):
        try:
            print(f"[OPEN] Loading: {os.path.basename(src_path)}")
            img = Image.open(src_path).convert("RGB")
            img_array = np.array(img)
            h, w = img_array.shape[:2]
            print(f"[INFO] Original size: {w}x{h}")

            gray = np.mean(img_array, axis=2)
            mask = (gray > threshold) & (gray < (255 - threshold))
            coords = np.argwhere(mask)

            # Case 1: No content at all
            if coords.size == 0:
                print(f"[CHECK] No content (all near black/white). Moving as-is.")
                shutil.move(src_path, dst_path)
                print(f"[MOVED] As-is → {os.path.basename(dst_path)}")
                return True, "no_content"

            y0, x0 = coords.min(axis=0)
            y1, x1 = coords.max(axis=0)

            # Case 2: Content fills entire image → no border
            if x0 == 0 and y0 == 0 and x1 == w - 1 and y1 == h - 1:
                print(f"[CHECK] No borders detected. Moving as-is.")
                shutil.move(src_path, dst_path)
                print(f"[MOVED] As-is → {os.path.basename(dst_path)}")
                return True, "no_border"

            # === BORDERS DETECTED ===
            removed = {'L': x0, 'T': y0, 'R': w - 1 - x1, 'B': h - 1 - y1}
            content_w = x1 - x0 + 1
            content_h = y1 - y0 + 1
            print(f"[BORDER] Removed: L={removed['L']}, T={removed['T']}, R={removed['R']}, B={removed['B']}")
            print(f"[BORDER] Content: {content_w}x{content_h}")

            cropped = img.crop((x0, y0, x1 + 1, y1 + 1))

            # Apply fixed crop only if enough height
            if content_h <= crop_top + crop_bottom:
                print(f"[WARN] Too small for fixed crop. Saving border-cropped only.")
                cropped.save(dst_path, quality=95)
                os.remove(src_path)  # delete original
                print(f"[SAVED] Border-only → {os.path.basename(dst_path)}")
                return True, "border_only"

            new_top = crop_top
            new_bottom = content_h - crop_bottom
            if new_bottom <= new_top:
                print(f"[WARN] Fixed crop would remove all. Saving border-cropped only.")
                cropped.save(dst_path, quality=95)
                os.remove(src_path)
                print(f"[SAVED] Border-only → {os.path.basename(dst_path)}")
                return True, "border_only"

            final_cropped = cropped.crop((0, new_top, content_w, new_bottom))
            final_h = new_bottom - new_top
            print(f"[FIXED] Cropped: {crop_top}px top, {crop_bottom}px bottom → {final_h}px tall")
            final_cropped.save(dst_path, quality=95)
            os.remove(src_path)
            print(f"[SAVED] Fully cropped → {os.path.basename(dst_path)}")
            return True, "full_crop"

        except Exception as e:
            print(f"[ERROR] Failed: {e}")
            return False, "error"

    # === MAIN ===
    if not os.path.exists(json_path):
        print(f"JSON not found: {json_path}")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"JSON error: {e}")
        return

    author = data.get("author", "").strip()
    if not author:
        print("Missing 'author' in JSON")
        return

    source_dir = os.path.join(base_dir, "downloaded", author)
    output_dir = os.path.join(base_dir, "jpgfolders", author)

    if not os.path.exists(source_dir):
        print(f"Source dir not found: {source_dir}")
        return

    os.makedirs(output_dir, exist_ok=True)

    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(image_extensions)]
    image_files.sort()

    if not image_files:
        print(f"No images in {source_dir}")
        return

    print(f"Found {len(image_files)} image(s) in {source_dir}\n")

    stats = {k: 0 for k in ["total", "saved", "no_border", "border_only", "full_crop", "no_content", "error"]}
    stats["total"] = len(image_files)

    for img_file in image_files:
        src_path = os.path.join(source_dir, img_file)
        dst_path = os.path.join(output_dir, img_file)

        print(f"\n{'='*60}")
        print(f"PROCESSING: {img_file}")
        print(f"{'='*60}")

        success, action = process_image(src_path, dst_path, threshold)
        if success:
            stats["saved"] += 1
            stats[action] += 1
        else:
            stats["error"] += 1
            print(f"[FAILED] Keeping original due to error.")

    # === FINAL SUMMARY ===
    print(f"\n{'='*60}")
    print(f"FINAL SUMMARY - Author: {author}")
    print(f"{'='*60}")
    print(f"Total images: {stats['total']}")
    print(f"Successfully processed: {stats['saved']}")
    if stats['saved'] > 0:
        print(f"  • Moved as-is (no crop):      {stats['no_border']}")
        print(f"  • Border crop only:           {stats['border_only']}")
        print(f"  • Full crop (border + fixed): {stats['full_crop']}")
        print(f"  • No content (all border):    {stats['no_content']}")
    print(f"Errors: {stats['error']}")
    print(f"{'='*60}")

def check_single_url(
    url: str,
    timeout: int = 30,
    temp_dir: str | None = None,
    final_dir: str | None = None,
) -> Tuple[bool, str]:
    """
    Downloads and verifies image integrity using Pillow.
    Returns (is_valid: bool, debug_info: str)
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, stream=True)
        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}"
    except Exception as e:
        return False, f"Request error: {e}"

    if not temp_dir:
        return False, "temp_dir required"

    os.makedirs(temp_dir, exist_ok=True)
    base_name = os.path.basename(url.split("?")[0])
    if not base_name.lower().endswith((".jpg", ".jpeg")):
        base_name += ".jpg"

    temp_path = os.path.join(temp_dir, base_name)
    root, ext = os.path.splitext(base_name)
    counter = 1
    while os.path.exists(temp_path):
        temp_path = os.path.join(temp_dir, f"{root}_{counter}{ext}")
        counter += 1

    try:
        with open(temp_path, "wb") as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)
    except Exception as e:
        return False, f"Save failed: {e}"

    try:
        with Image.open(temp_path) as img:
            img.verify()
        with Image.open(temp_path) as img:
            img.load()
    except Exception as e:
        try:
            os.remove(temp_path)
        except:
            pass
        return False, f"Corrupted: {e}"

    final_path = temp_path
    if final_dir and final_dir != temp_dir:
        os.makedirs(final_dir, exist_ok=True)
        dest_name = os.path.basename(temp_path)
        final_path = os.path.join(final_dir, dest_name)
        root, ext = os.path.splitext(dest_name)
        counter = 1
        while os.path.exists(final_path):
            final_path = os.path.join(final_dir, f"{root}_{counter}{ext}")
            counter += 1
        try:
            shutil.move(temp_path, final_path)
        except Exception as e:
            try:
                os.remove(temp_path)
            except:
                pass
            return False, f"Move failed: {e}"

    return True, f"OK → {os.path.getsize(final_path)} bytes"

def markjpgs():
    """
    Ensures:
      1. jpgfolders has EXACTLY cardamount JPG/PNG files
      2. next_jpgcard.json has EXACTLY cardamount valid URLs
      3. 1:1 perfect match between files and URLs
    If ANY mismatch → DELETE ALL + REDOWNLOAD ALL
    """
    # ------------------------------------------------------------------ #
    # 1. Load config
    # ------------------------------------------------------------------ #
    JSON_CONFIG_PATH = r'C:\xampp\htdocs\serenum\pageandgroupauthors.json'
    FETCHED_JSON_PATH = r'C:\xampp\htdocs\serenum\files\fetchedjpgsurl.json'

    try:
        with open(JSON_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)

        author = config.get('author', '').strip()
        processjpgfrom = config.get('processjpgfrom', 'freshjpgs').strip().lower()
        if not author:
            print("Error: 'author' missing in config.")
            return

        try:
            cardamount = max(1, int(config.get('cardamount', 1)))
        except:
            print("Warning: Invalid cardamount. Using 1.")
            cardamount = 1

        if processjpgfrom not in ['freshjpgs', 'uploadedjpgs']:
            processjpgfrom = 'freshjpgs'

    except Exception as e:
        print(f"Config load failed: {e}")
        return

    # ------------------------------------------------------------------ #
    # 2. Paths
    # ------------------------------------------------------------------ #
    base_path = (
        f"https://jpgsvault.rf.gd/jpgs/{author}_uploaded/"
        if processjpgfrom == 'uploadedjpgs'
        else f"https://jpgsvault.rf.gd/jpgs/{author}/"
    )

    jpgfolders_dir = fr'C:\xampp\htdocs\serenum\files\jpgfolders\{author}'
    next_json_dir = fr'C:\xampp\htdocs\serenum\files\next jpg\{author}'
    next_json_path = os.path.join(next_json_dir, 'next_jpgcard.json')
    download_dir = fr'C:\xampp\htdocs\serenum\files\downloaded\{author}'

    os.makedirs(jpgfolders_dir, exist_ok=True)
    os.makedirs(next_json_dir, exist_ok=True)
    os.makedirs(download_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    # 3. Load fetched URLs
    # ------------------------------------------------------------------ #
    if not os.path.exists(FETCHED_JSON_PATH):
        print(f"fetchedjpgsurl.json not found: {FETCHED_JSON_PATH}")
        return

    try:
        with open(FETCHED_JSON_PATH, 'r', encoding='utf-8') as f:
            all_fetched_urls = set(json.load(f).get("jpg_urls", []))
        print(f"Loaded {len(all_fetched_urls)} URLs from fetched list")
    except Exception as e:
        print(f"Failed to read fetched list: {e}")
        return

    candidate_urls = [
        u for u in all_fetched_urls
        if u.startswith(base_path) and u.lower().endswith(('.jpg', '.jpeg'))
    ]
    print(f"Found {len(candidate_urls)} candidate JPG URLs")

    if len(candidate_urls) < cardamount:
        print(f"Only {len(candidate_urls)} URLs available, but need {cardamount}. Cannot proceed.")
        return

    # ------------------------------------------------------------------ #
    # 4. Load next_jpgcard.json
    # ------------------------------------------------------------------ #
    next_urls = []
    if os.path.exists(next_json_path):
        try:
            with open(next_json_path, 'r', encoding='utf-8') as f:
                next_data = json.load(f)
                next_urls = next_data.get("next_jpgcard", [])
            print(f"Loaded {len(next_urls)} URL(s) from next_jpgcard.json")
        except Exception as e:
            print(f"Corrupted next_jpgcard.json → {e}. Will rebuild.")
            next_urls = []

    # ------------------------------------------------------------------ #
    # 5. Count files in jpgfolders
    # ------------------------------------------------------------------ #
    image_exts = ('.jpg', '.jpeg', '.png')
    existing_files = [
        f for f in os.listdir(jpgfolders_dir)
        if f.lower().endswith(image_exts)
    ]
    file_count = len(existing_files)
    print(f"Found {file_count} image(s) in jpgfolders")

    # ------------------------------------------------------------------ #
    # 6. EXACT MATCH VALIDATION (Files + URLs + 1:1 Mapping)
    # ------------------------------------------------------------------ #
    def get_filename_from_url(url):
        return os.path.basename(url.split("?")[0])

    # Extract filenames from URLs
    url_filenames = {get_filename_from_url(u) for u in next_urls}
    file_names = {f for f in existing_files}

    # Check 1:1 mapping
    files_match_urls = file_names == url_filenames
    url_count_ok = len(next_urls) == cardamount
    file_count_ok = file_count == cardamount

    print(f"\nVALIDATION CHECK:")
    print(f"  • Required count       : {cardamount}")
    print(f"  • Files in folder      : {file_count}")
    print(f"  • URLs in JSON         : {len(next_urls)}")
    print(f"  • 1:1 filename match   : {'YES' if files_match_urls else 'NO'}")

    # ------------------------------------------------------------------ #
    # 7. FINAL DECISION
    # ------------------------------------------------------------------ #
    if file_count_ok and url_count_ok and files_match_urls:
        print(f"\nPERFECT MATCH: {cardamount} files + {cardamount} URLs + 1:1 mapping")
        print("SKIPPING DOWNLOAD – All data is valid and complete.")
        return
    else:
        mismatch_reasons = []
        if not file_count_ok:
            mismatch_reasons.append(f"File count ({file_count} ≠ {cardamount})")
        if not url_count_ok:
            mismatch_reasons.append(f"URL count ({len(next_urls)} ≠ {cardamount})")
        if not files_match_urls:
            mismatch_reasons.append("Filename mismatch between files and URLs")

        print(f"\nMISMATCH DETECTED:")
        for r in mismatch_reasons:
            print(f"  → {r}")

        print("DELETING ALL files, downloaded images, and JSON records...")
        
        # Delete all in jpgfolders
        for f in existing_files:
            try:
                os.remove(os.path.join(jpgfolders_dir, f))
                print(f"  [DELETED] {f}")
            except:
                pass

        # Delete all in downloaded
        for f in os.listdir(download_dir):
            try:
                path = os.path.join(download_dir, f)
                if os.path.isfile(path):
                    os.remove(path)
            except:
                pass

        # Reset next_jpgcard.json
        with open(next_json_path, 'w', encoding='utf-8') as f:
            json.dump({"next_jpgcard": []}, f, indent=4, ensure_ascii=False)
        print(f"  [RESET] next_jpgcard.json")

        print(f"\nREDOWNLOADING EXACTLY {cardamount} VALID IMAGES...\n")

    # ------------------------------------------------------------------ #
    # 8. Download exactly cardamount valid images
    # ------------------------------------------------------------------ #
    downloaded = 0
    valid_urls = []

    for url in candidate_urls:
        if downloaded >= cardamount:
            break

        print(f"[{downloaded + 1}/{cardamount}] Downloading: {url}")
        is_valid, debug = check_single_url(
            url,
            temp_dir=download_dir,
            final_dir=download_dir
        )

        if is_valid:
            valid_urls.append(url)
            downloaded += 1
            print(f"  [SUCCESS] {debug}")
        else:
            print(f"  [FAILED] {debug}")

    if downloaded != cardamount:
        print(f"\nFAILED: Only {downloaded}/{cardamount} images downloaded successfully.")
        return

    # ------------------------------------------------------------------ #
    # 9. Save next_jpgcard.json
    # ------------------------------------------------------------------ #
    try:
        with open(next_json_path, 'w', encoding='utf-8') as f:
            json.dump({"next_jpgcard": valid_urls}, f, indent=4, ensure_ascii=False)
        print(f"\nSUCCESS: Saved {len(valid_urls)} valid URLs to next_jpgcard.json")
    except Exception as e:
        print(f"Failed to save JSON: {e}")

    # ------------------------------------------------------------------ #
    # 10. Final Status
    # ------------------------------------------------------------------ #
    print("\n" + "="*80)
    print("FINAL STATUS – PERFECT SYNC ENFORCED")
    print("="*80)
    print(f"Author       : {author}")
    print(f"Required     : {cardamount}")
    print(f"Downloaded   : {downloaded}")
    print(f"jpgfolders   : {jpgfolders_dir}")
    print(f"Download Dir : {download_dir}")
    print(f"JSON Path    : {next_json_path}")
    print(f"Ready for    : crop_and_moveto_jpgs()")
    print("="*80)
    print("All files and records are in perfect 1:1 sync.")
    print("="*80)


def orderjpgs():
    # Load configuration from JSON
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        processjpgfrom = config.get('processjpgfrom', 'freshjpgs')  # Default to 'freshjpgs'
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

    # === HANDLE uploadedjpgs LOGIC ===
    if processjpgfrom == 'uploadedjpgs':
        base_uploaded_path = f"C:\\xampp\\htdocs\\serenum\\files\\uploaded jpgs\\{author}"
        if not os.path.exists(base_uploaded_path):
            print(f"Base uploaded jpgs directory does not exist: {base_uploaded_path}")
            processjpgfrom = 'freshjpgs'
            directory = freshjpgs_directory
        else:
            date_folders = []
            for f in os.listdir(base_uploaded_path):
                folder_path = os.path.join(base_uploaded_path, f)
                if os.path.isdir(folder_path):
                    try:
                        datetime.strptime(f, "%d-%B-%Y")
                        date_folders.append(f)
                    except ValueError:
                        print(f"Skipping invalid date folder: {f}")

            if not date_folders:
                # No valid date folders → check root for files
                base_files = [f for f in os.listdir(base_uploaded_path) if f.lower().endswith(tuple(image_extensions))]
                if base_files:
                    today_folder = datetime.now().strftime("%d-%B-%Y")
                    today_path = os.path.join(base_uploaded_path, today_folder)
                    os.makedirs(today_path, exist_ok=True)
                    for file in base_files:
                        src = os.path.join(base_uploaded_path, file)
                        dst = os.path.join(today_path, file)
                        shutil.move(src, dst)
                        print(f"Moved {file} → {today_folder}/")
                    date_folders.append(today_folder)
                else:
                    print(f"No images in base uploaded folder. Falling back to freshjpgs.")
                    processjpgfrom = 'freshjpgs'
                    directory = freshjpgs_directory
            else:
                # Sort date folders: oldest first
                date_folders.sort(key=lambda x: datetime.strptime(x, "%d-%B-%Y"))

                # Look for first folder with >20 images
                for date_folder in date_folders:
                    dir_path = os.path.join(base_uploaded_path, date_folder)
                    img_files = [f for f in os.listdir(dir_path) if f.lower().endswith(tuple(image_extensions))]
                    if len(img_files) > 20:
                        directory = dir_path
                        print(f"Selected directory with {len(img_files)} images: {directory}")
                        break

                # If none >20, consolidate into oldest folder
                if not directory:
                    oldest_folder = date_folders[0]
                    oldest_path = os.path.join(base_uploaded_path, oldest_folder)
                    os.makedirs(oldest_path, exist_ok=True)

                    # Move all root-level images into oldest folder
                    root_files = [f for f in os.listdir(base_uploaded_path) if f.lower().endswith(tuple(image_extensions))]
                    for file in root_files:
                        src = os.path.join(base_uploaded_path, file)
                        dst = os.path.join(oldest_path, file)
                        shutil.move(src, dst)
                        print(f"Moved {file} → {oldest_folder}/")

                    # Re-check count
                    final_files = [f for f in os.listdir(oldest_path) if f.lower().endswith(tuple(image_extensions))]
                    if len(final_files) > 20:
                        directory = oldest_path
                        print(f"Consolidated into {oldest_folder} with {len(final_files)} images.")
                    else:
                        print(f"Even after consolidation, <=20 images. Falling back to freshjpgs.")
                        processjpgfrom = 'freshjpgs'
                        directory = freshjpgs_directory

    # === FALLBACK TO freshjpgs ===
    if processjpgfrom == 'freshjpgs':
        directory = freshjpgs_directory
        if not directory.endswith(author):
            print(f"Error: input directory ({directory}) does not end with author folder '{author}'")
            return

    # Final directory validation
    if not directory or not os.path.exists(directory):
        print(f"Invalid or missing directory: {directory}")
        return

    image_files = [f for f in os.listdir(directory) if f.lower().endswith(tuple(image_extensions))]
    if not image_files:
        print(f"No image files found in {directory}")
        return

    # === STEP 1: Parse existing card_N.jpg numbers ===
    existing_numbers = []
    for file in image_files:
        match = re.match(r'card_(\d+)\.jpg$', file, re.IGNORECASE)
        if match:
            existing_numbers.append(int(match.group(1)))

    highest_num = max(existing_numbers) if existing_numbers else 0
    existing_numbers.sort()

    # Find isolated low numbers (before first big gap)
    isolated_numbers = []
    for i in range(len(existing_numbers) - 1):
        if existing_numbers[i + 1] - existing_numbers[i] > 1:
            isolated_numbers = existing_numbers[:i + 1]
            break
    else:
        # No gap found → all are sequential from 1
        if existing_numbers and existing_numbers[0] == 1:
            isolated_numbers = []

    next_num = highest_num + 1
    all_card_numbers = [n for n in existing_numbers if n not in isolated_numbers]

    # === STEP 2: Move isolated low cards to the end ===
    for num in sorted(isolated_numbers):
        old_name = f'card_{num}.jpg'
        new_name = f'card_{next_num}.jpg'
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)

        while os.path.exists(new_path):
            next_num += 1
            new_name = f'card_{next_num}.jpg'
            new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed {old_name} → {new_name}")
        all_card_numbers.append(next_num)
        next_num += 1

    # === STEP 3: Rename unnumbered .jpg files ===
    non_card_jpgs = [
        f for f in image_files
        if f.lower().endswith('.jpg') and not re.match(r'card_\d+\.jpg$', f, re.IGNORECASE)
    ]
    non_card_jpgs.sort()

    for file in non_card_jpgs:
        old_path = os.path.join(directory, file)
        new_name = f'card_{next_num}.jpg'
        new_path = os.path.join(directory, new_name)

        while os.path.exists(new_path):
            next_num += 1
            new_name = f'card_{next_num}.jpg'
            new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed {file} → {new_name}")
        all_card_numbers.append(next_num)
        next_num += 1

    # === STEP 4: Convert & rename non-JPG images ===
    non_jpg_images = [
        f for f in image_files
        if f.lower().endswith(tuple(image_extensions - {'.jpg'}))
    ]
    non_jpg_images.sort()

    for file in non_jpg_images:
        old_path = os.path.join(directory, file)
        new_name = f'card_{next_num}.jpg'
        new_path = os.path.join(directory, new_name)

        while os.path.exists(new_path):
            next_num += 1
            new_name = f'card_{next_num}.jpg'
            new_path = os.path.join(directory, new_name)

        try:
            with Image.open(old_path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                img.save(new_path, 'JPEG', quality=95)
            os.remove(old_path)
            print(f"Converted {file} → {new_name}")
            all_card_numbers.append(next_num)
            next_num += 1
        except Exception as e:
            print(f"Failed to convert {file}: {e}")

    # === STEP 5: ALWAYS REPLACE card_x.jpg & next_jpgcard.json ===
    if all_card_numbers:
        lowest_num = min(all_card_numbers)
        lowest_card = f'card_{lowest_num}.jpg'
        src_path = os.path.join(directory, lowest_card)
        dst_path = os.path.join(output_dir, 'card_x.jpg')
        json_path = os.path.join(output_dir, 'next_jpgcard.json')

        # Always overwrite card_x.jpg
        try:
            if os.path.exists(dst_path):
                os.remove(dst_path)
                print(f"Removed existing card_x.jpg")
            shutil.copy2(src_path, dst_path)
            print(f"Replaced → card_x.jpg (from {lowest_card})")
        except Exception as e:
            print(f"Failed to replace card_x.jpg: {e}")
            return

        # Always write JSON with current timestamp
        try:
            timestamp = datetime.now(pytz.timezone('Africa/Lagos')).isoformat()
            with open(json_path, 'w') as f:
                json.dump({
                    'next_jpgcard': lowest_card,
                    'changed_to': 'card_x.jpg',
                    'timestamp': timestamp
                }, f, indent=4)
            print(f"Updated next_jpgcard.json → {lowest_card} @ {timestamp}")
        except Exception as e:
            print(f"Failed to write JSON: {e}")
    else:
        print("No card images processed. Nothing to output.")



def update_calendar():
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
    group_types = pageauthors['group_types']
    print(f"Author: {author}, Type: {type_value}, Group Types: {group_types}")
    
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
                                            "minutes_DISTANCE": int((
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
    
    # Define output path with author, group_types, and type
    output_path = f"C:\\xampp\\htdocs\\serenum\\files\\next jpg\\{author}\\jsons\\{group_types}\\{type_value}calendar.json"
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
    """Move next → last (OVERWRITE), generate NEW next_schedule starting AFTER schedule_date."""
    import os
    import json
    from datetime import datetime, timedelta

    # --------------------------------------------------------------------- #
    # 1. Load config
    # --------------------------------------------------------------------- #
    pageauthors_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    try:
        with open(pageauthors_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    except Exception as e:
        print(f"Config error: {e}")
        return

    author        = cfg['author']
    type_value    = cfg['type']
    group_types   = cfg['group_types']
    cardamount    = int(cfg.get('cardamount', 1))
    schedule_date_str = cfg.get('schedule_date', '').strip()

    print(f"Config loaded: author={author}, type={type_value}, cardamount={cardamount}, schedule_date='{schedule_date_str}'")

    # --------------------------------------------------------------------- #
    # 2. Parse schedule_date (must be valid)
    # --------------------------------------------------------------------- #
    base_datetime = None
    if schedule_date_str:
        for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y"):
            try:
                dt = datetime.strptime(schedule_date_str.split('.')[0], fmt)  # ignore milliseconds
                if ' ' not in schedule_date_str:
                    dt = dt.replace(hour=0, minute=0)
                base_datetime = dt
                print(f"Using schedule_date: {base_datetime.strftime('%d/%m/%Y %H:%M')}")
                break
            except ValueError:
                continue

    if base_datetime is None:
        base_datetime = datetime.now()
        print(f"Invalid schedule_date. Falling back to now: {base_datetime.strftime('%d/%m/%Y %H:%M')}")

    # --------------------------------------------------------------------- #
    # 3. Load timeorders
    # --------------------------------------------------------------------- #
    timeorders_path = r"C:\xampp\htdocs\serenum\timeorders.json"
    try:
        with open(timeorders_path, 'r', encoding='utf-8') as f:
            timeorders_data = json.load(f)
    except Exception as e:
        print(f"Timeorders error: {e}")
        return

    if type_value not in timeorders_data:
        print(f"Type '{type_value}' not in timeorders.json")
        return

    timeorders = sorted(timeorders_data[type_value], key=lambda x: x["24hours"])
    valid_times_24 = [t["24hours"] for t in timeorders]
    time_map = {t["24hours"]: t["12hours"] for t in timeorders}

    print(f"Valid time slots for '{type_value}': {', '.join(valid_times_24)}")

    # --------------------------------------------------------------------- #
    # 4. Paths
    # --------------------------------------------------------------------- #
    base_dir = f"C:\\xampp\\htdocs\\serenum\\files\\next jpg\\{author}\\jsons\\{group_types}"
    schedules_path = os.path.join(base_dir, f"{type_value}schedules.json")

    # --------------------------------------------------------------------- #
    # 5. Load existing schedules
    # --------------------------------------------------------------------- #
    old_last_schedule = []
    old_next_schedule = []
    if os.path.exists(schedules_path):
        try:
            with open(schedules_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            old_last_schedule = data.get("last_schedule", [])
            old_next_schedule = data.get("next_schedule", [])
            print(f"Loaded: {len(old_last_schedule)} last, {len(old_next_schedule)} next")
        except Exception as e:
            print(f"Error reading schedules.json: {e}")

    # --------------------------------------------------------------------- #
    # 6. STEP 1: Overwrite last_schedule with old_next_schedule
    # --------------------------------------------------------------------- #
    new_last_schedule = []
    for item in old_next_schedule:
        if isinstance(item, dict):
            new_last_schedule.append(item)
        elif isinstance(item, str):
            # Legacy migration
            if '_' not in item:
                continue
            day, time_part = item.split('_', 1)
            time_24 = f"{time_part[:2]}:{time_part[2:]}"
            time_12 = time_map.get(time_24, "12:00 AM")
            migrated = {
                "id": item,
                "date": f"{day.zfill(2)}/{base_datetime.strftime('%m/%Y')}",
                "time_12hour": time_12,
                "time_24hour": time_24
            }
            new_last_schedule.append(migrated)
            print(f"Migrated legacy: {item} → {migrated}")
        else:
            print(f"Skipping invalid schedule item: {item}")

    print(f"last_schedule updated with {len(new_last_schedule)} slot(s)")

    # --------------------------------------------------------------------- #
    # 7. Build used_ids from new_last_schedule
    # --------------------------------------------------------------------- #
    used_ids = {slot.get("id") for slot in new_last_schedule if isinstance(slot, dict)}

    # --------------------------------------------------------------------- #
    # 8. Generate next_schedule: start AFTER base_datetime
    # --------------------------------------------------------------------- #
    next_schedule_list = []
    current_search = base_datetime
    max_days_ahead = 60  # safety
    days_searched = 0

    while len(next_schedule_list) < cardamount and days_searched < max_days_ahead:
        day_searched = current_search.date()
        day_str = day_searched.strftime("%d/%m/%Y")

        for t in timeorders:
            if len(next_schedule_list) >= cardamount:
                break

            slot_time_24 = t["24hours"]
            try:
                slot_datetime = datetime.combine(day_searched, datetime.strptime(slot_time_24, "%H:%M").time())
            except:
                continue

            # Must be AFTER base_datetime
            if slot_datetime <= base_datetime:
                continue

            # Today: apply 50-minute buffer
            if day_searched == base_datetime.date():
                minutes_diff = (slot_datetime - base_datetime).total_seconds() / 60
                if minutes_diff < 50:
                    continue
            # Future days: allow immediate slot (e.g., 00:05)

            slot_id = f"{day_searched.day:02d}_{slot_time_24.replace(':', '')}"

            if slot_id in used_ids:
                continue

            new_slot = {
                "id": slot_id,
                "date": day_str,
                "time_12hour": t["12hours"],
                "time_24hour": slot_time_24
            }
            next_schedule_list.append(new_slot)
            used_ids.add(slot_id)
            print(f"Added to next: {day_str} {slot_time_24} ({slot_id})")

        # Move to next day
        current_search += timedelta(days=1)
        days_searched += 1

    if not next_schedule_list:
        print("No available slots found after schedule_date.")
        return

    # --------------------------------------------------------------------- #
    # 9. Write schedules.json
    # --------------------------------------------------------------------- #
    output_data = {
        "last_schedule": new_last_schedule,
        "next_schedule": next_schedule_list
    }
    os.makedirs(os.path.dirname(schedules_path), exist_ok=True)
    with open(schedules_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"Schedules written to {schedules_path}")

    # --------------------------------------------------------------------- #
    # 10. Update schedule_date to LAST slot in next_schedule
    # --------------------------------------------------------------------- #
    if next_schedule_list:
        last_slot = next_schedule_list[-1]
        try:
            new_schedule_date = datetime.strptime(
                f"{last_slot['date']} {last_slot['time_24hour']}",
                "%d/%m/%Y %H:%M"
            )
            cfg["schedule_date"] = new_schedule_date.strftime("%d/%m/%Y %H:%M")
            with open(pageauthors_path, 'w', encoding='utf-8') as f:
                json.dump(cfg, f, indent=4, ensure_ascii=False)
            print(f"schedule_date updated to: {cfg['schedule_date']}")
        except Exception as e:
            print(f"Failed to update schedule_date: {e}")

    print(f"SUCCESS: {len(next_schedule_list)} new slot(s) scheduled.")
    print(f"         last_schedule: {len(new_last_schedule)} slot(s)")

    # --------------------------------------------------------------------- #
    # 11. Optional: randomize minutes
    # --------------------------------------------------------------------- #
    try:
        randomize_next_schedule_minutes()
    except NameError:
        pass

def randomize_next_schedule_minutes():
    """
    Randomize minutes (01–30) for EACH slot in next_schedule using its OWN hour.
    Preserves original hour, only changes minutes.
    """

    # === Load config ===
    pageauthors_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    try:
        with open(pageauthors_path, 'r', encoding='utf-8') as f:
            pageauthors = json.load(f)
    except Exception as e:
        print(f"[randomize] Config error: {e}")
        return

    author = pageauthors.get('author')
    type_value = pageauthors.get('type')
    group_types = pageauthors.get('group_types', '')

    if not author or not type_value:
        print("[randomize] Missing author or type in config")
        return

    # === Build path ===
    schedules_path = f"C:\\xampp\\htdocs\\serenum\\files\\next jpg\\{author}\\jsons\\{group_types}\\{type_value}schedules.json"

    if not os.path.exists(schedules_path):
        print(f"[randomize] schedules.json not found: {schedules_path}")
        return

    # === Read schedule ===
    try:
        with open(schedules_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[randomize] Error reading JSON: {e}")
        return

    if 'next_schedule' not in data or not data['next_schedule']:
        print("[randomize] No next_schedule to randomize.")
        return

    schedule_list = data['next_schedule']
    if isinstance(schedule_list, dict):
        schedule_list = [schedule_list]

    updated_slots = []
    for slot in schedule_list:
        try:
            old_time = slot.get('time_24hour')
            if not old_time or ':' not in old_time:
                print(f"[randomize] Invalid time_24hour in slot: {slot}")
                continue

            hour = int(old_time.split(':')[0])
            new_min = random.randint(1, 30)  # 01 to 30
            new_time_24 = f"{hour:02d}:{new_min:02d}"

            # Format 12-hour time
            dt = datetime.strptime(new_time_24, "%H:%M")
            new_time_12 = dt.strftime("%I:%M %p").lstrip("0").lower()
            new_time_12 = new_time_12.replace(" 0", " ").replace("am", "AM").replace("pm", "PM")
            if new_time_12.startswith("0"):
                new_time_12 = new_time_12[1:]

            # Update slot
            slot["time_24hour"] = new_time_24
            slot["time_12hour"] = new_time_12
            updated_slots.append(f"{slot['date']} {new_time_24}")

        except Exception as e:
            print(f"[randomize] Failed to process slot {slot}: {e}")
            continue

    # === Write back ===
    try:
        with open(schedules_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"[randomize] Successfully randomized {len(updated_slots)} slots (minutes 01–30):")
        for s in sorted(updated_slots):
            print(f"  → {s}")
    except Exception as e:
        print(f"[randomize] Failed to save file: {e}")
def check_schedule_time():
    """Check if the next schedule in schedules.json is behind the current time."""
    # Get current date and time
    now = datetime.now()
    current_time_24hour = now.strftime("%H:%M")
    current_date = now.strftime("%d/%m/%Y")
    current_datetime = datetime.strptime(f"{current_date} {current_time_24hour}", "%d/%m/%Y %H:%M")
    
    print(f"Current date and time: {current_date} {current_time_24hour}")
    
    # Read pageandgroupauthors.json to get author, type, and group_types
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
    group_types = pageauthors['group_types']
    print(f"Author: {author}, Type: {type_value}, Group Types: {group_types}")
    
    # Read schedules.json based on new path structure
    schedules_path = f"C:\\xampp\\htdocs\\serenum\\files\\next jpg\\{author}\\jsons\\{group_types}\\{type_value}schedules.json"
    print(f"Reading schedules.json from {schedules_path}")
    if not os.path.exists(schedules_path):
        print(f"Error: schedules.json not found at {schedules_path}")
        update_calendar()
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
        update_calendar()
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

def sync_last_schedule_between_groups():
    """
    PURE DATA COPY ONLY.
    - If group_types == 'uk' → copy others → uk (last_schedule only)
    - If group_types == 'others' → copy uk → others (last_schedule only)
    Overwrites destination file. No other actions.
    """
    import os
    import json

    # 1. Read config
    config_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    except:
        return  # Silent fail — pure copy, no noise

    author = cfg.get('author')
    group_types = cfg.get('group_types', '').strip().lower()
    if group_types not in ['uk', 'others']:
        return

    # 2. Determine source and dest
    source_group = 'others' if group_types == 'uk' else 'uk'
    dest_group = group_types

    base_dir = f"C:\\xampp\\htdocs\\serenum\\files\\next jpg\\{author}\\jsons"

    # 3. Get all type names
    timeorders_path = r"C:\xampp\htdocs\serenum\timeorders.json"
    try:
        with open(timeorders_path, 'r', encoding='utf-8') as f:
            types = list(json.load(f).keys())
    except:
        return

    # 4. Copy last_schedule for each type
    for t in types:
        src_file = os.path.join(base_dir, source_group, f"{t}schedules.json")
        dst_file = os.path.join(base_dir, dest_group, f"{t}schedules.json")

        if not os.path.exists(src_file):
            continue

        try:
            with open(src_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            last_schedule = data.get("last_schedule", [])

            # Write only last_schedule (preserve next_schedule if exists, else empty)
            output = {
                "last_schedule": last_schedule,
                "next_schedule": data.get("next_schedule", [])
            }

            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            with open(dst_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
        except:
            pass  # Silent — pure copy
        

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
            toggle_group_types()
            print("Updated tracker: groups_selected set to True, failed_attempts reset to 0")
            return True

        except Exception as e:
            print(f"Failed to locate popup window or process groups: {str(e)}")
            return False
    else:
        print(f"Invalid group config: '{group_config}'. Defaulting to no group selection.")
        return False

def toggle_group_types():
    """
    Toggle the 'group_types' field in the JSON config between 'uk' and 'others'.
    If current value is 'uk' → rewrite to 'others'
    If current value is 'others' → rewrite to 'uk'
    If missing or invalid → default to 'others'
    """
    if not os.path.exists(JSON_CONFIG_PATH):
        print(f"Config file {JSON_CONFIG_PATH} does not exist. Creating with default 'group_types': 'others'.")
        config_data = {"group_types": "others"}
        os.makedirs(os.path.dirname(JSON_CONFIG_PATH), exist_ok=True)
        with open(JSON_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        print("Created config with group_types = 'others'")
        return True

    try:
        with open(JSON_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"Error reading config {JSON_CONFIG_PATH}: {str(e)}. Initializing with defaults.")
        config_data = {}

    current_type = config_data.get('group_types', 'others').strip().lower()
    
    new_type = 'uk' if current_type == 'others' else 'others'
    
    config_data['group_types'] = new_type

    try:
        with open(JSON_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        print(f"Successfully toggled group_types: '{current_type}' → '{new_type}'")
        sync_last_schedule_between_groups()
        return True
    except Exception as e:
        print(f"Failed to write to config {JSON_CONFIG_PATH}: {str(e)}")
        return False



def toggleaddphoto():
    """
    OCR-based 'Add photo/video' button click.
    • 0–2 random mouse movements (never the same region twice).
    • Infinite variety – no hard-coded paths.
    • Creates / updates laststate.json safely.
    """
    # ---- STATE TRACKER ----
    if getattr(toggleaddphoto, 'is_toggled', False):
        print("'Add photo/video' button already toggled. Skipping.")
        return

    print("Searching for 'Add photo' or 'Add photo/video' text content")
    try:
        retry_count = 0
        max_retries = 3
        save_path = r"C:\xampp\htdocs\serenum\files\gui"
        laststate_path = r"C:\xampp\htdocs\serenum\laststate.json"

        # --- LOAD OR CREATE laststate.json ---
        full_state = {}
        if os.path.exists(laststate_path):
            try:
                with open(laststate_path, 'r') as f:
                    full_state = json.load(f)
                print("Loaded laststate.json")
            except Exception as e:
                print(f"Error reading laststate.json: {e}. Starting fresh.")
                full_state = {}
        else:
            print(f"laststate.json not found – will create at: {laststate_path}")

        last_region = full_state.get("toggleaddphoto_last_region")
        print(f"Last visited region: {last_region}")

        while retry_count < max_retries:
            # ---- 1. Capture screenshot ----
            screenshot = ImageGrab.grab()
            screenshot_cv = cv2.cvtColor(np.array(screenshot, dtype=np.uint8), cv2.COLOR_RGB2BGR)

            # Save for debugging
            os.makedirs(save_path, exist_ok=True)
            screenshot_file = os.path.join(save_path, "windowstext.png")
            cv2.imwrite(screenshot_file, screenshot_cv)
            print(f"Screenshot captured: '{screenshot_file}'")

            # ---- 2. Pre-process image for OCR ----
            gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            resized = cv2.resize(blur, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            thresh = cv2.adaptiveThreshold(
                resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )

            # ---- 3. OCR ----
            data = pytesseract.image_to_data(
                thresh, output_type=pytesseract.Output.DICT, config='--psm 3'
            )
            text_lower = [t.lower().strip() for t in data["text"]]

            # ---- 4. Locate target phrase ----
            texts_index = None
            detected_phrase = None

            # Case A: "add" followed by "photo" or "photo/video"
            for i, txt in enumerate(text_lower):
                if txt == "add":
                    nxt = text_lower[i + 1] if i + 1 < len(text_lower) else ""
                    if nxt in ("photo", "photo/video"):
                        texts_index = i
                        detected_phrase = f"add {nxt}"
                        break

            # Case B: single word "addphoto"
            if texts_index is None:
                for i, txt in enumerate(text_lower):
                    if txt == "addphoto":
                        texts_index = i
                        detected_phrase = "addphoto"
                        break

            # ---- 5. If found → click ----
            if texts_index is not None and "addvideo" not in detected_phrase:
                # Convert OCR coordinates back to original resolution
                x = data["left"][texts_index] // 1.5
                y = data["top"][texts_index] // 1.5
                w = data["width"][texts_index] // 1.5
                h = data["height"][texts_index] // 1.5
                center_x = x + w // 2
                center_y = y + h // 2

                print(f"Detected: {detected_phrase} at ({center_x}, {center_y})")

                # ---- Human-like mouse path ----
                screen_w, screen_h = pyautogui.size()

                # 9 dynamic region centers (top-left → bottom-right)
                region_centers = [
                    (screen_w * 0.2, screen_h * 0.2),
                    (screen_w * 0.5, screen_h * 0.2),
                    (screen_w * 0.8, screen_h * 0.2),
                    (screen_w * 0.2, screen_h * 0.5),
                    (screen_w * 0.5, screen_h * 0.5),
                    (screen_w * 0.8, screen_h * 0.5),
                    (screen_w * 0.2, screen_h * 0.8),
                    (screen_w * 0.5, screen_h * 0.8),
                    (screen_w * 0.8, screen_h * 0.8),
                ]

                # **0, 1 or 2** random intermediate moves
                num_moves = random.randint(0, 2)
                print(f"Performing {num_moves} random movement(s)...")

                used_regions = []
                if isinstance(last_region, (list, tuple)) and len(last_region) == 2:
                    used_regions.append(tuple(last_region))

                current_region = None
                for _ in range(num_moves):
                    available = [r for r in region_centers if r not in used_regions]
                    if not available:          # fallback if we somehow exhausted all
                        available = region_centers
                    region = random.choice(available)
                    used_regions.append(region)
                    current_region = region

                    # Random offset inside a ±150 px box
                    off_x = random.randint(-150, 150)
                    off_y = random.randint(-150, 150)
                    rand_x = max(50, min(region[0] + off_x, screen_w - 50))
                    rand_y = max(50, min(region[1] + off_y, screen_h - 50))

                    duration = random.uniform(0.3, 0.9)
                    print(f"  → Moving to region near ({rand_x}, {rand_y})")
                    pyautogui.moveTo(rand_x, rand_y, duration=duration,
                                     tween=pyautogui.easeInOutQuad)
                    time.sleep(random.uniform(0.1, 0.4))

                # ---- Final slow move to the button ----
                print(f"Slowly moving to target ({center_x}, {center_y})...")
                pyautogui.moveTo(center_x, center_y,
                                 duration=random.uniform(1.2, 2.1),
                                 tween=pyautogui.easeInOutQuad)

                # Tiny final jitter inside the button bounds
                jitter_x = random.randint(-w // 4, w // 4)
                jitter_y = random.randint(-h // 4, h // 4)
                final_x = max(0, min(center_x + jitter_x, screen_w))
                final_y = max(0, min(center_y + jitter_y, screen_h))

                print(f"Final click at: ({final_x}, {final_y})")
                pyautogui.moveTo(final_x, final_y, duration=0.2)
                time.sleep(0.2)
                pyautogui.click()
                print("Clicked 'Add photo/video'")

                # ---- Mark as toggled & persist last region ----
                toggleaddphoto.is_toggled = True

                if current_region:
                    full_state["toggleaddphoto_last_region"] = list(current_region)

                os.makedirs(os.path.dirname(laststate_path), exist_ok=True)
                with open(laststate_path, 'w') as f:
                    json.dump(full_state, f, indent=2)
                print(f"SAVED: laststate.json (region {current_region})")

                time.sleep(3)
                selectmedia()          # <-- your existing helper
                return

            # ---- Not found → retry logic ----
            retry_count += 1
            print(f"Retry {retry_count}/{max_retries}: Button not found")
            if retry_count >= max_retries:
                if any("loading" in t for t in text_lower):
                    print("Detected 'loading' – giving it one more second...")
                    time.sleep(1)
                    continue
                print("Max retries reached – giving up.")
            time.sleep(1)

    except Exception as e:
        print(f"Error in toggleaddphoto(): {e}")

def selectmedia():
    """
    Select media by COPYING the file path and PASTING it (faster & more reliable).
    Adds randomized human-like delays:
      - Before paste: 0.8–2.1 sec
      - Before Enter: 0.5–2.0 sec
    """
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

        print(f"Preparing to COPY-PASTE: {file_path}")
        
        # **COPY PATH TO CLIPBOARD**
        pyperclip.copy(file_path)
        print(f"COPIED TO CLIPBOARD: {file_path}")

        # **RANDOM DELAY BEFORE PASTING** (human thinking + focus shift)
        paste_delay = random.uniform(0.8, 2.1)
        print(f"Waiting {paste_delay:.2f}s before pasting...")
        time.sleep(paste_delay)

        # **PASTE PATH** (Ctrl+V)
        pyautogui.hotkey('ctrl', 'v')
        print("PASTED PATH (Ctrl+V)")

        # **RANDOM DELAY BEFORE ENTER** (0.5 to 2.0 sec)
        enter_delay = random.uniform(0.5, 2.0)
        print(f"Waiting {enter_delay:.2f}s before pressing Enter...")
        time.sleep(enter_delay)

        # **PRESS ENTER**
        pyautogui.press("enter")
        print("PRESSED ENTER")

        # Update tracker to indicate media has been selected
        selectmedia.has_uploaded = True
        print("Updated tracker: has_uploaded set to True")

        time.sleep(3)  # Final wait for upload dialog to process
        confirmselectedmedia()

    except Exception as e:
        print(f"Failed to select media: {str(e)}")
        selectmedia.has_uploaded = True  # Prevent retry loop
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
    NIGERIA FAST MODE: 6 BEHAVIORS (START/END + CAPSLOCK TYPOS)
    Strict 6-cycle. No last repeat. Saves state.
    """
    # ---- EARLY EXIT ----
    if getattr(writecaption_element, 'has_written', False):
        print("\nCAPTION ALREADY WRITTEN. SKIPPING.")
        return None

    print("\nLOCATING COMPOSER (NIGERIA FAST MODE)")

    # --------------------------------------------------------------------- #
    # 0. Load caption
    # --------------------------------------------------------------------- #
    try:
        with open(JSON_CONFIG_PATH, 'r') as json_file:
            config = json.load(json_file)
        author = config['author']
        group_types = config.get('group_types', 'others').lower()
        if group_types not in ['uk', 'others']:
            group_types = 'others'
        json_path = f"C:\\xampp\\htdocs\\serenum\\files\\captions\\{author}({group_types}).json"

        if not os.path.exists(json_path):
            raise FileNotFoundError(json_path)

        with open(json_path, 'r') as f:
            captions = json.load(f)

        selected_caption = random.choice(captions)['description']
        print(f"Caption: '{selected_caption}'")

    except Exception as e:
        print(f"JSON error: {e}")
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
        candidates = WebDriverWait(driver, 8).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        print(f"Found {len(candidates)} candidate(s).")
    except:
        print("No candidates.")
        return None

    # --------------------------------------------------------------------- #
    # 2. SPEED TYPING + BACKSPACE ENGINE
    # --------------------------------------------------------------------- #
    def type_with_speed(el, text, speed_profile):
        if not text:
            return
        ActionChains(driver).click(el).perform()
        time.sleep(random.uniform(0.1, 0.25))

        speed_map = {
            "fast": (0.01, 0.06),
            "slow": (0.04, 0.09)
        }

        p1 = len(text) // 3
        p2 = len(text) // 3
        p3 = len(text) - p1 - p2
        parts = [text[:p1], text[p1:p1+p2], text[p1+p2:]]

        for i, part in enumerate(parts):
            if not part:
                continue
            min_d, max_d = speed_map[speed_profile[i]]
            for char in part:
                ActionChains(driver).send_keys(char).perform()
                time.sleep(random.uniform(min_d, max_d))

    def backspace(el, count):
        for _ in range(count):
            ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
            time.sleep(random.uniform(0.06, 0.12))

    # --------------------------------------------------------------------- #
    # 3. 6 BEHAVIORS (START & END ONLY + CAPSLOCK)
    # --------------------------------------------------------------------- #
    def b1_start_typo(el, text):
        print("  [1] START typo → backspace → correct | Speed: fast-slow-fast")
        wrong = random.choice(['zx', 'qw', 'fp', 'vb'])
        type_with_speed(el, wrong, ["fast", "fast", "fast"])
        time.sleep(random.uniform(0.3, 0.7))
        backspace(el, len(wrong))
        type_with_speed(el, text, ["fast", "slow", "fast"])

    def b2_end_typo(el, text):
        print("  [2] END typo → backspace → correct | Speed: slow-fast-fast")
        type_with_speed(el, text, ["slow", "fast", "fast"])
        wrong = random.choice(['zx', 'qw', 'fp'])
        type_with_speed(el, wrong, ["fast", "fast", "fast"])
        time.sleep(random.uniform(0.3, 0.7))
        backspace(el, len(wrong))

    def b3_start_capslock(el, text):
        print("  [3] START CAPSLOCK typo → backspace → correct")
        wrong = random.choice(['Zx', 'Qw', 'Fp', 'Vb'])
        type_with_speed(el, wrong, ["fast", "fast", "fast"])
        time.sleep(random.uniform(0.4, 0.8))
        backspace(el, len(wrong))
        type_with_speed(el, text, ["fast", "slow", "fast"])

    def b4_end_capslock(el, text):
        print("  [4] END CAPSLOCK typo → backspace → correct")
        type_with_speed(el, text, ["slow", "fast", "fast"])
        wrong = random.choice(['Zx', 'Qw', 'Fp'])
        type_with_speed(el, wrong, ["fast", "fast", "fast"])
        time.sleep(random.uniform(0.4, 0.8))
        backspace(el, len(wrong))

    def b5_start_clear_rewrite(el, text):
        print("  [5] START typo → CLEAR ALL → rewrite | Speed: fast-fast-slow")
        wrong = random.choice(['zx', 'qw'])
        type_with_speed(el, wrong, ["fast", "fast", "fast"])
        time.sleep(0.5)
        backspace(el, len(wrong))
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        time.sleep(0.2)
        ActionChains(driver).send_keys(Keys.DELETE).perform()
        time.sleep(0.3)
        type_with_speed(el, text, ["fast", "fast", "slow"])

    def b6_end_partial_rewrite(el, text):
        print("  [6] END typo → delete last 3 → rewrite end | Speed: slow-slow-fast")
        type_with_speed(el, text[:-3], ["slow", "slow", "fast"])
        wrong = random.choice(['zx', 'qw', 'fp'])
        type_with_speed(el, wrong, ["fast", "fast", "fast"])
        time.sleep(0.5)
        backspace(el, len(wrong) + 3)
        type_with_speed(el, text[-3:], ["fast", "fast", "fast"])

    # Behavior registry
    behaviors = [
        ("start_typo", b1_start_typo),
        ("end_typo", b2_end_typo),
        ("start_capslock", b3_start_capslock),
        ("end_capslock", b4_end_capslock),
        ("start_clear", b5_start_clear_rewrite),
        ("end_partial", b6_end_partial_rewrite),
    ]
    behavior_order = [b[0] for b in behaviors]

    # --------------------------------------------------------------------- #
    # 4. LOAD laststate.json
    # --------------------------------------------------------------------- #
    laststate_path = r"C:\xampp\htdocs\serenum\laststate.json"
    used_behaviors = []
    last_used_behavior = None

    if os.path.exists(laststate_path):
        try:
            with open(laststate_path, 'r') as f:
                data = json.load(f)
                used = data.get("write_caption_previous_behaviors", [])
                used_behaviors = [s for s in used if s in behavior_order]
                last_used_behavior = data.get("caption_last_used")
                if last_used_behavior not in behavior_order:
                    last_used_behavior = None
        except Exception as e:
            print(f"ERROR reading laststate.json: {e}")

    print(f"Used: {len(used_behaviors)}/6 → {used_behaviors}")
    print(f"Last: {last_used_behavior}")

    # --------------------------------------------------------------------- #
    # 5. PICK NEXT BEHAVIOR (6-CYCLE)
    # --------------------------------------------------------------------- #
    next_behavior_key = None
    if len(used_behaviors) < 6:
        for key in behavior_order:
            if key not in used_behaviors:
                next_behavior_key = key
                break
    else:
        for key in behavior_order:
            if key != last_used_behavior:
                next_behavior_key = key
                break
        else:
            next_behavior_key = behavior_order[0]

    chosen_func = dict(behaviors)[next_behavior_key]
    print(f"USING: {next_behavior_key.upper()}")

    # --------------------------------------------------------------------- #
    # 6. Test candidates
    # --------------------------------------------------------------------- #
    working_element = None
    for i, el in enumerate(candidates):
        try:
            if not el.is_displayed():
                continue

            print(f"  [{i}] Testing → {next_behavior_key}")

            current = driver.execute_script(
                "return arguments[0].textContent || arguments[0].innerText || '';", el
            ).strip()

            if selected_caption.lower() in current.lower():
                print(f"  [{i}] Already present.")
                working_element = el
                writecaption_element.has_written = True
                writecaption_element.last_written_caption = selected_caption
                break

            chosen_func(el, selected_caption)
            time.sleep(0.6)

            final = driver.execute_script(
                "return arguments[0].textContent || arguments[0].innerText || '';", el
            ).strip()

            if selected_caption.lower() in final.lower():
                print(f"  SUCCESS! Composer locked.")
                working_element = el
                writecaption_element.has_written = True
                writecaption_element.last_written_caption = selected_caption

                # SAVE STATE
                if next_behavior_key not in used_behaviors:
                    used_behaviors.append(next_behavior_key)
                else:
                    used_behaviors.remove(next_behavior_key)
                    used_behaviors.append(next_behavior_key)
                used_behaviors = used_behaviors[-6:]

                state_data = {}
                if os.path.exists(laststate_path):
                    try:
                        with open(laststate_path, 'r') as f:
                            state_data = json.load(f)
                    except:
                        pass

                state_data.update({
                    "write_caption_previous_behaviors": used_behaviors,
                    "caption_last_used": next_behavior_key
                })

                try:
                    with open(laststate_path, 'w') as f:
                        json.dump(state_data, f, indent=2)
                    print(f"SAVED: {len(used_behaviors)}/6 | Last: {next_behavior_key}")
                except Exception as e:
                    print(f"ERROR writing laststate.json: {e}")

                break
            else:
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                ActionChains(driver).send_keys(Keys.DELETE).perform()

        except Exception as e:
            print(f"  [{i}] Error: {e}")

    # --------------------------------------------------------------------- #
    # 7. Return
    # --------------------------------------------------------------------- #
    if working_element:
        print(f"\nCOMPOSER FOUND | {next_behavior_key.upper()} | NIGERIA FAST MODE")
        return working_element
    else:
        print("\nFallback to OCR...")
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
    """
    Toggle the 'Set date and time' button or checkbox for scheduling a post.
    - Random delay: 1.0 to 3.0 seconds before click (human-like)
    - State tracker prevents redundant clicks
    - Multiple robust locators with fallback
    """
    try:
        # Initialize tracker if not already set
        if not hasattr(toggleschedule, 'is_toggled'):
            toggleschedule.is_toggled = False

        # Skip if already toggled
        if toggleschedule.is_toggled:
            print("Schedule toggle already activated. Skipping click operation.")
            return

        print("Locating 'Set date and time' toggle...")
        
        # Primary locator (flexible XPath + CSS hybrid via multiple strategies)
        scheduling_toggle = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'set date and time')]//input[@type='checkbox'] | "
                "//div[contains(@aria-label, 'Set date and time') or contains(text(), 'Set date and time')]//following-sibling::div[@role='switch'] | "
                "//span[contains(text(), 'Set date and time')]/following::input[1]"
            ))
        )

        # === RANDOM HUMAN-LIKE DELAY BEFORE CLICK ===
        delay = random.uniform(1.0, 3.0)
        print(f"Waiting {delay:.2f} seconds before toggling schedule...")
        time.sleep(delay)

        # Handle checkbox or switch
        if scheduling_toggle.tag_name == 'input' and scheduling_toggle.get_attribute('type') == 'checkbox':
            if not scheduling_toggle.is_selected():
                scheduling_toggle.click()
                print("Toggled 'Set date and time' checkbox ON.")
            else:
                print("'Set date and time' checkbox already enabled.")
        else:
            scheduling_toggle.click()
            print("Clicked 'Set date and time' toggle switch.")

        # Mark as toggled
        toggleschedule.is_toggled = True
        print("Tracker updated: is_toggled = True")

        time.sleep(2)  # Allow UI to respond

    except Exception as e:
        print(f"Primary locator failed: {str(e)}")
        try:
            print("Trying alternative locator...")
            
            # === ALTERNATIVE LOCATOR ===
            scheduling_toggle = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "[aria-label*='Schedule'] input[type='checkbox'], [data-testid*='schedule-toggle']"
                ))
            )

            # === RANDOM DELAY AGAIN (fallback path) ===
            delay = random.uniform(1.0, 3.0)
            print(f"Waiting {delay:.2f} seconds before fallback click...")
            time.sleep(delay)

            if scheduling_toggle.tag_name == 'input' and scheduling_toggle.get_attribute('type') == 'checkbox':
                if not scheduling_toggle.is_selected():
                    scheduling_toggle.click()
                    print("Toggled 'Set date and time' via alternative checkbox.")
                else:
                    print("'Set date and time' already enabled (alternative).")
            else:
                scheduling_toggle.click()
                print("Clicked toggle via alternative locator.")

            # Update tracker
            toggleschedule.is_toggled = True
            print("Tracker updated: is_toggled = True (fallback)")

            time.sleep(2)

        except Exception as e2:
            print(f"Alternative locator also failed: {str(e2)}")
            raise Exception("Could not locate or toggle 'Set date and time' button")




def set_webschedule():
    """
    Set web schedule using 6 input sequences in STRICT ORDER.
    Forces full 6-round cycle before any repeat.
    NEVER repeats last used.
    Records ONLY its own state in laststate.json (SAFE MERGE).
    """
    # --- 1. Read pageandgroupauthors.json ---
    pageauthors_path = r"C:\xampp\htdocs\serenum\pageandgroupauthors.json"
    print(f"[{time.strftime('%H:%M:%S')}] Reading pageandgroupauthors.json")
    try:
        with open(pageauthors_path, 'r') as f:
            pageauthors = json.load(f)
        author = pageauthors['author']
        type_value = pageauthors['type']
        group_types = pageauthors['group_types']
        print(f"Author: {author} | Type: {type_value} | Group: {group_types}")
    except FileNotFoundError:
        print("ERROR: pageandgroupauthors.json not found!")
        return
    except Exception as e:
        print(f"ERROR parsing pageandgroupauthors.json: {e}")
        return

    # --- 2. Build schedules.json path ---
    schedules_path = f"C:\\xampp\\htdocs\\serenum\\files\\next jpg\\{author}\\jsons\\{group_types}\\{type_value}schedules.json"
    print(f"Reading schedule from: {schedules_path}")

    try:
        with open(schedules_path, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {type_value}schedules.json not found!")
        return
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON in schedules.json")
        return

    # --- 3. Extract next_schedule ---
    next_schedule_list = json_data.get('next_schedule')
    if not next_schedule_list or len(next_schedule_list) == 0:
        print("ERROR: No next_schedule found!")
        return

    next_schedule = next_schedule_list[0]
    target_date = next_schedule.get('date')
    target_time_12h = next_schedule.get('time_12hour')
    target_time_24h = next_schedule.get('time_24hour')

    if not all([target_date, target_time_12h, target_time_24h]):
        print(f"ERROR: Missing schedule data: {next_schedule}")
        return

    target_time_12h = target_time_12h.strip().lower()
    target_time_24h = target_time_24h.strip()

    print(f"Target → Date: {target_date} | Time: {target_time_12h.upper()} ({target_time_24h})")

    # --- 4. Parse times ---
    match_12h = re.match(r"(\d{1,2}):(\d{2})\s*(am|pm)", target_time_12h, re.IGNORECASE)
    match_24h = re.match(r"(\d{1,2}):(\d{2})", target_time_24h)
    if not match_12h or not match_24h:
        print(f"ERROR: Invalid time format: {target_time_12h} / {target_time_24h}")
        return

    hour_12h, minute_12h, period = match_12h.groups()
    period = period.upper()
    hour_24h, minute_24h = match_24h.groups()

    # --- 5. Generate all date formats ---
    def generate_all_date_formats(target_date):
        day, month, year = target_date.split('/')
        day_padded = day.zfill(2)
        day_unpadded = day.lstrip('0')
        month_padded = month.zfill(2)
        year_short = year[-2:]

        month_map = {
            '01': ('January', 'Jan'), '02': ('February', 'Feb'), '03': ('March', 'Mar'),
            '04': ('April', 'Apr'), '05': ('May', 'May'), '06': ('June', 'Jun'),
            '07': ('July', 'Jul'), '08': ('August', 'Aug'), '09': ('September', 'Sep'),
            '10': ('October', 'Oct'), '11': ('November', 'Nov'), '12': ('December', 'Dec')
        }
        full_month, short_month = month_map.get(month, (month, month))

        return {
            'dd/mm/yyyy': f"{day_padded}/{month_padded}/{year}",
            'd/mm/yyyy': f"{day_unpadded}/{month_padded}/{year}",
            'dd/mm/yy': f"{day_padded}/{month_padded}/{year_short}",
            'd/mm/yy': f"{day_unpadded}/{month_padded}/{year_short}",
            'dd-mm-yyyy': f"{day_padded}-{month_padded}-{year}",
            'd-mm-yyyy': f"{day_unpadded}-{month_padded}-{year}",
            'dd-mm-yy': f"{day_padded}-{month_padded}-{year_short}",
            'd-mm-yy': f"{day_unpadded}-{month_padded}-{year_short}",
            'dd month yyyy': f"{day_padded} {full_month} {year}",
            'd month yyyy': f"{day_unpadded} {full_month} {year}",
            'dd mon yyyy': f"{day_padded} {short_month} {year}",
            'd mon yyyy': f"{day_unpadded} {short_month} {year}",
            'month dd, yyyy': f"{full_month} {day_padded}, {year}",
            'month d, yyyy': f"{full_month} {day_unpadded}, {year}",
            'mon dd yyyy': f"{short_month} {day_padded} {year}",
            'mon d yyyy': f"{short_month} {day_unpadded} {year}",
        }

    all_target_formats = generate_all_date_formats(target_date)

    # --- 6. Wait for Schedule Panel ---
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'schedule')]")
            )
        )
        print("Schedule panel loaded.")
        time.sleep(2)
    except TimeoutException:
        print("ERROR: Schedule panel not found!")
        return

    # --- 7. Locate Inputs ---
    inputs = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
    )
    print(f"Found {len(inputs)} input fields.")

    date_input = hour_input = minute_input = am_pm_input = None
    for i, inp in enumerate(inputs):
        ph = (inp.get_attribute("placeholder") or "").lower()
        al = (inp.get_attribute("aria-label") or "").lower()
        if "dd/mm/yyyy" in ph or "date" in al:
            date_input = inp
        elif "hour" in al:
            hour_input = inp
        elif "minute" in al:
            minute_input = inp
        elif "am" in al or "pm" in al or "period" in al:
            am_pm_input = inp

    if not all([date_input, hour_input, minute_input]):
        print("ERROR: Missing required inputs!")
        return

    is_24h_format = am_pm_input is None
    print(f"Time format: {'24-hour' if is_24h_format else '12-hour'}")

    # --- 8. Check if already correct ---
    current_date = (driver.execute_script("return arguments[0].value", date_input) or "").strip()
    _, extracted_time, _ = extract_texts() or ("", "", [])

    date_matches = any(current_date == fmt for fmt in all_target_formats.values())
    time_matches = False

    if is_24h_format:
        expected = f"Time: {hour_24h.zfill(2)}:{minute_24h}"
        time_matches = extracted_time == expected
    else:
        exp1 = f"Time: {int(hour_12h):d}:{minute_12h}"
        exp2 = f"Time: {hour_12h.zfill(2)}:{minute_12h}"
        time_matches = extracted_time in [exp1, exp2]

    if date_matches and time_matches:
        print("Schedule already correct. Skipping.")
        return

    # --- 9. SEQUENCE DEFINITIONS ---
    sequences = {
        "hh_date_mm": [
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("date", date_input, target_date),
            ("minute", minute_input, minute_24h),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None
        ],
        "hh_mm_date": [
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("minute", minute_input, minute_24h),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None,
            ("date", date_input, target_date)
        ],
        "mm_hh_date": [
            ("minute", minute_input, minute_24h),
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None,
            ("date", date_input, target_date)
        ],
        "mm_date_hh": [
            ("minute", minute_input, minute_24h),
            ("date", date_input, target_date),
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None
        ],
        "date_hh_mm": [
            ("date", date_input, target_date),
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("minute", minute_input, minute_24h),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None
        ],
        "date_mm_hh": [
            ("date", date_input, target_date),
            ("minute", minute_input, minute_24h),
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None
        ]
    }

    # --- 10. FIXED ORDER ---
    order = [
        "hh_date_mm",
        "hh_mm_date",
        "mm_hh_date",
        "mm_date_hh",
        "date_hh_mm",
        "date_mm_hh"
    ]

    # --- 11. LOAD laststate.json SAFELY ---
    laststate_path = r"C:\xampp\htdocs\serenum\laststate.json"
    used_sequences = []
    last_used = None
    full_state = {}  # Will hold entire JSON

    if os.path.exists(laststate_path):
        try:
            with open(laststate_path, 'r') as f:
                full_state = json.load(f)
            used = full_state.get("setwebschedule_previous_input", [])
            used_sequences = [s for s in used if s in order]
            last_used = full_state.get("last_used")
            if last_used not in order:
                last_used = None
        except Exception as e:
            print(f"ERROR reading laststate.json: {e}")
            full_state = {}

    print(f"Used so far: {len(used_sequences)}/6 → {used_sequences}")
    print(f"Last used: {last_used}")

    # --- 12. PICK NEXT IN STRICT 6-CYCLE ---
    next_seq_key = None
    if len(used_sequences) < 6:
        for seq in order:
            if seq not in used_sequences:
                next_seq_key = seq
                break
    else:
        for seq in order:
            if seq != last_used:
                next_seq_key = seq
                break
        else:
            next_seq_key = order[0]

    chosen_seq = [s for s in sequences[next_seq_key] if s is not None]
    seq_names = " → ".join([s[0].capitalize() for s in chosen_seq])
    print(f"USING #{used_sequences.count(next_seq_key) + 1 if next_seq_key in used_sequences else 1}: {next_seq_key} → {seq_names}")

    # --- 13. EXECUTE SEQUENCE ---
    for field_name, element, value in chosen_seq:
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)
            element.click()
            time.sleep(0.5)

            if field_name == "date":
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                time.sleep(0.3)
                ActionChains(driver).send_keys(value).perform()
            elif field_name == "period":
                ActionChains(driver).send_keys(value).send_keys(Keys.ENTER).perform()
            else:
                element.clear()
                time.sleep(0.3)
                element.send_keys(value)

            element.send_keys(Keys.TAB)
            time.sleep(0.6)
        except Exception as e:
            if "intercepted" in str(e).lower():
                print("Click intercepted. Reloading...")
                reset_trackers()
                driver.refresh()
                raise
            else:
                print(f"Error on {field_name}: {e}")
                raise

    # --- 14. UPDATE used_sequences (rotate) ---
    if next_seq_key not in used_sequences:
        used_sequences.append(next_seq_key)
    else:
        used_sequences.remove(next_seq_key)
        used_sequences.append(next_seq_key)
    used_sequences = used_sequences[-6:]  # Keep last 6

    # --- 15. FINAL VERIFICATION ---
    time.sleep(1.5)
    final_date = (driver.execute_script("return arguments[0].value", date_input) or "").strip()
    _, final_time, _ = extract_texts() or ("", "", [])

    if not any(final_date == fmt for fmt in all_target_formats.values()):
        raise Exception(f"Date not set: '{final_date}'")
    if is_24h_format:
        if final_time != f"Time: {hour_24h.zfill(2)}:{minute_24h}":
            raise Exception(f"Time not set: '{final_time}'")
    else:
        exp = [f"Time: {int(hour_12h):d}:{minute_12h}", f"Time: {hour_12h.zfill(2)}:{minute_12h}"]
        if final_time not in exp:
            raise Exception(f"Time not set: '{final_time}'")

    print(f"SCHEDULE SET: {target_date} @ {target_time_12h.upper()} via {seq_names}")

    # --- 16. Handle Overlay ---
    overlays = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay')]")
    if overlays:
        print("Overlay detected. Reloading...")
        reset_trackers()
        driver.refresh()
        raise Exception("Overlay after set")

    # --- 17. SAVE ONLY OUR STATE (PRESERVE OTHERS) ---
    full_state.update({
        "setwebschedule_previous_input": used_sequences,
        "last_used": next_seq_key
    })

    try:
        with open(laststate_path, 'w') as f:
            json.dump(full_state, f, indent=2)
        print(f"SAVED (SAFE): {len(used_sequences)}/6 used | Last: {next_seq_key}")
    except Exception as e:
        print(f"ERROR writing laststate.json: {e}")

    print("set_webschedule() completed successfully.\n")
    click_schedule_button()
    

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
    """Archive VALID URLs from next_jpgcard.json → uploadedjpgs.json
       AND DELETE **ALL** files from BOTH:
         - next jpg folder
         - uploaded jpgs folder
       Only valid URLs are preserved. Safe, robust, full logging."""

    # ------------------------------------------------------------------ #
    # 1. Load configuration
    # ------------------------------------------------------------------ #
    JSON_CONFIG_PATH = r'C:\xampp\htdocs\serenum\pageandgroupauthors.json'

    try:
        with open(JSON_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)

        author = config.get('author', '').strip()
        if not author:
            print("Error: 'author' is missing or empty in config.")
            return

    except Exception as e:
        print(f"Failed to load config: {e}")
        return

    # ------------------------------------------------------------------ #
    # 2. Define paths
    # ------------------------------------------------------------------ #
    next_dir       = fr'C:\xampp\htdocs\serenum\files\next jpg\{author}'
    uploaded_dir   = fr'C:\xampp\htdocs\serenum\files\uploaded jpgs\{author}'
    next_json_path = os.path.join(next_dir, 'next_jpgcard.json')
    uploaded_json_path = os.path.join(uploaded_dir, 'uploadedjpgs.json')

    os.makedirs(next_dir, exist_ok=True)
    os.makedirs(uploaded_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    # 3. Load next_jpgcard.json – keep ONLY valid URLs
    # ------------------------------------------------------------------ #
    next_urls = []
    if os.path.exists(next_json_path):
        try:
            with open(next_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            raw = data.get("next_jpgcard")

            if raw is not None:
                items = [raw] if isinstance(raw, str) else raw
                for item in items:
                    if isinstance(item, str):
                        url = item.strip()
                        if url.lower().startswith(('http://', 'https://')):
                            next_urls.append(url)
                        else:
                            print(f"Skipped invalid URL: {url}")
        except Exception as e:
            print(f"Failed to read next_jpgcard.json: {e}")
    else:
        print(f"Info: No next_jpgcard.json found.")

    print(f"Detected {len(next_urls)} valid URL(s) to archive.")

    # ------------------------------------------------------------------ #
    # 4. Delete ALL files from next jpg folder
    # ------------------------------------------------------------------ #
    next_files = [f for f in os.listdir(next_dir) if os.path.isfile(os.path.join(next_dir, f))]
    next_deleted = 0
    next_failed = []

    if next_files:
        print(f"\nDeleting {len(next_files)} file(s) from next jpg:")
        for f in next_files:
            path = os.path.join(next_dir, f)
            try:
                os.remove(path)
                next_deleted += 1
                print(f"   Deleted: next jpg/{f}")
            except Exception as e:
                next_failed.append((f, str(e)))
                print(f"   Failed: {f} → {e}")
    else:
        print("\nnext jpg folder already empty.")

    # ------------------------------------------------------------------ #
    # 5. Delete ALL files from uploaded jpgs folder (except JSON)
    # ------------------------------------------------------------------ #
    uploaded_files = [
        f for f in os.listdir(uploaded_dir)
        if os.path.isfile(os.path.join(uploaded_dir, f)) and f != 'uploadedjpgs.json'
    ]
    uploaded_deleted = 0
    uploaded_failed = []

    if uploaded_files:
        print(f"\nDeleting {len(uploaded_files)} file(s) from uploaded jpgs:")
        for f in uploaded_files:
            path = os.path.join(uploaded_dir, f)
            try:
                os.remove(path)
                uploaded_deleted += 1
                print(f"   Deleted: uploaded jpgs/{f}")
            except Exception as e:
                uploaded_failed.append((f, str(e)))
                print(f"   Failed: {f} → {e}")
    else:
        print("\nuploaded jpgs folder has no extra files.")

    # ------------------------------------------------------------------ #
    # 6. Load existing uploadedjpgs.json – keep ONLY valid URLs
    # ------------------------------------------------------------------ #
    existing_uploaded = []
    if os.path.exists(uploaded_json_path):
        try:
            with open(uploaded_json_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                raw = existing_data.get("uploaded_jpgs", [])
                candidates = [raw] if isinstance(raw, str) else raw
                for u in candidates:
                    if isinstance(u, str) and u.strip().lower().startswith(('http://', 'https://')):
                        existing_uploaded.append(u.strip())
        except Exception as e:
            print(f"Warning: Could not read uploadedjpgs.json: {e}")

    print(f"Found {len(existing_uploaded)} previously valid URLs.")

    # ------------------------------------------------------------------ #
    # 7. Combine & deduplicate URLs
    # ------------------------------------------------------------------ #
    all_urls = existing_uploaded + next_urls
    unique_urls = list(dict.fromkeys(all_urls))  # Preserves order
    newly_added = len(unique_urls) - len(existing_uploaded)

    # ------------------------------------------------------------------ #
    # 8. Save updated uploadedjpgs.json
    # ------------------------------------------------------------------ #
    timestamp = datetime.now(pytz.timezone('Africa/Lagos')).isoformat()

    uploaded_data = {
        "uploaded_jpgs": unique_urls,
        "last_cleared": timestamp,
        "total_uploaded": len(unique_urls),
        "urls_added_this_time": len(next_urls),
        "new_unique_urls": newly_added,
        "next_jpg_files_deleted": next_deleted,
        "uploaded_jpgs_files_deleted": uploaded_deleted,
        "failed_deletes_next": [f"{n}: {e}" for n, e in next_failed],
        "failed_deletes_uploaded": [f"{n}: {e}" for n, e in uploaded_failed],
        "author": author
    }

    try:
        with open(uploaded_json_path, 'w', encoding='utf-8') as f:
            json.dump(uploaded_data, f, indent=4, ensure_ascii=False)
        print(f"\nSaved uploadedjpgs.json → {len(unique_urls)} clean URLs")
    except Exception as e:
        print(f"Failed to write JSON: {e}")
        return

    # ------------------------------------------------------------------ #
    # 9. Clear next_jpgcard.json
    # ------------------------------------------------------------------ #
    try:
        cleared = {
            "next_jpgcard": [],
            "timestamp": timestamp,
            "total_checked": data.get("total_checked", 0) if 'data' in locals() else 0,
            "total_valid": len(next_urls),
            "note": "Cleared by uploadedjpgs() – ALL files deleted from both folders"
        }
        with open(next_json_path, 'w', encoding='utf-8') as f:
            json.dump(cleared, f, indent=4, ensure_ascii=False)
        print("Cleared next_jpgcard.json")
    except Exception as e:
        print(f"Warning: Could not clear next_jpgcard.json: {e}")

    # ------------------------------------------------------------------ #
    # 10. Final Summary
    # ------------------------------------------------------------------ #
    print("\n" + "="*70)
    print(f" FULL CLEANUP COMPLETE FOR @{author.upper()}")
    print(f"   URLs archived       : {len(next_urls)} → {newly_added} new")
    print(f"   next jpg deleted    : {next_deleted} file(s)")
    print(f"   uploaded jpgs deleted: {uploaded_deleted} file(s)")
    if next_failed: print(f"   next failed         : {len(next_failed)}")
    if uploaded_failed: print(f"   uploaded failed     : {len(uploaded_failed)}")
    print(f"   Total valid URLs    : {len(unique_urls)}")
    print(f"   Both folders now clean (except uploadedjpgs.json)")
    print("="*70)
    print(f"\nReady for fresh upload cycle. @teamxtech")

def moveuploadedurls():
    """
    Automates moving uploaded JPG URLs to the 'Uploaded' folder on jpgsvault.rf.gd using Selenium.
    After successful move:
      • Deletes ALL image files (.jpg, .png, .gif, etc.) from:
          - jpgfolders\{author}
          - next jpg\{author}
          - uploaded jpgs\{author}
      • Clears next_jpgcard.json
      • Removes moved URLs from uploadedjpgs.json
    Full cleanup for a clean slate.
    """
    # --------------------- CONFIG & PATHS ---------------------
    TARGET_URL = "https://jpgsvault.rf.gd/jpgsvault.php"
    CONFIG_PATH = r'C:\xampp\htdocs\serenum\pageandgroupauthors.json'
    UPLOADED_JSON_DIR = r'C:\xampp\htdocs\serenum\files\uploaded jpgs'
    NEXT_JSON_DIR = r'C:\xampp\htdocs\serenum\files\next jpg'
    JPGFOLDERS_DIR = r'C:\xampp\htdocs\serenum\files\jpgfolders'
    CHROME_BINARY = r"C:\xampp\htdocs\CIPHER\googlechrome\Google\Chrome\Application\chrome.exe"

    # Supported image extensions (case-insensitive)
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.tif', '.ico', '.svg'}

    print("\n" + "="*80)
    print("STARTING: move uploaded urls + FULL IMAGE CLEANUP (ALL FOLDERS)")
    print("="*80)

    # --------------------- LOAD CONFIG ---------------------
    if not os.path.exists(CONFIG_PATH):
        print(f"ERROR: Config file not found: {CONFIG_PATH}")
        return

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        author = config.get('author', '').strip()
        if not author:
            print("ERROR: 'author' is missing or empty in config.")
            return
        print(f"Author: {author}")
    except Exception as e:
        print(f"ERROR: Failed to load config: {e}")
        return

    # --------------------- DERIVED PATHS ---------------------
    uploaded_json_path = os.path.join(UPLOADED_JSON_DIR, author, 'uploadedjpgs.json')
    next_json_path = os.path.join(NEXT_JSON_DIR, author, 'next_jpgcard.json')
    jpgfolder_dir = os.path.join(JPGFOLDERS_DIR, author)
    next_dir = os.path.join(NEXT_JSON_DIR, author)
    uploaded_dir = os.path.join(UPLOADED_JSON_DIR, author)

    # Ensure all author directories exist
    author_dirs = {
        'jpgfolders': jpgfolder_dir,
        'next_jpg': next_dir,
        'uploaded_jpgs': uploaded_dir
    }

    for name, path in author_dirs.items():
        if not os.path.exists(path):
            print(f"WARNING: Directory not found: {path} ({name})")
        else:
            print(f"Found: {path} ({name})")

    if not os.path.exists(uploaded_json_path):
        print(f"ERROR: uploadedjpgs.json not found: {uploaded_json_path}")
        return

    # --------------------- LOAD UPLOADED URLS TO MOVE ---------------------
    try:
        with open(uploaded_json_path, 'r', encoding='utf-8') as f:
            uploaded_data = json.load(f)
        all_uploaded_urls = uploaded_data.get("uploaded_jpgs", [])
    except Exception as e:
        print(f"ERROR: Failed to read uploadedjpgs.json: {e}")
        return

    if not all_uploaded_urls:
        print("No URLs in uploadedjpgs.json. Nothing to move.")
        return

    # Load next_jpgcard to know which ones were just marked
    next_urls = []
    if os.path.exists(next_json_path):
        try:
            with open(next_json_path, 'r', encoding='utf-8') as f:
                next_data = json.load(f)
            next_urls = next_data.get("next_jpgcard", [])
        except Exception as e:
            print(f"Warning: Could not read next_jpgcard.json: {e}")
    else:
        print("No next_jpgcard.json found. Will move all in uploadedjpgs.json.")

    # Use next_urls if available, else fall back to all
    urls_to_move = next_urls if next_urls else all_uploaded_urls
    if not urls_to_move:
        print("No URLs to move (next_jpgcard empty and no fallback).")
        return

    print(f"Preparing to move {len(urls_to_move)} URL(s) to 'Uploaded' folder...")

    # --------------------- SETUP SELENIUM ---------------------
    driver = None
    success = False
    try:
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-autofill")
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

        if os.path.exists(CHROME_BINARY):
            options.binary_location = CHROME_BINARY
            print("Using custom Chrome binary.")
        else:
            print("Custom Chrome binary not found. Using default.")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(driver_version="139.0.7258.128").install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        driver.implicitly_wait(10)

        print(f"Navigating to: {TARGET_URL}")
        driver.get(TARGET_URL)
        time.sleep(3)

        # Click "FOLDERS ▼"
        print('Clicking "FOLDERS ▼"')
        folder_toggle = driver.find_element(By.ID, "folder-toggle")
        folder_toggle.click()
        time.sleep(1)

        # Click author folder
        print(f'Opening folder: "{author}"')
        folder_menu = driver.find_element(By.ID, "folder-menu")
        author_folder_xpath = f".//div[contains(@class, 'folder-item')]//span[@class='folder-name' and text()='{author}']"
        author_folder = folder_menu.find_element(By.XPATH, author_folder_xpath)
        author_folder.click()
        time.sleep(2)

        # Click "Move to Uploaded"
        print('Clicking "Move to Uploaded"')
        move_btn = driver.find_element(By.ID, "move-to-uploaded-btn")
        move_btn.click()
        time.sleep(1)

        # Input URLs
        print(f"Pasting {len(urls_to_move)} URL(s)...")
        textarea = driver.find_element(By.ID, "move-indices")
        url_input = ",\n".join(urls_to_move)
        textarea.clear()
        textarea.send_keys(url_input)

        # Click Move
        print('Confirming move...')
        move_yes_btn = driver.find_element(By.ID, "move-yes")
        move_yes_btn.click()
        time.sleep(4)

        # Check success
        try:
            alert_modal = driver.find_element(By.ID, "alert-modal")
            alert_msg = alert_modal.find_element(By.ID, "alert-message").text
            print(f"Server: {alert_msg}")

            if "moved" in alert_msg.lower() and "to uploaded" in alert_msg.lower():
                success = True
                print("SUCCESS: Server confirmed move!")
                alert_ok = driver.find_element(By.ID, "alert-ok")
                alert_ok.click()
            else:
                print("WARNING: Move may have failed. Check message.")
        except Exception as e:
            print(f"WARNING: No alert appeared. Exception: {e}")

    except Exception as e:
        print(f"SELENIUM ERROR: {e}")
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
            print("Browser closed.")

    # --------------------- FULL CLEANUP (ONLY IF SUCCESS) ---------------------
    if not success:
        print("\nCLEANUP SKIPPED: Move was not confirmed successful.")
        return

    print("\n" + "-"*60)
    print("STARTING FULL IMAGE CLEANUP ACROSS ALL AUTHOR FOLDERS")
    print("-"*60)

    deleted_files = 0
    failed_deletes = 0

    def is_image_file(filepath):
        """Check if file is an image by extension AND content (using imghdr)"""
        if not os.path.isfile(filepath):
            return False
        ext = os.path.splitext(filepath)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            # Double-check with imghdr (except for SVG which is XML)
            if ext == '.svg':
                return True
            try:
                return imghdr.what(filepath) is not None
            except:
                return ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        return False

    def delete_images_in_folder(folder_path, label):
        nonlocal deleted_files, failed_deletes
        if not os.path.exists(folder_path):
            print(f"{label} not found: {folder_path}")
            return
        print(f"Scanning for images in: {folder_path}")
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if is_image_file(file_path):
                try:
                    os.remove(file_path)
                    deleted_files += 1
                    print(f"  [DELETED] {label}/{filename}")
                except Exception as e:
                    failed_deletes += 1
                    print(f"  [FAILED] {label}/{filename} → {e}")

    # 1. Delete ALL images from all three author directories
    delete_images_in_folder(jpgfolder_dir, "jpgfolders")
    delete_images_in_folder(next_dir, "next jpg")
    delete_images_in_folder(uploaded_dir, "uploaded jpgs")

    # 2. Clear next_jpgcard.json
    if os.path.exists(next_json_path):
        try:
            with open(next_json_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "next_jpgcard": [],
                    "timestamp": datetime.now(pytz.timezone('Africa/Lagos')).isoformat(),
                    "note": "Cleared after successful move to Uploaded folder"
                }, f, indent=4)
            print(f"Cleared: {next_json_path}")
        except Exception as e:
            print(f"Failed to clear next_jpgcard.json: {e}")
    else:
        print("next_jpgcard.json not found (already clean)")

    # 3. Remove moved URLs from uploadedjpgs.json
    remaining_urls = [u for u in all_uploaded_urls if u not in urls_to_move]
    try:
        timestamp = datetime.now(pytz.timezone('Africa/Lagos')).isoformat()
        new_data = {
            "uploaded_jpgs": remaining_urls,
            "last_moved_to_uploaded": timestamp,
            "total_uploaded": len(remaining_urls),
            "last_moved_count": len(urls_to_move),
            "author": author
        }
        with open(uploaded_json_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=4)
        print(f"Updated uploadedjpgs.json → {len(remaining_urls)} remaining")
    except Exception as e:
        print(f"Failed to update uploadedjpgs.json: {e}")

    # --------------------- FINAL SUMMARY ---------------------
    print("\n" + "="*80)
    print("FULL CLEANUP COMPLETE")
    print("="*80)
    print(f"Moved URLs             : {len(urls_to_move)}")
    print(f"Total images deleted   : {deleted_files}")
    print(f"Delete failures        : {failed_deletes}")
    print(f"Remaining in uploaded  : {len(remaining_urls)}")
    print(f"next_jpgcard.json      : CLEARED")
    print(f"All author image dirs  : CLEANED (.jpg, .png, .gif, .webp, etc.)")
    print("="*80)
    print("All done. Ready for next batch!")


def firstbatch():  
    fetch_urls()
    corruptedjpgs()
    markjpgs()
    corruptedjpgs()
    crop_and_moveto_jpgs()
    orderjpgs()

def secondbatch():  
    selectgroups() #*
    toggleaddphoto() #*
    writecaption_element()
    toggleschedule() #*
    update_calendar()
    set_webschedule() #*  
    uploadedjpgs() 

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
   




