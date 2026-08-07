from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # ← 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECZtfn
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
from datetime import datetime, timezone
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
import csv
import random
import string
import psutil
from datetime import datetime, timezone
import connectwithinfinitydb as db
import json
import os
from datetime import datetime
import time
from selenium.webdriver.common.by import By
import pyautogui
import pytesseract
from PIL import Image
import os
import glob
from datetime import datetime
import subprocess
import json
import win32gui
import win32con
import win32process
import win32api
import win32process
import psutil
import time
import re
import difflib
import pyperclip
import keyboard 
import tkinter as tk
import threading
import zipfile
import csv
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
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
import os
import json
import csv
import random
import string


# Global JSON configuration path
JSON_CONFIG_PATH = r'C:\xampp\htdocs\AI automation\serenum\pageandgroupauthors.json'
GUI_PATH = r'C:\xampp\htdocs\AI automation\serenum\files\gui'
NEW_CONFIGS = r"C:\xampp\htdocs\AI automation\serenum\new_configs.json"
DEFAULT_PATH = r"C:\xampp\htdocs\AI automation\serenum"
AUTHOR_URL = r"C:\xampp\htdocs\AI automation\serenum\pageandgroupaccounts.json"
URLS_FILE = r"C:\xampp\htdocs\AI automation\serenum\files\fetchedjpgsurl.json"
INPUT_IMAGE_PATH = r"C:\xampp\htdocs\AI automation\serenum\input_images"
OUTPUT_TEXT_PATH = r"C:\xampp\htdocs\AI automation\serenum\screen_content.text"
UPDATED_CONFIGS = r"C:\xampp\htdocs\AI automation\serenum\updated_configs.json"
PHPSQLURL = "https://fhdrikxsirudr.fwh.is/phpmyadmintemplate.php"
NEW_CONFIGS = r"C:\xampp\htdocs\AI automation\serenum\new_configs.json"
UPDATED_CONFIGS = r"C:\xampp\htdocs\AI automation\serenum\updated_configs.json"
URLS_FILE = r"C:\xampp\htdocs\AI automation\serenum\files\fetchedjpgsurl.json"
AUTHOR_URL = r"C:\xampp\htdocs\AI automation\serenum\pageandgroupaccounts.json"
CAPTIONS_PATH = r"C:\xampp\htdocs\AI automation\serenum\files\captions"
TIME_ORDER_PATH = r"C:\xampp\htdocs\AI automation\serenum\timeorders.json"  
AUTHOR_PATH = r"C:\xampp\htdocs\AI automation\serenum\pageandgroupauthors.json"  
FILES_ROOT = r"C:\xampp\htdocs\AI automation\serenum\files"

# Global driver and wait objects
driver = None
wait = None
# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\xampp\htdocs\AI automation\serenum\pytesseract\tessdata"

# Configure Paths
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\xampp\htdocs\AI automation\sceniq\pytesseract\tessdata"
tessdata_path = r"C:\xampp\htdocs\AI automation\scenIQ\pytesseract\tessdata\eng.traineddata"
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
class AutomationHUD:
    def __init__(self):
        self.root = None
        self.label_status = None
        self.visible = True
        self.current_text = "Initializing..."
        self.status_history = []
        self.current_status_type = "initializing"
        self.thread = threading.Thread(target=self._run_hud, daemon=True)
        self.thread.start()

    def _run_hud(self):
        self.root = tk.Tk()
        self.root.title("Automation HUD")
        
        # Frameless, always on top, transparent background
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.config(bg="black")
        
        # Make window larger to display full text
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 600, 120  # Increased height for text visibility
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2) - 100
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        # Main container with black background
        container = tk.Frame(self.root, bg="black")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status message with large, bold font centered
        self.label_status = tk.Label(container, text="🚀 Initializing...", 
                                   font=("Segoe UI", 10, "bold"), 
                                   fg="#00FFCC", bg="black",
                                   wraplength=560, justify="center")
        self.label_status.pack(expand=True, fill="both")
        
        # Apply Windows styling hooks for click-through
        try:
            hwnd = win32gui.GetParent(self.root.winfo_id())
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                                 ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        except:
            pass  # Fallback if Windows API fails
        
        self.root.mainloop()

    def print(self, text, status_type="processing"):
        """Update status text"""
        self.current_text = text
        self.current_status_type = status_type
        
        # Store history
        self.status_history.append((time.time(), text))
        if len(self.status_history) > 20:
            self.status_history.pop(0)
        
        # Update UI in thread-safe manner
        if self.root and self.label_status:
            # Color mapping for different status types
            color_map = {
                "searching": "#00CCFF",
                "scanning": "#00FF88",
                "processing": "#00FFCC",
                "success": "#00FF88",
                "warning": "#FFAA00",
                "waiting": "#8888FF",
                "clicking": "#FF66CC",
                "typing": "#66CCFF",
                "navigating": "#FF8844",
                "error": "#FF4466",
                "initializing": "#00FFCC",
                "booting": "#00CCFF",
                "connecting": "#66CCFF",
                "loading": "#00FF88",
                "verifying": "#00FFCC",
                "complete": "#FF66CC"
            }
            color = color_map.get(status_type, "white")
            self.root.after(0, lambda: self.label_status.config(text=text, fg=color))
        
        # Log with timestamp
        timestamp = time.strftime("%H:%M:%S")
        # Extract emoji from text if present
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+', flags=re.UNICODE)
        emojis = emoji_pattern.findall(text)
        icon = emojis[0] if emojis else "📊"
        clean_text = emoji_pattern.sub('', text).strip()
        print(f"{icon} [HUD @ {timestamp}] {clean_text}")

    def hide(self):
        """Hide the HUD (kept for compatibility but not used)"""
        self.visible = False

    def show(self):
        """Show the HUD (kept for compatibility)"""
        self.visible = True

    def show_summary(self, final_status="✅ Operation Complete"):
        """Display final operation summary with flash effect"""
        if self.root:
            self.print(final_status, "complete")
            # Flash effect for completion
            for _ in range(3):
                if self.root:
                    self.root.attributes("-alpha", 0.7)
                    time.sleep(0.1)
                    self.root.attributes("-alpha", 1.0)
                    time.sleep(0.1)

    def cleanup(self):
        """Clean up resources"""
        if self.root:
            self.root.quit()
            self.root.destroy()
hud = AutomationHUD()
def ocr():
    """
    Validates environment, cleans working directories, captures the screen,
    extracts all characters, spatially merges characters/words purely by coordinate 
    proximity (ignoring brittle Tesseract line numbers) to rebuild clean text chunks, 
    writes output logs, and summarizes results.
    """
    
    
    if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        print(f"❌ Error: Tesseract executable not found at: {pytesseract.pytesseract.tesseract_cmd}")
        return None
    if not os.path.exists(tessdata_path):
        print(f"❌ Error: English language data not found at: {tessdata_path}")
        return None
    try:
        # Create the input_images directory if it doesn't exist
        os.makedirs(INPUT_IMAGE_PATH, exist_ok=True)
        
        if os.path.exists(INPUT_IMAGE_PATH):
            for file in glob.glob(os.path.join(INPUT_IMAGE_PATH, "*.png")):
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"   ⚠️ Could not delete {os.path.basename(file)}: {e}")

        print("📸 Capturing screen...")
        screenshot = pyautogui.screenshot()
        output_image_path = os.path.join(INPUT_IMAGE_PATH, "screen.png")
        screenshot.save(output_image_path)

        screen_width, screen_height = pyautogui.size()
        print(f"🖥️ Screen Dimensions: {screen_width} x {screen_height} pixels")
        
        print("📝 Extracting text with coordinates...")
        custom_config = (
            '--psm 11 -c tessedit_char_whitelist='
            '\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,:-_=@############/\\\\?&|()[]{}<>~°%©®+— \\"\\\'\''
        )
        
        data = pytesseract.image_to_data(screenshot, config=custom_config, output_type=pytesseract.Output.DICT)
        
        raw_elements = []
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            text = data['text'][i].strip()
            confidence = int(data['conf'][i])
            
            if text:
                left = data['left'][i]
                top = data['top'][i]
                width = data['width'][i]
                height = data['height'][i]
                
                raw_elements.append({
                    'text': text,
                    'left': left,
                    'top': top,
                    'right': left + width,
                    'bottom': top + height,
                    'width': width,
                    'height': height,
                    'confidence': confidence
                })
        clean_texts = []
        
        if raw_elements:
            raw_elements.sort(key=lambda x: (x['top'], x['left']))
            
            while raw_elements:
                current = raw_elements.pop(0)
                max_horizontal_gap = max(12, current['height'] * 0.4) 
                max_vertical_deviation = current['height'] * 0.4      
                
                merged_any = True
                while merged_any:
                    merged_any = False
                    for i, next_el in enumerate(raw_elements):
                        current_center_y = current['top'] + (current['height'] / 2)
                        next_center_y = next_el['top'] + (next_el['height'] / 2)
                        
                        is_same_line_geometry = abs(current_center_y - next_center_y) <= max_vertical_deviation
                        horizontal_gap = next_el['left'] - current['right']
                        is_close_horizontally = (-5 <= horizontal_gap <= max_horizontal_gap)
                        
                        if is_same_line_geometry and is_close_horizontally:
                            if horizontal_gap > 3 and not current['text'].endswith(('/', ':', '.', '@', '-')):
                                current['text'] += " " + next_el['text']
                            else:
                                current['text'] += next_el['text']
                                
                            current['right'] = max(current['right'], next_el['right'])
                            current['left'] = min(current['left'], next_el['left'])
                            current['top'] = min(current['top'], next_el['top'])
                            current['bottom'] = max(current['bottom'], next_el['bottom'])
                            current['width'] = current['right'] - current['left']
                            current['height'] = current['bottom'] - current['top']
                            
                            if current['confidence'] != -1 and next_el['confidence'] != -1:
                                current['confidence'] = (current['confidence'] + next_el['confidence']) // 2
                            
                            raw_elements.pop(i)
                            merged_any = True
                            break
                
                current['distance_from_top'] = current['top']
                current['distance_from_bottom'] = screen_height - current['bottom']
                current['screen_percentage'] = (current['top'] / screen_height) * 100
                
                if "htips" in current['text']:
                    current['text'] = current['text'].replace("htips", "https")
                if "searcl" in current['text'].lower():
                    current['text'] = current['text'].lower().replace("searcl", "search").replace("Searcl", "Search")
                    
                clean_texts.append(current)

            clean_texts.sort(key=lambda x: (x['top'], x['left']))

        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(OUTPUT_TEXT_PATH), exist_ok=True)
        with open(OUTPUT_TEXT_PATH, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("GEOMETRICALLY CLEANED SCREEN EXTRACTION\n")
            f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Screen Resolution: {screen_width} x {screen_height} pixels\n")
            f.write("="*80 + "\n\n")
            
            for i, word_data in enumerate(clean_texts, 1):
                f.write(f"Text Block {i}: {word_data['text']}\n")
                f.write(f"  Left: {word_data['left']:>6}  Top: {word_data['top']:>6}\n")
                f.write(f"  Right: {word_data['right']:>6}  Bottom: {word_data['bottom']:>6}\n")
                f.write(f"  Width: {word_data['width']:>6}  Height: {word_data['height']:>6}\n")
                f.write(f"  📏 Distance from Top: {word_data['distance_from_top']:>6} pixels ({word_data['screen_percentage']:.1f}% of screen)\n")
                f.write(f"  📏 Distance from Bottom: {word_data['distance_from_bottom']:>6} pixels\n")
                f.write(f"  Confidence: {word_data['confidence']}%\n")
                f.write("-" * 40 + "\n")
            
            f.write("\n\n" + "="*80 + "\n")
            f.write("COMPACT FORMAT (left, top, right, bottom, distance_from_top_px, screen_percentage%, text):\n")
            f.write("="*80 + "\n")
            for word_data in clean_texts:
                f.write(f"{word_data['left']:>6}, {word_data['top']:>6}, {word_data['right']:>6}, {word_data['bottom']:>6}, "
                        f"{word_data['distance_from_top']:>6}px, {word_data['screen_percentage']:>5.1f}%, '{word_data['text']}'\n")

        full_text = "   ".join([word['text'] for word in clean_texts])
        print(f"✅ Total clean text blocks saved: {len(clean_texts)}")
        
        if clean_texts:
            highest = min(clean_texts, key=lambda x: x['top'])
            lowest = max(clean_texts, key=lambda x: x['bottom'])
        print("="*80)

        return clean_texts

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return None
def abort_operation(reason="Operation aborted"):
        """
        Global abort helper that triggers the Alt+/ hotkey to stop the automation.
        Can be called from anywhere in the function to gracefully terminate.
        
        Args:
            reason: String describing why the operation was aborted
        """
        print(f"🛑 [ABORT] {reason}")
        hud.print(f"🛑 {reason}", "error")
        
        # Trigger the termination flag
        global terminate_automation
        terminate_automation = True
        
        # Also simulate the hotkey press as a backup
        try:
            pyautogui.hotkey('alt', '/')
        except Exception:
            pass
        
        # Raise KeyboardInterrupt to break out of loops
        raise KeyboardInterrupt(f"Operation aborted: {reason}")

# db and tables
def analyze_and_distribute_configs():
    """
    Analyzes new_configs.json and validates configurations.
    
    UPDATES status and operation_status in AUTHOR_PATH based on processing results.
    status = 'pending' if no errors, 'aborted' if any errors encountered.
    operation_status contains professional message explaining any issues.
    
    MOVES any config with status='pending' from NEW_CONFIGS to AUTHOR_PATH.
    Updates status for all other configs based on their validation results.
    
    Only keeps ONE config in AUTHOR_PATH at a time (replaces existing).
    
    When moving config to AUTHOR_PATH, extracts the time_order_type key and adds
    a new 'time_order' field with that key value.
    
    Before flattening, saves dynamic field names to dynamic_fields.txt in DEFAULT_PATH.
    """
    import os
    import json
    import re
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        return default if default is not None else {}
                    return json.loads(content)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def save_text_file(file_path, data):
        """Save text file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            # Check if the config is a list or dict
            is_list = isinstance(author_data, list)
            
            if is_list:
                # It's a list - work with the list
                if not author_data:
                    author_data = [{}]
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                # It's a dict - work with the dict directly
                if not isinstance(author_data, dict):
                    author_data = {}
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def extract_fields_from_config(config):
        """Extract all needed fields from a config for validation"""
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            data = config['dynamic_values']
        else:
            data = config
        
        account_url = data.get('account_url', '')
        captions = data.get('author_caption', '') or data.get('author_captions', '')
        jpgs = data.get('Jpgsurl', '') or data.get('jpgsurl', '')
        time_order = data.get('time_order_type', '') or data.get('time_order', '')
        
        return account_url, captions, jpgs, time_order
    
    def parse_account_url_field(account_url_field):
        """Parse account_url field to check if it has valid data"""
        if not account_url_field:
            return None, None
        
        if isinstance(account_url_field, dict):
            for key, value in account_url_field.items():
                return key, value
        
        if isinstance(account_url_field, str) and not account_url_field.strip().startswith('{'):
            return account_url_field, None
        
        try:
            parsed = json.loads(account_url_field)
            if isinstance(parsed, dict):
                for key, value in parsed.items():
                    return key, value
        except:
            pass
        
        return None, None
    
    def parse_captions_field(captions_field):
        """Parse captions field to check if it has valid data"""
        if not captions_field:
            return []
        
        if isinstance(captions_field, list):
            return captions_field
        
        if isinstance(captions_field, dict):
            if 'author_caption' in captions_field and isinstance(captions_field['author_caption'], list):
                return captions_field['author_caption']
            if 'author_captions' in captions_field and isinstance(captions_field['author_captions'], list):
                return captions_field['author_captions']
            for value in captions_field.values():
                if isinstance(value, list):
                    return value
            return []
        
        if isinstance(captions_field, str):
            try:
                cleaned = captions_field.replace('\\"', '"')
                parsed = json.loads(cleaned)
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict):
                    if 'author_caption' in parsed and isinstance(parsed['author_caption'], list):
                        return parsed['author_caption']
                    elif 'author_captions' in parsed and isinstance(parsed['author_captions'], list):
                        return parsed['author_captions']
            except:
                try:
                    cleaned = captions_field.replace('"[', '[').replace(']"', ']')
                    parsed = json.loads(cleaned)
                    if isinstance(parsed, list):
                        return parsed
                except:
                    pass
        
        return []
    
    def parse_jpgs_field(jpgs_field):
        """Parse JPGs field to check if it has valid data"""
        if not jpgs_field:
            return None, []
        
        if isinstance(jpgs_field, dict):
            for key, value in jpgs_field.items():
                if isinstance(value, str):
                    urls = [u.strip() for u in value.split(',') if u.strip()]
                    return key, urls
                elif isinstance(value, list):
                    return key, value
        
        if isinstance(jpgs_field, str):
            try:
                parsed = json.loads(jpgs_field)
                if isinstance(parsed, dict):
                    for key, value in parsed.items():
                        if isinstance(value, str):
                            urls = [u.strip() for u in value.split(',') if u.strip()]
                            return key, urls
                        elif isinstance(value, list):
                            return key, value
            except:
                match = re.search(r'{"([^"]+)":"([^"]+)"', jpgs_field)
                if match:
                    username = match.group(1)
                    url_string = match.group(2)
                    urls = [u.strip() for u in url_string.split(',') if u.strip()]
                    return username, urls
        
        return None, []
    
    def parse_time_order_field(time_order_field):
        """Parse time_order field to check if it has valid data"""
        if not time_order_field:
            return {}
        
        if isinstance(time_order_field, dict):
            return time_order_field
        
        if isinstance(time_order_field, str):
            try:
                cleaned = time_order_field.replace('\\"', '"')
                parsed = json.loads(cleaned)
                if isinstance(parsed, dict):
                    return parsed
            except:
                pass
        
        return {}
    
    def extract_time_order_key(time_order_field):
        """Extract the first key from time_order_type field"""
        if not time_order_field:
            return None
        
        time_orders = parse_time_order_field(time_order_field)
        if time_orders and isinstance(time_orders, dict):
            for key in time_orders.keys():
                return key
        
        return None
    
    def flatten_config(config):
        """Flatten a config by removing dynamic_values wrapper"""
        flattened = {}
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            if 'status' in config:
                flattened['status'] = config['status']
            if 'operation_status' in config:
                flattened['operation_status'] = config['operation_status']
            for key, value in config['dynamic_values'].items():
                flattened[key] = value
        else:
            for key, value in config.items():
                flattened[key] = value
        return flattened
    
    def extract_dynamic_field_names(config):
        """Extract field names from dynamic_values wrapper"""
        field_names = []
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            for key in config['dynamic_values'].keys():
                field_names.append(key)
        return field_names
    
    # ============================================================
    # STEP 1: LOAD CONFIGURATIONS
    # ============================================================
    print(f"\n{'='*60}")
    print("📁 Loading configurations...")
    print(f"{'='*60}")
    
    configs = load_json_file(NEW_CONFIGS, [])
    if not configs:
        error_msg = "analyze_and_distribute_configs: The configuration file is empty or contains invalid data."
        print(f"❌ {error_msg}")
        update_author_status('aborted', error_msg)
        return False
    
    if not isinstance(configs, list):
        configs = [configs]
    
    print(f"✅ Loaded {len(configs)} configurations")
    
    # ============================================================
    # STEP 1.5: EXTRACT AND SAVE DYNAMIC FIELD NAMES
    # ============================================================
    print(f"\n{'='*60}")
    print("📝 Extracting dynamic field names...")
    print(f"{'='*60}")
    
    all_dynamic_fields = set()
    for config in configs:
        if isinstance(config, dict):
            field_names = extract_dynamic_field_names(config)
            all_dynamic_fields.update(field_names)
    
    if all_dynamic_fields:
        # Sort for consistency
        sorted_fields = sorted(all_dynamic_fields)
        dynamic_fields_text = '\n'.join(sorted_fields)
        
        # Save to DEFAULT_PATH using global constant
        dynamic_fields_path = os.path.join(DEFAULT_PATH, "dynamic_fields.txt")
        
        if save_text_file(dynamic_fields_path, dynamic_fields_text):
            print(f"✅ Dynamic field names saved to: {dynamic_fields_path}")
            print(f"   Fields: {len(sorted_fields)}")
            for field in sorted_fields:
                print(f"   - {field}")
        else:
            print(f"⚠️ Failed to save dynamic field names to: {dynamic_fields_path}")
    else:
        print("ℹ️ No dynamic_values found in configurations")
    
    # Initialize tracking variables
    errors_encountered = []
    warnings_encountered = []
    processed_count = 0
    failed_count = 0
    pending_count = 0
    updated_configs = []
    
    # Track pending config
    pending_config_index = None
    pending_config = None
    pending_time_order_key = None
    
    # ============================================================
    # STEP 2: VALIDATE EACH CONFIGURATION
    # ============================================================
    for idx, config in enumerate(configs):
        print(f"\n📝 Validating config {idx + 1}/{len(configs)}")
        
        config_status = None
        if isinstance(config, dict):
            if 'status' in config:
                config_status = config.get('status')
            elif 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                config_status = config['dynamic_values'].get('status')
        
        print(f"📌 Current status: {config_status}")
        
        try:
            # Extract fields from config
            account_url_field, captions_field, jpgs_field, time_order_field = extract_fields_from_config(config)
            
            print(f"📌 Account URL field: {'Present' if account_url_field else 'None'}")
            print(f"📌 Captions field: {'Present' if captions_field else 'None'}")
            print(f"📌 JPGs field: {'Present' if jpgs_field else 'None'}")
            print(f"📌 Time order field: {'Present' if time_order_field else 'None'}")
            
            # ============================================================
            # VALIDATE CONFIG FIELDS - CHECK IF VALUES EXIST AND ARE VALID
            # ============================================================
            config_has_issues = False
            issue_messages = []
            
            # Validate account_url
            account_key, account_url_value = parse_account_url_field(account_url_field)
            if not account_key:
                issue_messages.append("Account URL field is missing or empty. A valid account URL is required.")
                config_has_issues = True
            elif not account_url_value:
                issue_messages.append(f"Account URL for '{account_key}' exists but has no value. A valid URL is required.")
                config_has_issues = True
            
            # Validate captions
            if not captions_field:
                issue_messages.append("Captions field is missing or empty. At least one caption is required.")
                config_has_issues = True
            else:
                captions_list = parse_captions_field(captions_field)
                if not captions_list:
                    issue_messages.append("Captions field exists but could not be parsed or is empty. At least one valid caption is required.")
                    config_has_issues = True
            
            # Validate JPGs
            if not jpgs_field:
                issue_messages.append("JPGs URL field is missing or empty. At least one image URL is required.")
                config_has_issues = True
            else:
                jpgs_username, jpgs_urls = parse_jpgs_field(jpgs_field)
                if not jpgs_username or not jpgs_urls:
                    issue_messages.append("JPGs URL field exists but could not be parsed or is empty. At least one valid image URL is required.")
                    config_has_issues = True
            
            # Validate time order
            if not time_order_field:
                issue_messages.append("Time order field is missing or empty. A schedule type is required.")
                config_has_issues = True
            else:
                time_orders = parse_time_order_field(time_order_field)
                if not time_orders:
                    issue_messages.append("Time order field exists but could not be parsed or is empty. A valid schedule type is required.")
                    config_has_issues = True
            
            # ============================================================
            # UPDATE STATUS BASED ON VALIDATION RESULTS
            # ============================================================
            if config_has_issues:
                new_status = 'aborted'
                status_message = f"analyze_and_distribute_configs: Configuration validation failed. Issues: {'; '.join(issue_messages)}"
                
                if 'status' in config:
                    config['status'] = new_status
                    config['operation_status'] = status_message
                elif 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                    config['dynamic_values']['status'] = new_status
                    config['dynamic_values']['operation_status'] = status_message
                
                failed_count += 1
                print(f"❌ Config {idx + 1} has validation issues - status set to 'aborted'")
                for msg in issue_messages:
                    print(f"   - {msg}")
                
                if pending_config_index == idx:
                    pending_config = None
                    pending_config_index = None
                    pending_time_order_key = None
            else:
                new_status = 'pending'
                status_message = "analyze_and_distribute_configs: Configuration validated successfully. All required fields are present and valid."
                
                if 'status' in config:
                    config['status'] = new_status
                    config['operation_status'] = status_message
                elif 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                    config['dynamic_values']['status'] = new_status
                    config['dynamic_values']['operation_status'] = status_message
                
                pending_count += 1
                print(f"✅ Config {idx + 1} passed validation - status set to 'pending'")
                
                if pending_config is None and config_status != 'pending':
                    pending_config_index = idx
                    pending_config = config
                    pending_time_order_key = extract_time_order_key(time_order_field)
                    print(f"📌 Config {idx + 1} marked as pending for moving")
                    if pending_time_order_key:
                        print(f"📌 Time order key extracted: {pending_time_order_key}")
            
            # Flatten the config for saving
            flattened_config = flatten_config(config)
            updated_configs.append(flattened_config)
            processed_count += 1
            print(f"✅ Config {idx + 1} validated and flattened")
            
        except Exception as e:
            error_msg = f"Config {idx + 1}: Unexpected error during validation: {str(e)}"
            print(f"❌ {error_msg}")
            errors_encountered.append(error_msg)
            
            if 'status' in config:
                config['status'] = 'aborted'
                config['operation_status'] = f"analyze_and_distribute_configs: Critical validation error: {str(e)}"
            elif 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                config['dynamic_values']['status'] = 'aborted'
                config['dynamic_values']['operation_status'] = f"analyze_and_distribute_configs: Critical validation error: {str(e)}"
            
            if pending_config_index == idx:
                pending_config = None
                pending_config_index = None
                pending_time_order_key = None
            
            failed_count += 1
    
    # ============================================================
    # STEP 3: SAVE UPDATED CONFIGS WITH STATUSES
    # ============================================================
    print(f"\n{'='*60}")
    print("💾 Saving updated configurations...")
    print(f"{'='*60}")
    
    save_errors = []
    
    if not save_json_file(NEW_CONFIGS, updated_configs):
        error_msg = "analyze_and_distribute_configs: Failed to save updated configurations to NEW_CONFIGS."
        print(f"❌ {error_msg}")
        save_errors.append(error_msg)
    else:
        print(f"✅ Updated configs saved to: {NEW_CONFIGS}")
    
    # ============================================================
    # STEP 4: FIND AND MOVE PENDING CONFIG TO AUTHOR_PATH
    # ============================================================
    print(f"\n{'='*60}")
    print("📦 Finding and moving 'pending' config to AUTHOR_PATH...")
    print(f"{'='*60}")
    
    try:
        current_configs = load_json_file(NEW_CONFIGS, [])
        
        if isinstance(current_configs, list) and len(current_configs) > 0:
            pending_index = None
            pending_config = None
            pending_time_key = None
            
            for i, config in enumerate(current_configs):
                config_status = None
                if isinstance(config, dict):
                    if 'status' in config:
                        config_status = config.get('status')
                    elif 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                        config_status = config['dynamic_values'].get('status')
                    
                    if config_status == 'pending':
                        pending_index = i
                        pending_config = config
                        
                        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                            time_order_field = config['dynamic_values'].get('time_order_type', '')
                        else:
                            time_order_field = config.get('time_order_type', '')
                        pending_time_key = extract_time_order_key(time_order_field)
                        break
            
            if pending_config is not None:
                print(f"📌 Found pending config at index {pending_index + 1}")
                
                # Copy the entire config as-is - DO NOT REMOVE ANY FIELDS
                config_to_move = json.loads(json.dumps(pending_config))
                
                # Add time_order field if we have the key
                if pending_time_key:
                    print(f"   - Adding 'time_order' field with value: {pending_time_key}")
                    config_to_move['time_order'] = pending_time_key
                    print(f"   - Added 'time_order' to root level")
                else:
                    print(f"   ⚠️ No time_order_key found - skipping 'time_order' field addition")
                    warnings_encountered.append("Pending config did not have a time_order_type key to extract")
                
                # Save the ENTIRE config to AUTHOR_PATH (preserving ALL fields)
                print(f"   - Saving config to AUTHOR_PATH (preserving all fields)")
                
                if not save_json_file(AUTHOR_PATH, config_to_move):
                    error_msg = f"analyze_and_distribute_configs: Failed to save config to AUTHOR_PATH."
                    print(f"❌ {error_msg}")
                    save_errors.append(error_msg)
                else:
                    print(f"✅ Pending config moved to AUTHOR_PATH (replaced existing)")
                    if pending_time_key:
                        print(f"   - Added 'time_order' field: {pending_time_key}")
                    
                    # Remove pending config from NEW_CONFIGS
                    remaining_configs = current_configs[:pending_index] + current_configs[pending_index + 1:]
                    if not save_json_file(NEW_CONFIGS, remaining_configs):
                        error_msg = "analyze_and_distribute_configs: Failed to update NEW_CONFIGS after removing pending config."
                        print(f"❌ {error_msg}")
                        save_errors.append(error_msg)
                    else:
                        print(f"✅ Removed pending config from NEW_CONFIGS")
                        print(f"   - Remaining configs: {len(remaining_configs)}")
            else:
                print("ℹ️ No 'pending' config found to move")
                
                config_statuses = []
                for config in current_configs:
                    if isinstance(config, dict):
                        if 'status' in config:
                            config_statuses.append(config.get('status', 'no status'))
                        elif 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                            config_statuses.append(config['dynamic_values'].get('status', 'no status'))
                        else:
                            config_statuses.append('no status')
                
                if config_statuses:
                    unique_statuses = set(config_statuses)
                    print(f"   - Available statuses: {', '.join(unique_statuses)}")
        else:
            print("ℹ️ No configs to move (NEW_CONFIGS is empty or invalid)")
    except Exception as e:
        error_msg = f"analyze_and_distribute_configs: Error moving pending config: {str(e)}"
        print(f"❌ {error_msg}")
        save_errors.append(error_msg)
    
    # ============================================================
    # STEP 5: UPDATE AUTHOR_PATH STATUS
    # ============================================================
    all_errors = errors_encountered + save_errors
    
    detailed_issues = []
    
    if errors_encountered:
        detailed_issues.append(f"Critical Errors ({len(errors_encountered)}): " + "; ".join(errors_encountered[:3]))
        if len(errors_encountered) > 3:
            detailed_issues.append(f"... and {len(errors_encountered) - 3} more errors")
    
    if warnings_encountered:
        detailed_issues.append(f"Warnings ({len(warnings_encountered)}): " + "; ".join(warnings_encountered[:3]))
        if len(warnings_encountered) > 3:
            detailed_issues.append(f"... and {len(warnings_encountered) - 3} more warnings")
    
    if save_errors and save_errors not in errors_encountered:
        detailed_issues.append(f"Save Errors ({len(save_errors)}): " + "; ".join(save_errors))
    
    if all_errors or failed_count > 0:
        status_value = 'aborted'
        
        error_summary = []
        if errors_encountered:
            error_summary.append(f"{len(errors_encountered)} critical validation errors")
        if save_errors:
            error_summary.append(f"{len(save_errors)} file save errors")
        if warnings_encountered:
            error_summary.append(f"{len(warnings_encountered)} warnings")
        if failed_count > 0:
            error_summary.append(f"{failed_count} configurations failed validation")
        
        operation_msg = f"analyze_and_distribute_configs: Configuration validation encountered issues. Summary: {', '.join(error_summary)}. Details: {'. '.join(detailed_issues)}."
        
        print(f"\n⚠️ Setting status to 'aborted'")
        update_author_status(status_value, operation_msg)
    else:
        status_value = 'pending'
        
        if warnings_encountered:
            operation_msg = f"analyze_and_distribute_configs: Configuration validation completed successfully with {len(warnings_encountered)} warnings. Warnings: " + "; ".join(warnings_encountered)
        else:
            operation_msg = f"analyze_and_distribute_configs: Configuration validation completed successfully. Validated {processed_count} configurations."
        
        print(f"\n✅ Setting status to 'pending'")
        update_author_status(status_value, operation_msg)
    
    # ============================================================
    # SUMMARY
    # ============================================================
    print(f"\n{'='*60}")
    print("✅ ANALYZER COMPLETED!")
    print(f"\n📊 Summary:")
    print(f"  - Validated configurations: {processed_count} successful, {failed_count} failed")
    print(f"  - Configurations set to pending: {pending_count}")
    print(f"  - Status set to: {status_value}")
    
    if warnings_encountered:
        print(f"\n⚠️ WARNINGS ({len(warnings_encountered)}):")
        for warning in warnings_encountered[:5]:
            print(f"    - {warning}")
        if len(warnings_encountered) > 5:
            print(f"    ... and {len(warnings_encountered) - 5} more warnings")
    
    if all_errors:
        print(f"\n❌ ERRORS ({len(all_errors)}):")
        for error in all_errors[:5]:
            print(f"    - {error}")
        if len(all_errors) > 5:
            print(f"    ... and {len(all_errors) - 5} more errors")
    
    print(f"{'='*60}\n")
    
    return len(all_errors) == 0

def fetch_settings():
    """
    Launches/uses Microsoft Edge for phpMyAdmin operations.
    Gets settings from serenum_config and saves to panel.json.
    Uses clipboard-based communication only.
    Dynamically finds phpMyAdmin URL by searching for "phpmysqlkdkw.php" in any key/value.
    Falls back to PHPSQLURL if not found.
    Creates default files if they don't exist or are invalid.
    Closes the Edge window upon successful completion.
    
    UPDATES status and operation_status in AUTHOR_PATH based on processing results.
    status = 'pending' if no errors, 'aborted' if any errors encountered.
    operation_status contains professional message explaining any issues.
    """
    pyautogui.PAUSE = 0.0
    
    # Define termination flag
    terminate_automation = False
    
    # Define MAX_RETRIES for operations
    MAX_OPERATION_RETRIES = 5
    
    def check_for_termination():
        if terminate_automation:
            raise KeyboardInterrupt("User forced exit via shortcut key.")
    
    # Helper functions for status updates
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        return default if default is not None else []
                    return json.loads(content)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError as e:
            return default if default is not None else {}
        except Exception as e:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                # Update the last entry (most recently added)
                author_data[-1]['status'] = status_value
                author_data[-1]['operation_status'] = operation_message
                
                if save_json_file(AUTHOR_PATH, author_data):
                    return True
            return False
        except Exception as e:
            return False
    
    def update_all_configs_status(status_value, operation_message):
        """Update status and operation_status for ALL configs in NEW_CONFIGS"""
        try:
            configs = load_json_file(NEW_CONFIGS, [])
            if not isinstance(configs, list):
                configs = [configs] if configs else []
            
            updated = False
            for config in configs:
                if isinstance(config, dict):
                    # Update status in the config
                    if 'status' in config:
                        config['status'] = status_value
                        config['operation_status'] = operation_message
                        updated = True
                    elif 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                        config['dynamic_values']['status'] = status_value
                        config['dynamic_values']['operation_status'] = operation_message
                        updated = True
            
            if updated:
                return save_json_file(NEW_CONFIGS, configs)
            return False
        except Exception as e:
            return False
    
    def ensure_new_configs_exists():
        """Create default NEW_CONFIGS file if it doesn't exist or is invalid."""
        if os.path.exists(NEW_CONFIGS):
            try:
                with open(NEW_CONFIGS, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if not content:
                        return False
                    json.loads(content)
                return True
            except Exception as e:
                try:
                    os.remove(NEW_CONFIGS)
                except:
                    pass
        else:
            pass
        
        default_config = {
            "url": "https://fhdrikxsirudr.fwh.is/phpmysqlkdkw.php",
            "author": "Brilliance",
            "engine": "csv",
            "page": "none",
            "group": "include",
            "processjpgfrom": "freshjpgs"
        }
        
        try:
            os.makedirs(os.path.dirname(NEW_CONFIGS), exist_ok=True)
            with open(NEW_CONFIGS, 'w', encoding='utf-8') as file:
                json.dump(default_config, file, indent=2, ensure_ascii=False, separators=(',', ': '))
            return True
        except Exception as e:
            return False
    
    def get_current_monitor():
        try:
            cursor_pos = win32api.GetCursorPos()
            monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint(cursor_pos))
            return monitor_info['Monitor']
        except Exception:
            return (0, 0, win32api.GetSystemMetrics(win32con.SM_CXSCREEN), 
                   win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
    
    def get_edge_window_on_monitor(monitor_bounds):
        monitor_left, monitor_top, monitor_right, monitor_bottom = monitor_bounds
        edge_windows = []
        edge_process_names = ["msedge.exe"]
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process = psutil.Process(pid)
                    if process.name().lower() in edge_process_names:
                        rect = win32gui.GetWindowRect(hwnd)
                        left, top, right, bottom = rect
                        width, height = right - left, bottom - top
                        if width > 200 and height > 200:
                            window_center_x = (left + right) / 2
                            window_center_y = (top + bottom) / 2
                            is_on_current_monitor = (
                                monitor_left <= window_center_x <= monitor_right and
                                monitor_top <= window_center_y <= monitor_bottom
                            )
                            if is_on_current_monitor:
                                windows.append({'hwnd': hwnd, 'width': width, 'height': height})
                except Exception:
                    pass
            return True
        
        win32gui.EnumWindows(enum_windows_callback, edge_windows)
        edge_windows.sort(key=lambda w: w['width'] * w['height'], reverse=True)
        return edge_windows
    
    def close_edge_window(hwnd):
        """Close the Edge window gracefully."""
        try:
            if win32gui.IsWindow(hwnd):
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                time.sleep(0.5)
                
                if win32gui.IsWindow(hwnd):
                    win32gui.DestroyWindow(hwnd)
                    time.sleep(0.3)
                
                return True
            else:
                return False
        except Exception as e:
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                if process.name().lower() == "msedge.exe":
                    process.terminate()
                    time.sleep(0.5)
                    return True
            except:
                pass
            return False
    
    def ensure_edge_window_ready():
        """Ensure Edge window exists and is maximized/focused"""
        check_for_termination()
        
        current_monitor = get_current_monitor()
        print(f"🖥️ [WATCHDOG] Monitor bounds: {current_monitor}")
        
        edge_windows = get_edge_window_on_monitor(current_monitor)
        
        if edge_windows:
            hwnd = edge_windows[0]['hwnd']
            print(f"🪟 [WATCHDOG] Found existing Edge window handle: {hwnd}")
            
            try:
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.3)
                
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                time.sleep(0.5)
                
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                except Exception as e:
                    try:
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.3)
                    except:
                        pass
                
                return hwnd
            except Exception as e:
                return hwnd
        
        subprocess.Popen([edge_path, "about:blank"])
        
        for attempt in range(20):
            check_for_termination()
            time.sleep(0.5)
            edge_windows = get_edge_window_on_monitor(current_monitor)
            if edge_windows:
                hwnd = edge_windows[0]['hwnd']
                
                try:
                    if win32gui.IsIconic(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        time.sleep(0.3)
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    time.sleep(0.5)
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                        time.sleep(0.2)
                    except:
                        pass
                    return hwnd
                except Exception as e:
                    continue
        
        raise RuntimeError("Failed to get or launch Edge window")
    
    def enforce_window_focus(hwnd):
        """Enforce window focus and maximized state"""
        check_for_termination()
        try:
            if not win32gui.IsWindow(hwnd):
                return ensure_edge_window_ready()
            
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.3)
            
            current_foreground = win32gui.GetForegroundWindow()
            if current_foreground != hwnd:
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.15)
                except Exception as e:
                    try:
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.3)
                    except:
                        pass
            
            try:
                placement = win32gui.GetWindowPlacement(hwnd)
                if placement[1] != win32con.SW_SHOWMAXIMIZED:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    time.sleep(0.3)
            except Exception as e:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    time.sleep(0.3)
                except:
                    pass
            
            return hwnd
        except Exception as e:
            return hwnd
    
    def ensure_window_ready_and_focused():
        """Get or create window and ensure it's ready"""
        check_for_termination()
        hwnd = ensure_edge_window_ready()
        return enforce_window_focus(hwnd)
    
    def fast_paste_url(hwnd, url, retry_count=0):
        """Fast paste URL with watchdog and retry"""
        check_for_termination()
        print(f"📋 Pasting URL: {url}")
        pyperclip.copy(url)
        
        try:
            hwnd = enforce_window_focus(hwnd)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.1)
            hwnd = enforce_window_focus(hwnd)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            return True, hwnd
        except Exception as e:
            if retry_count < 3:
                time.sleep(0.5)
                hwnd = ensure_window_ready_and_focused()
                return fast_paste_url(hwnd, url, retry_count + 1)
            else:
                return False, hwnd
    
    def wait_for_clipboard_content(expected_contains=None, timeout=60, check_interval=0.5):
        """Wait for clipboard to contain expected content or have any content."""
        check_for_termination()
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            check_for_termination()
            try:
                current_content = pyperclip.paste()
                if current_content and current_content.strip():
                    if expected_contains:
                        if expected_contains in current_content:
                            return current_content
                    else:
                        return current_content
            except Exception as e:
                pass
            
            time.sleep(check_interval)
        
        return None
    
    def wait_for_enter_confirmation(timeout=5, check_interval=0.3):
        """Wait for 'enter button activated' in clipboard."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            check_for_termination()
            try:
                current_content = pyperclip.paste()
                if current_content and "enter button activated" in current_content:
                    return True
            except Exception as e:
                pass
            
            time.sleep(check_interval)
        
        return False
    
    def create_backup_file(file_path):
        backup_path = file_path + ".backup"
        if os.path.exists(file_path):
            shutil.copy2(file_path, backup_path)
            return backup_path
        return None
    
    def restore_from_backup(file_path):
        backup_path = file_path + ".backup"
        if os.path.exists(backup_path):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                shutil.copy2(backup_path, file_path)
                os.remove(backup_path)
                return True
            except Exception as e:
                return False
        return False
    
    def wait_for_clipboard_data_with_retry(max_retries=15, retry_delay=1.0, min_content_length=10, hwnd=None):
        """Wait for clipboard content with retries."""
        print(f"⏳ [CLIPBOARD] Waiting for data with {max_retries} retries...")
        
        previous_content = None
        enter_confirmation_seen = False
        
        for attempt in range(max_retries):
            check_for_termination()
            
            try:
                current_content = pyperclip.paste()
                
                if current_content and current_content.strip():
                    content_length = len(current_content.strip())
                    
                    if "enter button activated" in current_content:
                        if not enter_confirmation_seen:
                            print(f"ℹ️ [CLIPBOARD] Enter confirmation received, waiting for actual data...")
                            enter_confirmation_seen = True
                        previous_content = current_content
                        time.sleep(retry_delay)
                        continue
                    
                    if current_content != previous_content:
                        print(f"📋 [CLIPBOARD] Attempt {attempt + 1}/{max_retries}: New content found ({content_length} chars)")
                        
                        if content_length > min_content_length:
                            return current_content
                        else:
                            print(f"⚠️ [CLIPBOARD] Content too short ({content_length} chars), waiting...")
                    else:
                        print(f"⏳ [CLIPBOARD] Attempt {attempt + 1}/{max_retries}: No new content")
                else:
                    print(f"⏳ [CLIPBOARD] Attempt {attempt + 1}/{max_retries}: Empty clipboard")
                
                previous_content = current_content
                
            except Exception as e:
                print(f"⚠️ [CLIPBOARD] Error reading: {e}")
            
            if attempt > 0 and attempt % 5 == 0 and hwnd:
                try:
                    hwnd = enforce_window_focus(hwnd)
                except:
                    pass
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        
        return None
    
    def overwrite_file_with_content(file_path, content):
        try:
            try:
                parsed_content = json.loads(content)
                content = json.dumps(parsed_content, indent=2, ensure_ascii=False, separators=(',', ': '))
            except:
                pass
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False
    
    def execute_sql_query_and_save(hwnd, sql_query, file_path, operation_description, retry_count=0):
        """Execute SQL query on current page and save results to file."""
        try:
            print(f"\n{'='*60}")
            print(f"🚀 [OPERATION] {operation_description} (Attempt {retry_count + 1}/{MAX_OPERATION_RETRIES})")
            print(f"📝 [SQL] {sql_query}")
            print(f"💾 [OUTPUT] {file_path}")
            print(f"{'='*60}")
            
            print("⌨️ [STEP 1] Ensuring window focus and maximized state...")
            hwnd = enforce_window_focus(hwnd)
            time.sleep(0.2)
            
            print("⌨️ [STEP 2] Pressing Tab to focus textarea...")
            hwnd = enforce_window_focus(hwnd)
            pyautogui.press('tab')
            time.sleep(0.5)
            
            print("⌨️ [STEP 3] Ctrl+A to select all text...")
            hwnd = enforce_window_focus(hwnd)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            
            print("⌨️ [STEP 4] Deleting text...")
            pyautogui.press('delete')
            time.sleep(0.3)
            
            print(f"⌨️ [STEP 5] Typing SQL query: {sql_query}")
            hwnd = enforce_window_focus(hwnd)
            pyperclip.copy(sql_query)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            print("⌨️ [STEP 6] Pressing Enter to execute query...")
            hwnd = enforce_window_focus(hwnd)
            pyautogui.press('enter')
            
            enter_confirmed = wait_for_enter_confirmation(timeout=5)
            if enter_confirmed:
                print("✅ [STEP 6] Enter confirmed")
            else:
                print("⚠️ [STEP 6] Enter not confirmed, but proceeding")
            
            print("⏳ [STEP 7] Waiting for query execution...")
            time.sleep(1.5)
            
            print("⌨️ [STEP 8] Pressing Ctrl+M to copy results...")
            hwnd = enforce_window_focus(hwnd)
            pyautogui.hotkey('ctrl', 'm')
            time.sleep(0.5)
            
            print("⏳ [STEP 9] Waiting for clipboard data...")
            
            backup_created = create_backup_file(file_path)
            
            final_result = wait_for_clipboard_data_with_retry(
                max_retries=20, 
                retry_delay=1.0,
                min_content_length=20,
                hwnd=hwnd
            )
            
            if not final_result:
                error_msg = f"SQL query '{sql_query}' executed but no data was returned or the clipboard was empty after {20} retry attempts."
                print(f"❌ {error_msg}")
                
                if retry_count < MAX_OPERATION_RETRIES - 1:
                    print(f"🔄 [RETRY] Operation failed, retrying in 2 seconds...")
                    time.sleep(2)
                    hwnd = enforce_window_focus(hwnd)
                    return execute_sql_query_and_save(
                        hwnd, sql_query, file_path, 
                        operation_description, retry_count + 1
                    )
                
                if backup_created and os.path.exists(file_path + ".backup"):
                    restore_from_backup(file_path)
                return False, error_msg
            
            print(f"✅ [STEP 9] Data received successfully: {len(final_result)} characters")
            
            print(f"💾 [STEP 10] Overwriting file {file_path} with data...")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if overwrite_file_with_content(file_path, final_result):
                print("✅ [STEP 10] File overwritten successfully!")
                backup_path = file_path + ".backup"
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                return True, None
            else:
                error_msg = f"Failed to write data to {file_path}. Check file permissions and disk space."
                print(f"❌ {error_msg}")
                
                if retry_count < MAX_OPERATION_RETRIES - 1:
                    print(f"🔄 [RETRY] File save failed, retrying in 2 seconds...")
                    time.sleep(2)
                    hwnd = enforce_window_focus(hwnd)
                    return execute_sql_query_and_save(
                        hwnd, sql_query, file_path, 
                        operation_description, retry_count + 1
                    )
                
                if backup_created and os.path.exists(file_path + ".backup"):
                    restore_from_backup(file_path)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Unexpected error during SQL execution: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            
            if retry_count < MAX_OPERATION_RETRIES - 1:
                print(f"🔄 [RETRY] Exception occurred, retrying in 2 seconds...")
                time.sleep(2)
                try:
                    hwnd = ensure_window_ready_and_focused()
                    return execute_sql_query_and_save(
                        hwnd, sql_query, file_path, 
                        operation_description, retry_count + 1
                    )
                except:
                    pass
            
            try:
                backup_path = file_path + ".backup"
                if os.path.exists(backup_path):
                    restore_from_backup(file_path)
            except:
                pass
            return False, error_msg
    
    # ============================================================
    # MAIN EXECUTION
    # ============================================================
    try:
        # Track errors and warnings with detailed messages
        errors_encountered = []
        warnings_encountered = []
        detailed_issues = []
        operation_success = True
        
        # Step 1: Validate config file
        if not ensure_new_configs_exists():
            error_msg = "The configuration file could not be created or validated. Please check file permissions and disk space."
            print(f"❌ {error_msg}")
            errors_encountered.append(error_msg)
            
            # Update status for all configs
            status_msg = f"fetch_settings: {error_msg}"
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
            return False
        
        # Step 2: Load panel data
        try:
            with open(NEW_CONFIGS, 'r', encoding='utf-8') as file:
                panel_data = json.load(file)
        except json.JSONDecodeError as e:
            error_msg = f"The configuration file contains invalid JSON: {str(e)}. Please check the file format."
            print(f"❌ {error_msg}")
            errors_encountered.append(error_msg)
            
            status_msg = f"fetch_settings: {error_msg}"
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
            return False
        except Exception as e:
            error_msg = f"Failed to read the configuration file: {str(e)}. Check file permissions."
            print(f"❌ {error_msg}")
            errors_encountered.append(error_msg)
            
            status_msg = f"fetch_settings: {error_msg}"
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
            return False
        
        # Step 3: Find phpMyAdmin URL
        phpmyadmin_url = None
        
        def search_for_phpmyadmin(data, path=""):
            nonlocal phpmyadmin_url
            if phpmyadmin_url:
                return
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    if isinstance(value, str) and "phpmysqlkdkw.php" in value:
                        phpmyadmin_url = value
                        print(f"🔍 [PHPMYADMIN] Found template reference in: {current_path}")
                        print(f"🔍 [PHPMYADMIN] URL: {phpmyadmin_url}")
                        return
                    if isinstance(value, (dict, list)):
                        search_for_phpmyadmin(value, current_path)
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    current_path = f"{path}[{index}]"
                    if isinstance(item, (dict, list)):
                        search_for_phpmyadmin(item, current_path)
        
        search_for_phpmyadmin(panel_data)
        
        if not phpmyadmin_url:
            warning_msg = "The 'phpmysqlkdkw.php' URL was not found in the configuration file. Using the fallback URL from PHPSQLURL."
            print(f"⚠️ {warning_msg}")
            warnings_encountered.append(warning_msg)
            phpmyadmin_url = PHPSQLURL
        else:
            print(f"🔍 [PHPMYADMIN] Using found URL: {phpmyadmin_url}")
        
        # Step 4: Get or create Edge window
        try:
            hwnd = ensure_window_ready_and_focused()
        except Exception as e:
            error_msg = f"Failed to launch or focus Microsoft Edge: {str(e)}. Check if Edge is installed and accessible."
            print(f"❌ {error_msg}")
            errors_encountered.append(error_msg)
            
            status_msg = f"fetch_settings: {error_msg}"
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
            return False
        
        # Step 5: Navigate to phpMyAdmin URL
        success, hwnd = fast_paste_url(hwnd, phpmyadmin_url)
        if not success:
            error_msg = f"Failed to navigate to '{phpmyadmin_url}'. The browser may have issues loading the page."
            print(f"❌ {error_msg}")
            errors_encountered.append(error_msg)
            
            status_msg = f"fetch_settings: {error_msg}"
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
            try:
                close_edge_window(hwnd)
            except:
                pass
            return False
        
        # Step 6: Wait for page to load
        print("⏳ [NAVIGATION] Waiting for page to load...")
        
        page_ready = None
        for attempt in range(MAX_OPERATION_RETRIES):
            hwnd = enforce_window_focus(hwnd)
            
            if attempt > 0:
                print(f"🔄 [NAVIGATION] Reloading page (attempt {attempt + 1})...")
                pyautogui.hotkey('ctrl', 'r')
                time.sleep(2)
                hwnd = enforce_window_focus(hwnd)
            
            page_ready = wait_for_clipboard_content(
                expected_contains="page is ready", 
                timeout=15 if attempt == 0 else 10, 
                check_interval=0.5
            )
            
            if page_ready:
                print(f"✅ [NAVIGATION] Page is ready (attempt {attempt + 1})")
                break
            else:
                print(f"⚠️ [NAVIGATION] Page not ready (attempt {attempt + 1})")
                time.sleep(1)
        
        if not page_ready:
            error_msg = f"The phpMyAdmin page at '{phpmyadmin_url}' failed to load after {MAX_OPERATION_RETRIES} attempts. Check if the URL is accessible and the server is running."
            print(f"❌ {error_msg}")
            errors_encountered.append(error_msg)
            
            status_msg = f"fetch_settings: {error_msg}"
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
            try:
                close_edge_window(hwnd)
            except:
                pass
            return False
        
        print("✅ [NAVIGATION] Page is ready")
        hwnd = enforce_window_focus(hwnd)
        
        # ============================================================
        # OPERATION: Get settings from serenum_config
        # ============================================================
        sql_query = "select settings from serenum_config"
        success, error_msg = execute_sql_query_and_save(
            hwnd, sql_query, NEW_CONFIGS,
            "Fetching settings from serenum_config"
        )
        
        if not success:
            if error_msg:
                errors_encountered.append(error_msg)
            else:
                error_msg = "The SQL query 'select settings from serenum_config' executed but failed to return valid data. Check if the 'serenum_config' table exists and contains data."
                errors_encountered.append(error_msg)
            
            status_msg = f"fetch_settings: {error_msg}"
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
            try:
                close_edge_window(hwnd)
            except:
                pass
            return False
        
        print("✅ [OPERATION] Settings fetched and saved successfully")
        
        # ============================================================
        # CLOSE EDGE WINDOW ON SUCCESS
        # ============================================================
        print(f"\n{'='*60}")
        print("🪟 [CLEANUP] Closing Edge window...")
        close_success = close_edge_window(hwnd)
        if close_success:
            print("✅ [CLEANUP] Edge window closed successfully")
        else:
            warning_msg = "The Edge browser window could not be closed gracefully. It may need to be closed manually."
            print(f"⚠️ {warning_msg}")
            warnings_encountered.append(warning_msg)
        
        # ============================================================
        # UPDATE STATUS IN AUTHOR_PATH WITH DETAILED MESSAGES
        # ============================================================
        # Build detailed operation message
        detailed_issues = []
        
        if errors_encountered:
            detailed_issues.append(f"Critical Errors ({len(errors_encountered)}): " + "; ".join(errors_encountered[:3]))
            if len(errors_encountered) > 3:
                detailed_issues.append(f"... and {len(errors_encountered) - 3} more errors")
        
        if warnings_encountered:
            detailed_issues.append(f"Warnings ({len(warnings_encountered)}): " + "; ".join(warnings_encountered[:3]))
            if len(warnings_encountered) > 3:
                detailed_issues.append(f"... and {len(warnings_encountered) - 3} more warnings")
        
        if errors_encountered:
            # There were errors - set status to 'aborted'
            status_value = 'aborted'
            
            operation_msg = f"fetch_settings: Settings fetch operation encountered issues. Details: {'. '.join(detailed_issues)}. Please resolve these issues and try again."
            
            print(f"\n⚠️ Setting status to 'aborted' with error message")
            update_all_configs_status(status_value, operation_msg)
            update_author_status(status_value, operation_msg)
            
        else:
            # No errors - set status to 'pending'
            status_value = 'pending'
            
            if warnings_encountered:
                operation_msg = f"fetch_settings: Settings fetch completed successfully, but with {len(warnings_encountered)} specific warnings that did not prevent the operation. Warnings: " + "; ".join(warnings_encountered)
            else:
                operation_msg = f"fetch_settings: Settings fetch completed successfully. The settings data has been retrieved from the 'serenum_config' table and saved to the configuration file."
            
            print(f"\n✅ Setting status to 'pending' with success message")
            update_all_configs_status(status_value, operation_msg)
            update_author_status(status_value, operation_msg)
        
        # ============================================================
        # OPERATION COMPLETE
        # ============================================================
        print(f"{'='*60}")
        print("✅ [PHPMYADMIN] OPERATION COMPLETED!")
        print(f"📊 Status set to: {status_value}")
        
        if warnings_encountered:
            print(f"\n⚠️ WARNINGS ({len(warnings_encountered)}):")
            for warning in warnings_encountered[:5]:
                print(f"    - {warning}")
            if len(warnings_encountered) > 5:
                print(f"    ... and {len(warnings_encountered) - 5} more warnings")
        
        if errors_encountered:
            print(f"\n❌ ERRORS ({len(errors_encountered)}):")
            for error in errors_encountered[:5]:
                print(f"    - {error}")
            if len(errors_encountered) > 5:
                print(f"    ... and {len(errors_encountered) - 5} more errors")
        
        print(f"{'='*60}\n")
        
        analyze_and_distribute_configs()
        return len(errors_encountered) == 0
        
    except KeyboardInterrupt:
        print("🛑 [PHPMYADMIN] Operation interrupted by user")
        
        status_msg = "fetch_settings: The settings fetch operation was cancelled by the user. Please restart the process when ready."
        
        try:
            backup_path = NEW_CONFIGS + ".backup"
            if os.path.exists(backup_path):
                restore_from_backup(NEW_CONFIGS)
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
        except:
            pass
        return False
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"❌ [PHPMYADMIN] {error_msg}")
        import traceback
        traceback.print_exc()
        
        status_msg = f"fetch_settings: Unexpected error: {str(e)}. Please check the logs for details."
        
        try:
            backup_path = NEW_CONFIGS + ".backup"
            if os.path.exists(backup_path):
                restore_from_backup(NEW_CONFIGS)
            update_all_configs_status('aborted', status_msg)
            update_author_status('aborted', status_msg)
        except:
            pass
        return False

def updated_config_construction():
    """
    Converts configurations to the proper nested format.
    
    IMPORTANT: 
    - Reads from NEW_CONFIGS (list) and AUTHOR_PATH (single object)
    - Converts all configs to UPDATED_CONFIGS format (list)
    - ALL fields (except status and operation_status) are placed inside dynamic_values nest
    - PRESERVES existing status and operation_status from AUTHOR_PATH at ROOT LEVEL only
    - REMOVES status and operation_status from dynamic_values (they should only be at root)
    - Does NOT override status - keeps whatever status was set by previous operations
    - PER-CONFIG operation_status with detailed messages about what was processed
    - ESCAPES backslashes in JSON strings to ensure valid JSON
    - APPENDS new messages to existing operation_status instead of overwriting
    - NORMALIZES all slashes (/) and backslashes (\) to underscores (_) in operation_status
    - CHECKS dynamic_fields.txt and removes any fields not listed in it from dynamic_values
    
    UPDATES operation_status in AUTHOR_PATH based on processing results.
    Preserves existing status (does not change it).
    operation_status contains professional message explaining any issues.
    """
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError as e:
            print(f"   ⚠️ JSON decode error in {file_path}: {e}")
            return default if default is not None else {}
        except Exception as e:
            print(f"   ⚠️ Error loading {file_path}: {e}")
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting and escape handling"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            return True
        except Exception as e:
            print(f"   ❌ Error saving to {file_path}: {e}")
            return False
    
    def save_text_file(file_path, data):
        """Save text file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data)
            return True
        except Exception:
            return False
    
    def load_dynamic_fields():
        """
        Load dynamic field names from dynamic_fields.txt.
        Returns a set of allowed field names.
        If the file doesn't exist, returns None to indicate all fields are allowed.
        """
        dynamic_fields_path = os.path.join(DEFAULT_PATH, "dynamic_fields.txt")
        
        if not os.path.exists(dynamic_fields_path):
            print(f"   ⚠️ dynamic_fields.txt not found at: {dynamic_fields_path}")
            print(f"   ℹ️ No field filtering will be applied")
            return None
        
        try:
            with open(dynamic_fields_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print(f"   ⚠️ dynamic_fields.txt is empty - no filtering applied")
                    return None
                
                # Split by newline and strip whitespace
                fields = set([line.strip() for line in content.split('\n') if line.strip()])
                print(f"   📋 Loaded {len(fields)} dynamic fields from dynamic_fields.txt")
                return fields
        except Exception as e:
            print(f"   ⚠️ Error reading dynamic_fields.txt: {e}")
            return None
    
    def escape_json_string(value):
        """Properly escape a value for JSON serialization."""
        if isinstance(value, str):
            if '\\' in value and not '\\\\' in value:
                value = value.replace('\\', '\\\\')
            return value
        elif isinstance(value, dict):
            return {k: escape_json_string(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [escape_json_string(item) for item in value]
        else:
            return value
    
    def clean_dynamic_values(dynamic_values, allowed_fields=None):
        """
        Clean dynamic_values by removing status, operation_status, and any fields
        not in allowed_fields (if allowed_fields is provided).
        Returns cleaned dictionary.
        """
        if not isinstance(dynamic_values, dict):
            return dynamic_values
        
        # Create a copy to avoid modifying the original
        cleaned = dynamic_values.copy()
        
        # Remove status and operation_status from dynamic_values
        cleaned.pop('status', None)
        cleaned.pop('operation_status', None)
        
        # If allowed_fields is provided, remove any fields not in the list
        if allowed_fields is not None:
            # Find fields to remove
            fields_to_remove = [key for key in cleaned.keys() if key not in allowed_fields]
            if fields_to_remove:
                print(f"   🗑️ Removing fields not in dynamic_fields.txt: {fields_to_remove}")
                for key in fields_to_remove:
                    cleaned.pop(key, None)
            else:
                print(f"   ✅ All fields are in dynamic_fields.txt")
        
        # Escape any string values to prevent JSON corruption
        cleaned = escape_json_string(cleaned)
        
        return cleaned
    
    def sanitize_for_json(data):
        """Recursively sanitize data for JSON serialization."""
        if isinstance(data, str):
            if '\\' in data:
                data = data.replace('\\', '\\\\')
            return data
        elif isinstance(data, dict):
            return {k: sanitize_for_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [sanitize_for_json(item) for item in data]
        else:
            return data
    
    def normalize_slashes(text):
        """Normalize all slashes (forward and backslashes) to underscores."""
        if not isinstance(text, str):
            return text
        
        text = text.replace('\\', '_')
        text = text.replace('/', '_')
        text = text.replace('\\\\', '_')
        
        return text
    
    def nest_fields_in_dynamic_values(config, existing_status=None, existing_operation_status=None, allowed_fields=None):
        """
        Move all fields (except status and operation_status) into dynamic_values nest.
        PRESERVES existing status if provided.
        REMOVES status and operation_status from dynamic_values.
        REMOVES any fields not in allowed_fields (if provided).
        Sanitizes all string values to ensure valid JSON.
        """
        if not isinstance(config, dict):
            return config
        
        nested_config = {}
        
        # PRESERVE existing status at ROOT LEVEL ONLY
        if existing_status is not None:
            nested_config['status'] = existing_status
        elif 'status' in config and config['status']:
            nested_config['status'] = config['status']
        else:
            nested_config['status'] = 'pending'
        
        # Handle operation_status at ROOT LEVEL ONLY
        if existing_operation_status is not None:
            nested_config['operation_status'] = normalize_slashes(existing_operation_status)
        elif 'operation_status' in config and config['operation_status']:
            nested_config['operation_status'] = normalize_slashes(config['operation_status'])
        else:
            author_name = config.get('author', '')
            if not author_name and 'dynamic_values' in config:
                author_name = config['dynamic_values'].get('author', 'Unknown')
            clean_author = normalize_slashes(author_name)
            nested_config['operation_status'] = normalize_slashes(f"updated_config_construction: Configuration for '{clean_author}' processed")
        
        # Collect all other fields into dynamic_values
        dynamic_values = {}
        excluded_fields = ['status', 'operation_status', 'dynamic_values']
        
        for key, value in config.items():
            if key not in excluded_fields:
                # Sanitize value for JSON
                dynamic_values[key] = sanitize_for_json(value)
        
        # If there was already a dynamic_values, merge it (but clean it first)
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            # Clean the existing dynamic_values (remove status/operation_status and any non-allowed fields)
            cleaned_existing = clean_dynamic_values(config['dynamic_values'], allowed_fields)
            for key, value in cleaned_existing.items():
                if key not in dynamic_values:
                    dynamic_values[key] = sanitize_for_json(value)
        
        # CRITICAL: Remove any status/operation_status and non-allowed fields from dynamic_values
        dynamic_values = clean_dynamic_values(dynamic_values, allowed_fields)
        
        # Only add dynamic_values if there are fields to nest
        if dynamic_values:
            nested_config['dynamic_values'] = dynamic_values
        
        # Ensure author is in dynamic_values if not already
        if 'author' in config and 'author' not in dynamic_values:
            # Check if 'author' is allowed
            if allowed_fields is None or 'author' in allowed_fields:
                if 'dynamic_values' not in nested_config:
                    nested_config['dynamic_values'] = {}
                nested_config['dynamic_values']['author'] = sanitize_for_json(config['author'])
        
        # Final sanitization of the entire config
        nested_config = sanitize_for_json(nested_config)
        
        return nested_config
    
    def flatten_config(config):
        """Flatten a config by moving dynamic_values to root level"""
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            flattened = {}
            if 'status' in config:
                flattened['status'] = config['status']
            if 'operation_status' in config:
                flattened['operation_status'] = config['operation_status']
            for key, value in config['dynamic_values'].items():
                flattened[key] = value
            return flattened
        else:
            return config
    
    def append_operation_status(existing_message, new_message):
        """Append a new message to an existing operation_status message."""
        if existing_message:
            existing_message = normalize_slashes(existing_message)
        if new_message:
            new_message = normalize_slashes(new_message)
        
        if not existing_message:
            return new_message
        
        if existing_message.endswith('.'):
            return f"{existing_message} {new_message}"
        else:
            return f"{existing_message}. {new_message}"
    
    def get_existing_operation_status():
        """Get the existing operation_status from AUTHOR_PATH."""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            if isinstance(author_data, dict):
                return author_data.get('operation_status', None)
            elif isinstance(author_data, list) and author_data:
                return author_data[-1].get('operation_status', None)
            return None
        except Exception:
            return None
    
    def update_author_operation_status(operation_message, preserve_status=True):
        """Update operation_status in AUTHOR_PATH while preserving existing status."""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            operation_message = normalize_slashes(operation_message)
            
            if isinstance(author_data, list):
                if not author_data:
                    author_data = [{}]
                
                existing_operation = author_data[-1].get('operation_status', '')
                existing_operation = normalize_slashes(existing_operation)
                combined_message = append_operation_status(existing_operation, operation_message)
                
                if preserve_status and 'status' in author_data[-1]:
                    pass
                else:
                    if 'status' not in author_data[-1]:
                        author_data[-1]['status'] = 'pending'
                
                author_data[-1]['operation_status'] = combined_message
                
                if save_json_file(AUTHOR_PATH, author_data):
                    return True
                return False
            
            elif isinstance(author_data, dict):
                existing_operation = author_data.get('operation_status', '')
                existing_operation = normalize_slashes(existing_operation)
                combined_message = append_operation_status(existing_operation, operation_message)
                
                if 'status' not in author_data:
                    author_data['status'] = 'pending'
                
                author_data['operation_status'] = combined_message
                
                if save_json_file(AUTHOR_PATH, author_data):
                    return True
                return False
            
            return False
        except Exception as e:
            print(f"   ❌ Error updating operation_status: {e}")
            return False
    
    # ============================================================
    # STEP 0: LOAD DYNAMIC FIELDS FROM TXT
    # ============================================================
    print(f"\n{'='*60}")
    print("📋 LOADING DYNAMIC FIELDS DEFINITION...")
    print(f"{'='*60}")
    
    allowed_dynamic_fields = load_dynamic_fields()
    
    if allowed_dynamic_fields is not None:
        print(f"   📋 Allowed dynamic fields: {len(allowed_dynamic_fields)} fields")
        # Show first 10 fields for preview
        preview_fields = list(allowed_dynamic_fields)[:10]
        print(f"   📋 Fields preview: {', '.join(preview_fields)}")
        if len(allowed_dynamic_fields) > 10:
            print(f"   📋 ... and {len(allowed_dynamic_fields) - 10} more fields")
    else:
        print(f"   ℹ️ No dynamic_fields.txt found - no field filtering will be applied")
    
    # ============================================================
    # STEP 1: LOAD CONFIGURATIONS
    # ============================================================
    print(f"\n{'='*60}")
    print("📖 LOADING CONFIGURATIONS...")
    print(f"{'='*60}")
    
    errors_encountered = []
    warnings_encountered = []
    processed_count = 0
    failed_count = 0
    config_status_messages = []
    has_critical_errors = False
    removed_fields_count = 0
    removed_fields_list = []
    
    operation_msg = "updated_config_construction: Processing completed."
    
    # Load NEW_CONFIGS (should be a list)
    try:
        new_configs = load_json_file(NEW_CONFIGS, [])
        if not isinstance(new_configs, list):
            new_configs = []
        print(f"📁 Loaded {len(new_configs)} configs from NEW_CONFIGS")
    except Exception as e:
        error_msg = f"Failed to load NEW_CONFIGS: {str(e)}."
        print(f"❌ {error_msg}")
        errors_encountered.append(error_msg)
        new_configs = []
    
    # Load AUTHOR_PATH (single object or list)
    try:
        author_path_data = load_json_file(AUTHOR_PATH, {})
        print(f"📁 Loaded from AUTHOR_PATH")
        
        if isinstance(author_path_data, dict):
            author_name = author_path_data.get('author', 'Unknown')
            status = author_path_data.get('status', 'No status')
            existing_op = author_path_data.get('operation_status', 'None')
            print(f"   📝 Type: Single config object")
            print(f"   👤 Author: {author_name}")
            print(f"   📊 Status: {status}")
            if existing_op != 'None':
                normalized_preview = normalize_slashes(existing_op[:80])
                print(f"   📝 Existing operation_status: {normalized_preview}...")
            
            if 'dynamic_values' in author_path_data and isinstance(author_path_data['dynamic_values'], dict):
                if 'status' in author_path_data['dynamic_values'] or 'operation_status' in author_path_data['dynamic_values']:
                    print(f"   ⚠️ Found status/operation_status in dynamic_values - will be cleaned")
        elif isinstance(author_path_data, list):
            print(f"   📝 Type: List of {len(author_path_data)} configs")
            for idx, item in enumerate(author_path_data):
                if isinstance(item, dict):
                    author_name = item.get('author', 'Unknown')
                    status = item.get('status', 'No status')
                    existing_op = item.get('operation_status', 'None')
                    print(f"   📝 Config {idx+1}: Author={author_name}, Status={status}")
                    if existing_op != 'None':
                        normalized_preview = normalize_slashes(existing_op[:80])
                        print(f"      📝 Existing operation_status: {normalized_preview}...")
                    if 'dynamic_values' in item and isinstance(item['dynamic_values'], dict):
                        if 'status' in item['dynamic_values'] or 'operation_status' in item['dynamic_values']:
                            print(f"      ⚠️ Found status/operation_status in dynamic_values - will be cleaned")
        else:
            print(f"   ⚠️ Unknown type: {type(author_path_data)}")
            
    except Exception as e:
        error_msg = f"Failed to load AUTHOR_PATH: {str(e)}."
        print(f"❌ {error_msg}")
        errors_encountered.append(error_msg)
        author_path_data = {}
    
    # ============================================================
    # STEP 2: CONVERT CONFIGURATIONS TO NESTED FORMAT
    # ============================================================
    print(f"\n{'='*60}")
    print("🔄 CONVERTING CONFIGURATIONS TO NESTED FORMAT...")
    print("🧹 REMOVING status/operation_status FROM dynamic_values...")
    print(f"🗑️ REMOVING fields NOT in dynamic_fields.txt...")
    print("🔧 ESCAPING backslashes and special characters...")
    print("📝 NORMALIZING slashes to underscores in operation_status...")
    print(f"{'='*60}")
    
    converted_configs = []
    processed_authors = set()
    
    # Process AUTHOR_PATH (single config object or list)
    if isinstance(author_path_data, dict):
        # Single config object
        print(f"\n📝 Processing single config from AUTHOR_PATH")
        
        try:
            author_name = author_path_data.get('author', '')
            if not author_name and 'dynamic_values' in author_path_data:
                author_name = author_path_data['dynamic_values'].get('author', '')
            
            if not author_name:
                warning_msg = "Config in AUTHOR_PATH has no 'author' field. Using 'Unknown'."
                print(f"   ⚠️ {warning_msg}")
                warnings_encountered.append(warning_msg)
                author_name = 'Unknown'
            
            print(f"   👤 Author: {author_name}")
            
            existing_status = author_path_data.get('status', None)
            existing_operation_status = author_path_data.get('operation_status', None)
            
            if existing_operation_status:
                existing_operation_status = normalize_slashes(existing_operation_status)
            
            # Check for fields that will be removed
            if allowed_dynamic_fields is not None and 'dynamic_values' in author_path_data:
                current_fields = set(author_path_data['dynamic_values'].keys())
                fields_to_remove = [f for f in current_fields if f not in allowed_dynamic_fields and f not in ['status', 'operation_status']]
                if fields_to_remove:
                    print(f"   🗑️ Fields to remove from dynamic_values: {fields_to_remove}")
                    removed_fields_count += len(fields_to_remove)
                    removed_fields_list.extend(fields_to_remove)
            
            if 'dynamic_values' in author_path_data and isinstance(author_path_data['dynamic_values'], dict):
                if 'status' in author_path_data['dynamic_values']:
                    print(f"   🧹 Found status in dynamic_values - will be removed")
                if 'operation_status' in author_path_data['dynamic_values']:
                    print(f"   🧹 Found operation_status in dynamic_values - will be removed")
            
            print(f"   📊 Preserving status (root): {existing_status}")
            
            # Check if already nested
            if 'dynamic_values' in author_path_data and isinstance(author_path_data['dynamic_values'], dict):
                nested_config = nest_fields_in_dynamic_values(
                    author_path_data,
                    existing_status=existing_status,
                    existing_operation_status=existing_operation_status,
                    allowed_fields=allowed_dynamic_fields
                )
                print(f"   ✅ Already in nested format - cleaned and filtered")
            else:
                nested_config = nest_fields_in_dynamic_values(
                    author_path_data,
                    existing_status=existing_status,
                    existing_operation_status=existing_operation_status,
                    allowed_fields=allowed_dynamic_fields
                )
                print(f"   ✅ Converted to nested format")
            
            # Ensure status is preserved at root level
            if existing_status:
                nested_config['status'] = existing_status
                print(f"   ✅ Status preserved at root: {existing_status}")
            
            # Ensure no status/operation_status in dynamic_values
            if 'dynamic_values' in nested_config and isinstance(nested_config['dynamic_values'], dict):
                nested_config['dynamic_values'] = clean_dynamic_values(nested_config['dynamic_values'], allowed_dynamic_fields)
                print(f"   🧹 Confirmed: no status/operation_status in dynamic_values")
            
            # Normalize slashes in operation_status
            if 'operation_status' in nested_config:
                nested_config['operation_status'] = normalize_slashes(nested_config['operation_status'])
            
            # Final sanitization
            nested_config = sanitize_for_json(nested_config)
            
            converted_configs.append(nested_config)
            processed_authors.add(author_name)
            processed_count += 1
            
            config_status_messages.append({
                'author': author_name,
                'status': nested_config.get('status', 'pending'),
                'message': nested_config.get('operation_status', '')
            })
            
        except Exception as e:
            error_msg = f"Config in AUTHOR_PATH: Error during conversion: {str(e)}"
            print(f"   ❌ {error_msg}")
            errors_encountered.append(error_msg)
            failed_count += 1
            has_critical_errors = True
            
            try:
                error_operation_msg = normalize_slashes(f"updated_config_construction: ERROR - {error_msg}")
                error_config = {
                    "status": "aborted",
                    "operation_status": error_operation_msg,
                    "dynamic_values": {
                        "author": "Unknown",
                        "error": str(e)
                    }
                }
                converted_configs.append(error_config)
                config_status_messages.append({
                    'author': 'Unknown',
                    'status': 'aborted',
                    'message': error_operation_msg
                })
            except:
                pass
    
    elif isinstance(author_path_data, list):
        # List of configs
        for idx, config in enumerate(author_path_data):
            print(f"\n📝 Processing config {idx + 1}/{len(author_path_data)} from AUTHOR_PATH")
            
            try:
                author_name = config.get('author', '')
                if not author_name and 'dynamic_values' in config:
                    author_name = config['dynamic_values'].get('author', '')
                
                if not author_name:
                    warning_msg = f"Config {idx + 1} in AUTHOR_PATH has no 'author' field. Skipping."
                    print(f"   ⚠️ {warning_msg}")
                    warnings_encountered.append(warning_msg)
                    failed_count += 1
                    continue
                
                print(f"   👤 Author: {author_name}")
                
                existing_status = config.get('status', None)
                existing_operation_status = config.get('operation_status', None)
                
                if existing_operation_status:
                    existing_operation_status = normalize_slashes(existing_operation_status)
                
                # Check for fields that will be removed
                if allowed_dynamic_fields is not None and 'dynamic_values' in config:
                    current_fields = set(config['dynamic_values'].keys())
                    fields_to_remove = [f for f in current_fields if f not in allowed_dynamic_fields and f not in ['status', 'operation_status']]
                    if fields_to_remove:
                        print(f"   🗑️ Fields to remove from dynamic_values: {fields_to_remove}")
                        removed_fields_count += len(fields_to_remove)
                        removed_fields_list.extend(fields_to_remove)
                
                if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                    if 'status' in config['dynamic_values']:
                        print(f"   🧹 Found status in dynamic_values - will be removed")
                    if 'operation_status' in config['dynamic_values']:
                        print(f"   🧹 Found operation_status in dynamic_values - will be removed")
                
                print(f"   📊 Preserving status (root): {existing_status}")
                
                if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
                    nested_config = nest_fields_in_dynamic_values(
                        config,
                        existing_status=existing_status,
                        existing_operation_status=existing_operation_status,
                        allowed_fields=allowed_dynamic_fields
                    )
                    print(f"   ✅ Already in nested format - cleaned and filtered")
                else:
                    nested_config = nest_fields_in_dynamic_values(
                        config,
                        existing_status=existing_status,
                        existing_operation_status=existing_operation_status,
                        allowed_fields=allowed_dynamic_fields
                    )
                    print(f"   ✅ Converted to nested format")
                
                if existing_status:
                    nested_config['status'] = existing_status
                    print(f"   ✅ Status preserved at root: {existing_status}")
                
                if 'dynamic_values' in nested_config and isinstance(nested_config['dynamic_values'], dict):
                    nested_config['dynamic_values'] = clean_dynamic_values(nested_config['dynamic_values'], allowed_dynamic_fields)
                    print(f"   🧹 Confirmed: no status/operation_status in dynamic_values")
                
                if 'operation_status' in nested_config:
                    nested_config['operation_status'] = normalize_slashes(nested_config['operation_status'])
                
                nested_config = sanitize_for_json(nested_config)
                
                converted_configs.append(nested_config)
                processed_authors.add(author_name)
                processed_count += 1
                
                config_status_messages.append({
                    'author': author_name,
                    'status': nested_config.get('status', 'pending'),
                    'message': nested_config.get('operation_status', '')
                })
                
            except Exception as e:
                error_msg = f"Config {idx + 1} in AUTHOR_PATH: Error during conversion: {str(e)}"
                print(f"   ❌ {error_msg}")
                errors_encountered.append(error_msg)
                failed_count += 1
                has_critical_errors = True
    
    else:
        print("ℹ️ No valid config found in AUTHOR_PATH")
    
    # Process configs from NEW_CONFIGS (list) that aren't already processed
    for new_config in new_configs:
        author_name = new_config.get('author', '')
        if not author_name and 'dynamic_values' in new_config:
            author_name = new_config['dynamic_values'].get('author', '')
        
        if author_name and author_name not in processed_authors:
            print(f"\n📝 Adding config from NEW_CONFIGS: {author_name}")
            
            # Check for fields that will be removed
            if allowed_dynamic_fields is not None and 'dynamic_values' in new_config:
                current_fields = set(new_config['dynamic_values'].keys())
                fields_to_remove = [f for f in current_fields if f not in allowed_dynamic_fields and f not in ['status', 'operation_status']]
                if fields_to_remove:
                    print(f"   🗑️ Fields to remove from dynamic_values: {fields_to_remove}")
                    removed_fields_count += len(fields_to_remove)
                    removed_fields_list.extend(fields_to_remove)
            
            if 'dynamic_values' in new_config and isinstance(new_config['dynamic_values'], dict):
                if 'status' in new_config['dynamic_values'] or 'operation_status' in new_config['dynamic_values']:
                    print(f"   🧹 Cleaning status/operation_status from dynamic_values")
                    new_config['dynamic_values'] = clean_dynamic_values(new_config['dynamic_values'], allowed_dynamic_fields)
            
            operation_msg_new = normalize_slashes(f"updated_config_construction: Adding configuration for '{author_name}' from NEW_CONFIGS.")
            
            nested_config = nest_fields_in_dynamic_values(
                new_config,
                existing_status='pending',
                existing_operation_status=operation_msg_new,
                allowed_fields=allowed_dynamic_fields
            )
            
            if 'dynamic_values' in nested_config and isinstance(nested_config['dynamic_values'], dict):
                nested_config['dynamic_values'] = clean_dynamic_values(nested_config['dynamic_values'], allowed_dynamic_fields)
            
            if 'operation_status' in nested_config:
                nested_config['operation_status'] = normalize_slashes(nested_config['operation_status'])
            
            nested_config = sanitize_for_json(nested_config)
            
            converted_configs.append(nested_config)
            processed_authors.add(author_name)
            processed_count += 1
            
            config_status_messages.append({
                'author': author_name,
                'status': 'pending',
                'message': operation_msg_new
            })
            
            print(f"   ✅ Added config for {author_name}")
        elif author_name:
            print(f"\n📝 Skipping config from NEW_CONFIGS: {author_name} (already processed from AUTHOR_PATH)")
    
    # ============================================================
    # STEP 3: ENSURE CONSISTENCY AND CLEAN ALL dynamic_values
    # ============================================================
    print(f"\n{'='*60}")
    print("🧹 FINAL CLEANUP - REMOVING status/operation_status AND FILTERING FIELDS...")
    print(f"{'='*60}")
    
    for i, config in enumerate(converted_configs):
        if 'status' not in config or not config['status']:
            config['status'] = 'pending'
            print(f"   ✅ Added default status 'pending' to config {i + 1}")
        else:
            print(f"   ✅ Preserved existing status '{config['status']}' for config {i + 1}")
        
        if 'operation_status' not in config or not config['operation_status']:
            author_name = config.get('author', '')
            if not author_name and 'dynamic_values' in config:
                author_name = config['dynamic_values'].get('author', f'config_{i+1}')
            config['operation_status'] = normalize_slashes(f"updated_config_construction: Configuration for '{author_name}' processed")
            print(f"   ✅ Added operation_status for config {i + 1}")
        else:
            config['operation_status'] = normalize_slashes(config['operation_status'])
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            had_status = 'status' in config['dynamic_values']
            had_operation = 'operation_status' in config['dynamic_values']
            
            # This will also filter fields
            config['dynamic_values'] = clean_dynamic_values(config['dynamic_values'], allowed_dynamic_fields)
            
            if had_status:
                print(f"   🧹 Removed 'status' from dynamic_values in config {i + 1}")
            if had_operation:
                print(f"   🧹 Removed 'operation_status' from dynamic_values in config {i + 1}")
            if not had_status and not had_operation:
                print(f"   ✅ No status/operation_status found in dynamic_values in config {i + 1}")
        else:
            print(f"   ✅ No dynamic_values to clean in config {i + 1}")
    
    print(f"   ✅ All {len(converted_configs)} configs have status and operation_status at ROOT LEVEL only")
    print(f"   ✅ All slashes in operation_status normalized to underscores")
    
    if removed_fields_count > 0:
        print(f"   🗑️ Removed {removed_fields_count} fields not in dynamic_fields.txt")
        if removed_fields_list:
            unique_removed = list(set(removed_fields_list))
            print(f"   🗑️ Unique fields removed: {unique_removed}")
    
    # ============================================================
    # STEP 4: SAVE CONVERTED CONFIGS
    # ============================================================
    print(f"\n{'='*60}")
    print("💾 SAVING CONFIGURATIONS TO UPDATED_CONFIGS...")
    print(f"{'='*60}")
    
    save_success = False
    try:
        if converted_configs:
            sanitized_configs = [sanitize_for_json(config) for config in converted_configs]
            
            if save_json_file(UPDATED_CONFIGS, sanitized_configs):
                print(f"✅ Converted {len(sanitized_configs)} configs saved to UPDATED_CONFIGS")
                save_success = True
                print(f"\n📋 PER-CONFIG STATUS SUMMARY:")
                for status_info in config_status_messages:
                    status_emoji = '✅' if status_info['status'] in ['completed', 'pending'] else '⚠️' if status_info['status'] == 'warning' else '❌'
                    print(f"   {status_emoji} 👤 {status_info['author']}: {status_info['status']}")
                    normalized_msg = normalize_slashes(status_info['message'][:80])
                    print(f"      📝 {normalized_msg}...")
            else:
                error_msg = f"Failed to save converted configs to {UPDATED_CONFIGS}."
                print(f"❌ {error_msg}")
                errors_encountered.append(error_msg)
                has_critical_errors = True
        else:
            print("ℹ️ No configs to save - creating empty file")
            save_json_file(UPDATED_CONFIGS, [])
            save_success = True
    except Exception as e:
        error_msg = f"Error saving to UPDATED_CONFIGS: {str(e)}"
        print(f"❌ {error_msg}")
        errors_encountered.append(error_msg)
        has_critical_errors = True
    
    # ============================================================
    # STEP 5: VALIDATE SAVED JSON
    # ============================================================
    print(f"\n{'='*60}")
    print("🔍 VALIDATING SAVED JSON...")
    print(f"{'='*60}")
    
    try:
        if os.path.exists(UPDATED_CONFIGS):
            with open(UPDATED_CONFIGS, 'r', encoding='utf-8') as f:
                content = f.read()
                json.loads(content)
                print(f"✅ JSON validation passed - file is valid JSON")
                
                if '\\\\' in content:
                    print(f"   ✅ Backslashes are properly escaped")
                elif '\\' in content and not '\\\\' in content:
                    print(f"   ⚠️ Found unescaped backslashes - may cause issues")
                    warnings_encountered.append("Found unescaped backslashes in JSON output")
                else:
                    print(f"   ✅ No backslash issues found")
                
                import re
                op_status_matches = re.findall(r'"operation_status":\s*"([^"]*)"', content)
                for match in op_status_matches:
                    if '/' in match or '\\' in match:
                        print(f"   ⚠️ Found slashes in operation_status: {match[:50]}...")
                        warnings_encountered.append("Slashes found in operation_status - should be normalized")
                        break
                else:
                    print(f"   ✅ No slashes found in operation_status values")
                
                # Check if any fields in dynamic_values are not in the allowed list
                if allowed_dynamic_fields is not None:
                    # Parse JSON and check dynamic_values
                    parsed_data = json.loads(content)
                    for config in parsed_data:
                        if 'dynamic_values' in config:
                            dynamic_keys = set(config['dynamic_values'].keys())
                            invalid_keys = [k for k in dynamic_keys if k not in allowed_dynamic_fields and k not in ['status', 'operation_status']]
                            if invalid_keys:
                                print(f"   ⚠️ Found fields in dynamic_values not in dynamic_fields.txt: {invalid_keys}")
                                warnings_encountered.append(f"Fields not in dynamic_fields.txt: {invalid_keys}")
                            else:
                                print(f"   ✅ All fields in dynamic_values are allowed")
    except Exception as e:
        print(f"   ⚠️ Could not validate JSON: {e}")
        warnings_encountered.append(f"JSON validation warning: {e}")
    
    # ============================================================
    # STEP 6: UPDATE OPERATION_STATUS IN AUTHOR_PATH
    # ============================================================
    all_errors = errors_encountered
    detailed_issues = []
    
    if errors_encountered:
        detailed_issues.append(f"Critical Errors ({len(errors_encountered)}): " + "; ".join(errors_encountered[:3]))
        if len(errors_encountered) > 3:
            detailed_issues.append(f"... and {len(errors_encountered) - 3} more errors")
    
    if warnings_encountered:
        detailed_issues.append(f"Warnings ({len(warnings_encountered)}): " + "; ".join(warnings_encountered[:3]))
        if len(warnings_encountered) > 3:
            detailed_issues.append(f"... and {len(warnings_encountered) - 3} more warnings")
    
    existing_operation = get_existing_operation_status()
    if existing_operation:
        normalized_existing = normalize_slashes(existing_operation[:100])
        print(f"\n📝 Existing operation_status found: {normalized_existing}...")
    
    # Build operation message
    if all_errors or has_critical_errors:
        operation_msg = normalize_slashes(f"updated_config_construction: Configuration conversion encountered issues. Details: {'. '.join(detailed_issues)}.")
        print(f"\n⚠️ Updating operation_status (preserving existing status, appending, normalizing slashes)")
    else:
        if removed_fields_count > 0:
            removed_summary = f"Removed {removed_fields_count} fields not in dynamic_fields.txt"
            if warnings_encountered:
                warnings_text = "; ".join(warnings_encountered)
                operation_msg = normalize_slashes(f"updated_config_construction: Configuration conversion completed successfully with {len(warnings_encountered)} warnings. {removed_summary}. Warnings: {warnings_text}")
            else:
                operation_msg = normalize_slashes(f"updated_config_construction: Configuration conversion completed successfully. Converted {len(converted_configs)} configurations. {removed_summary}. All status fields are at root level only.")
        else:
            if warnings_encountered:
                warnings_text = "; ".join(warnings_encountered)
                operation_msg = normalize_slashes(f"updated_config_construction: Configuration conversion completed successfully with {len(warnings_encountered)} warnings. Warnings: {warnings_text}")
            else:
                operation_msg = normalize_slashes(f"updated_config_construction: Configuration conversion completed successfully. Converted {len(converted_configs)} configurations. All status fields are at root level only.")
        print(f"\n✅ Updating operation_status (preserving existing status, appending, normalizing slashes)")
    
    update_author_operation_status(operation_msg, preserve_status=True)
    
    # ============================================================
    # STEP 7: DISPLAY LIVE SUMMARY
    # ============================================================
    print(f"\n{'='*60}")
    print("📊 LIVE CONFIGURATION OPERATION SUMMARY")
    print(f"{'='*60}")
    
    for idx, status_info in enumerate(config_status_messages, 1):
        status_emoji = '✅' if status_info['status'] in ['pending', 'completed'] else '❌' if status_info['status'] == 'aborted' else '⚠️'
        print(f"\n{status_emoji} Config #{idx} - Author: {status_info['author']}")
        print(f"   Status: {status_info['status']} (PRESERVED at ROOT LEVEL)")
        normalized_msg = normalize_slashes(status_info['message'])
        print(f"   Operation: {normalized_msg}")
        if idx < len(config_status_messages):
            print(f"   {'-'*50}")
    
    if not config_status_messages:
        print("ℹ️ No configurations were processed.")
    
    # ============================================================
    # SUMMARY
    # ============================================================
    print(f"\n{'='*60}")
    print("✅ CONFIGURATION CONVERTER COMPLETED!")
    print(f"\n📊 Summary:")
    print(f"  - Processed from AUTHOR_PATH: 1 config (preserved status at root)")
    print(f"  - Added from NEW_CONFIGS: {len([c for c in new_configs if c.get('author') not in processed_authors])}")
    print(f"  - Total configs saved: {len(converted_configs)}")
    print(f"  - Statuses preserved at ROOT LEVEL (NOT changed)")
    print(f"  - status/operation_status REMOVED from dynamic_values")
    if removed_fields_count > 0:
        print(f"  - 🗑️ Removed {removed_fields_count} fields NOT in dynamic_fields.txt")
        if removed_fields_list:
            unique_removed = list(set(removed_fields_list))
            preview_removed = unique_removed[:10]
            print(f"  - 🗑️ Removed fields: {', '.join(preview_removed)}")
            if len(unique_removed) > 10:
                print(f"  - 🗑️ ... and {len(unique_removed) - 10} more fields removed")
    else:
        print(f"  - ✅ All fields are in dynamic_fields.txt (no fields removed)")
    print(f"  - Configs with operation status: {len(config_status_messages)}")
    print(f"  - All backslashes properly escaped for JSON")
    print(f"  - New messages APPENDED to existing operation_status (not overwritten)")
    print(f"  - All slashes (/) and backslashes (\\) normalized to underscores (_)")
    
    if warnings_encountered:
        print(f"\n⚠️ WARNINGS ({len(warnings_encountered)}):")
        for warning in warnings_encountered[:5]:
            normalized_warning = normalize_slashes(warning)
            print(f"    - {normalized_warning}")
        if len(warnings_encountered) > 5:
            print(f"    ... and {len(warnings_encountered) - 5} more warnings")
    
    if all_errors:
        print(f"\n❌ ERRORS ({len(all_errors)}):")
        for error in all_errors[:5]:
            normalized_error = normalize_slashes(error)
            print(f"    - {normalized_error}")
        if len(all_errors) > 5:
            print(f"    ... and {len(all_errors) - 5} more errors")
    
    print(f"{'='*60}\n")
    
    return len(all_errors) == 0 and not has_critical_errors

def update_settings():
    """
    Updates only the settings in serenum_config table without touching URLs.
    Reads from UPDATED_CONFIGS file, copies the entire data as a string,
    and updates the settings column with it.
    
    STAGE 1: Extract uploaded_jpgs_url data and save to temp file
    STAGE 2: Update settings in serenum_config (filtered)
    STAGE 3: Send uploaded JPGs to jpgsvault
    STAGE 4: Reload page and confirm before closing
    
    Uses clipboard-based communication only.
    Creates default files if they don't exist or are invalid.
    Closes the Edge window upon successful completion.
    
    Updates operation_status in AUTHOR_PATH based on processing results.
    APPENDS new messages to existing operation_status.
    Contains professional message explaining any issues.
    
    PRE-CHECKS:
    - Validates that there is actual data to update (settings or uploaded_jpgs_url)
    - Does NOT launch browser if both are empty
    - Does NOT write empty data to database
    """
    # First reconstruct the configs
    reconstruction_success = updated_config_construction()
    if not reconstruction_success:
        print("❌ [UPDATE] Configuration reconstruction failed. Aborting update.")
        # Append to existing operation_status
        append_author_operation_status('Sorry, the settings update could not proceed because the configuration reconstruction failed. Please check the source files.')
        return False
    
    pyautogui.PAUSE = 0.0
    
    # Define termination flag
    terminate_automation = False
    
    # Define MAX_RETRIES for operations
    MAX_OPERATION_RETRIES = 5
    
    # Helper functions for status updates
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError as e:
            return default if default is not None else {}
        except Exception as e:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            return False
    
    def normalize_slashes(text):
        """
        Normalize all slashes (forward and backslashes) to underscores.
        This ensures operation_status messages don't contain problematic characters.
        """
        if not isinstance(text, str):
            return text
        
        # Replace all backslashes and forward slashes with underscore
        text = text.replace('\\', '_')
        text = text.replace('/', '_')
        text = text.replace('\\\\', '_')
        
        return text
    
    def append_operation_status(existing_message, new_message):
        """
        Append a new message to an existing operation_status message.
        Normalizes all slashes to underscores in both messages.
        Returns the combined message with proper formatting.
        """
        # Normalize slashes in both messages
        if existing_message:
            existing_message = normalize_slashes(existing_message)
        if new_message:
            new_message = normalize_slashes(new_message)
        
        if not existing_message:
            return new_message
        
        # If the existing message already ends with a period, add space
        if existing_message.endswith('.'):
            return f"{existing_message} {new_message}"
        else:
            return f"{existing_message}. {new_message}"
    
    def append_author_operation_status(operation_message):
        """
        Append a new message to the existing operation_status in AUTHOR_PATH.
        Preserves existing status.
        """
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            # Handle both dict and list formats
            if isinstance(author_data, dict):
                # Get existing operation_status
                existing_operation = author_data.get('operation_status', '')
                
                # Append new message to existing
                combined_message = append_operation_status(existing_operation, operation_message)
                
                # Update operation_status
                author_data['operation_status'] = combined_message
                
                if save_json_file(AUTHOR_PATH, author_data):
                    return True
            elif isinstance(author_data, list) and author_data:
                # Get existing operation_status
                existing_operation = author_data[-1].get('operation_status', '')
                
                # Append new message to existing
                combined_message = append_operation_status(existing_operation, operation_message)
                
                # Update operation_status
                author_data[-1]['operation_status'] = combined_message
                
                if save_json_file(AUTHOR_PATH, author_data):
                    return True
            return False
        except Exception as e:
            return False
    
    def get_existing_operation_status():
        """Get the existing operation_status from AUTHOR_PATH."""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            if isinstance(author_data, dict):
                return author_data.get('operation_status', '')
            elif isinstance(author_data, list) and author_data:
                return author_data[-1].get('operation_status', '')
            return ''
        except Exception:
            return ''
    
    def check_for_termination():
        if terminate_automation:
            raise KeyboardInterrupt("User forced exit via shortcut key.")
    
    def ensure_updated_configs_exists():
        """Create default UPDATED_CONFIGS file if it doesn't exist or is invalid."""
        if os.path.exists(UPDATED_CONFIGS):
            try:
                with open(UPDATED_CONFIGS, 'r', encoding='utf-8') as file:
                    json.load(file)
                return True
            except json.JSONDecodeError as e:
                error_msg = f"UPDATED_CONFIGS contains invalid JSON: {str(e)}. The file may be corrupted."
                print(f"⚠️ [VALIDATE] {error_msg}")
                try:
                    os.remove(UPDATED_CONFIGS)
                except:
                    pass
                return False
            except Exception as e:
                error_msg = f"Failed to read UPDATED_CONFIGS: {str(e)}"
                print(f"⚠️ [VALIDATE] {error_msg}")
                return False
        else:
            print(f"📁 [VALIDATE] UPDATED_CONFIGS not found, creating default...")
        
        default_config = {
            "url": "https://fhdrikxsirudr.fwh.is/phpmysqlkdkw.php",
            "author": "Brilliance",
            "engine": "csv",
            "page": "none",
            "group": "include",
            "processjpgfrom": "freshjpgs"
        }
        
        try:
            os.makedirs(os.path.dirname(UPDATED_CONFIGS), exist_ok=True)
            with open(UPDATED_CONFIGS, 'w', encoding='utf-8') as file:
                json.dump(default_config, file, indent=2, ensure_ascii=False, separators=(',', ': '))
            return True
        except Exception as e:
            error_msg = f"Failed to create default UPDATED_CONFIGS: {str(e)}. Check file permissions and disk space."
            print(f"❌ [VALIDATE] {error_msg}")
            return False
    
    def ensure_new_configs_exists():
        """Create default NEW_CONFIGS file if it doesn't exist or is invalid."""
        if os.path.exists(NEW_CONFIGS):
            try:
                with open(NEW_CONFIGS, 'r', encoding='utf-8') as file:
                    json.load(file)
                return True
            except json.JSONDecodeError as e:
                error_msg = f"NEW_CONFIGS contains invalid JSON: {str(e)}. The file may be corrupted."
                print(f"⚠️ [VALIDATE] {error_msg}")
                try:
                    os.remove(NEW_CONFIGS)
                except:
                    pass
                return False
            except Exception as e:
                error_msg = f"Failed to read NEW_CONFIGS: {str(e)}"
                print(f"⚠️ [VALIDATE] {error_msg}")
                return False
        else:
            print(f"📁 [VALIDATE] NEW_CONFIGS not found, creating default...")
        
        default_config = {
            "url": "https://fhdrikxsirudr.fwh.is/phpmysqlkdkw.php",
            "author": "Brilliance",
            "engine": "csv",
            "page": "none",
            "group": "include",
            "processjpgfrom": "freshjpgs"
        }
        
        try:
            os.makedirs(os.path.dirname(NEW_CONFIGS), exist_ok=True)
            with open(NEW_CONFIGS, 'w', encoding='utf-8') as file:
                json.dump(default_config, file, indent=2, ensure_ascii=False, separators=(',', ': '))
            return True
        except Exception as e:
            error_msg = f"Failed to create default NEW_CONFIGS: {str(e)}. Check file permissions and disk space."
            print(f"❌ [VALIDATE] {error_msg}")
            return False
    
    def extract_uploaded_jpgs_data(config_data):
        """
        Extract uploaded_jpgs_url data from config and return it separately.
        Handles nested structures properly.
        Returns: (filtered_config, uploaded_jpgs_data)
        """
        uploaded_jpgs_data = None
        
        # Handle different config structures
        if isinstance(config_data, list):
            # If it's a list, process each item
            for idx, item in enumerate(config_data):
                if isinstance(item, dict):
                    # Check for uploaded_jpgs_url in this item
                    if 'uploaded_jpgs_url' in item:
                        uploaded_jpgs_data = item.pop('uploaded_jpgs_url')
                        print(f"📸 [EXTRACT] Found uploaded_jpgs_url data in list item {idx} with {len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items")
                        break
                    else:
                        # Check nested fields
                        for key, value in item.items():
                            if isinstance(value, dict) and 'uploaded_jpgs_url' in value:
                                uploaded_jpgs_data = value.pop('uploaded_jpgs_url')
                                print(f"📸 [EXTRACT] Found uploaded_jpgs_url data in nested '{key}' with {len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items")
                                break
                            elif isinstance(value, list):
                                for sub_idx, sub_item in enumerate(value):
                                    if isinstance(sub_item, dict) and 'uploaded_jpgs_url' in sub_item:
                                        uploaded_jpgs_data = sub_item.pop('uploaded_jpgs_url')
                                        print(f"📸 [EXTRACT] Found uploaded_jpgs_url data in list {key}[{sub_idx}] with {len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items")
                                        break
                                if uploaded_jpgs_data:
                                    break
                    if uploaded_jpgs_data:
                        break
        
        elif isinstance(config_data, dict):
            # Check if there's an uploaded_jpgs_url field at root level
            if 'uploaded_jpgs_url' in config_data:
                uploaded_jpgs_data = config_data.pop('uploaded_jpgs_url')
                print(f"📸 [EXTRACT] Found uploaded_jpgs_url data at root level with {len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items")
            
            # Check for uploaded_jpgs_url in nested structures
            for key, value in config_data.items():
                if isinstance(value, dict) and 'uploaded_jpgs_url' in value:
                    uploaded_jpgs_data = value.pop('uploaded_jpgs_url')
                    print(f"📸 [EXTRACT] Found uploaded_jpgs_url data in nested '{key}' with {len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items")
                elif isinstance(value, list):
                    for idx, item in enumerate(value):
                        if isinstance(item, dict) and 'uploaded_jpgs_url' in item:
                            uploaded_jpgs_data = item.pop('uploaded_jpgs_url')
                            print(f"📸 [EXTRACT] Found uploaded_jpgs_url data in list item {idx} with {len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items")
                            break
                if uploaded_jpgs_data:
                    break
        
        return config_data, uploaded_jpgs_data
    
    def has_meaningful_data(config_data):
        """
        Check if config_data has meaningful data (not empty).
        Returns True if there's actual data to update.
        """
        if not config_data:
            return False
        
        # Check if it's a list
        if isinstance(config_data, list):
            if not config_data:
                return False
            # Check each item
            for item in config_data:
                if isinstance(item, dict) and item:
                    # Remove status and operation_status from consideration
                    item_copy = item.copy()
                    item_copy.pop('status', None)
                    item_copy.pop('operation_status', None)
                    if item_copy:
                        return True
            return False
        
        # Check if it's a dict
        if isinstance(config_data, dict):
            # Remove status and operation_status from consideration
            config_copy = config_data.copy()
            config_copy.pop('status', None)
            config_copy.pop('operation_status', None)
            if config_copy:
                return True
        
        return False
    
    def has_uploaded_jpgs_data(uploaded_data):
        """
        Check if uploaded_jpgs_url data has meaningful content.
        Returns True if there are actual URLs or data to store.
        """
        if not uploaded_data:
            return False
        
        if isinstance(uploaded_data, list):
            # Check if list has actual URL strings or meaningful data
            meaningful_items = []
            for item in uploaded_data:
                if isinstance(item, str) and item.startswith(('http://', 'https://')):
                    meaningful_items.append(item)
                elif isinstance(item, dict) and item:
                    # Check if dict has meaningful content (not just metadata)
                    if item.get('folder') or item.get('_timestamp'):
                        meaningful_items.append(item)
                    elif item:
                        meaningful_items.append(item)
                elif item:  # Any non-empty item
                    meaningful_items.append(item)
            
            return len(meaningful_items) > 0
        
        return bool(uploaded_data)
    
    def save_uploaded_jpgs_to_temp(uploaded_jpgs_data):
        """
        Save uploaded_jpgs_url data to a temporary JSON file
        Returns: (success, file_path)
        """
        if not uploaded_jpgs_data:
            print("📸 [TEMP] No uploaded_jpgs_url data to save")
            return True, None
        
        try:
            # Create temp directory if it doesn't exist
            temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            temp_file = os.path.join(temp_dir, 'uploaded_jpgs_temp.json')
            
            # Save the data
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(uploaded_jpgs_data, f, indent=2, ensure_ascii=False)
            
            print(f"📸 [TEMP] Saved uploaded_jpgs_url data to: {temp_file}")
            return True, temp_file
            
        except Exception as e:
            error_msg = f"Failed to save uploaded_jpgs_url to temp file: {str(e)}"
            print(f"❌ [TEMP] {error_msg}")
            return False, None
    
    def send_uploadedjpgs_to_database(hwnd, uploaded_jpgs_data):
        """
        Send uploaded_jpgs_url data to the database via jpgsvault.uploadedjpgs
        Returns: (success, message)
        """
        print(f"📸 [UPLOAD] Sending uploaded_jpgs_url data to database...")
        
        try:
            # Convert to JSON string - ensure it's always a valid array
            if uploaded_jpgs_data and has_uploaded_jpgs_data(uploaded_jpgs_data):
                uploadedjpgs_json = json.dumps(uploaded_jpgs_data, ensure_ascii=False)
            else:
                # If no meaningful data, don't update
                print("📸 [UPLOAD] No meaningful uploaded_jpgs_url data to store")
                return True, "No data to store (skipped)"
            
            print(f"📸 [UPLOAD] JSON data size: {len(uploadedjpgs_json)} characters")
            
            # Build the SQL query to update uploadedjpgs column
            uploadedjpgs_escaped = uploadedjpgs_json.replace("'", "''")
            sql_query = f"UPDATE jpgsvault SET uploadedjpgs = '{uploadedjpgs_escaped}' WHERE id = 1"
            
            print(f"📸 [UPLOAD] Executing: {sql_query[:150]}...")
            
            # Execute the query
            hwnd = enforce_window_focus(hwnd)
            pyautogui.press('tab')
            time.sleep(0.3)
            
            hwnd = enforce_window_focus(hwnd)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.2)
            
            hwnd = enforce_window_focus(hwnd)
            pyperclip.copy(sql_query)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            hwnd = enforce_window_focus(hwnd)
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Check for result data directly - don't wait for enter confirmation
            print("⏳ [UPLOAD] Waiting for query result...")
            result = wait_for_clipboard_data_with_retry(
                max_retries=8,
                retry_delay=0.5,
                min_content_length=5,
                hwnd=hwnd
            )
            
            if result:
                print(f"✅ [UPLOAD] uploadedjpgs data sent: {result[:100]}...")
                return True, "uploadedjpgs data stored successfully"
            else:
                print("⚠️ [UPLOAD] No confirmation received, but data may have been stored")
                return True, "uploadedjpgs data may have been stored (no confirmation)"
            
        except Exception as e:
            error_msg = f"Failed to send uploadedjpgs data: {str(e)}"
            print(f"❌ [UPLOAD] {error_msg}")
            return False, error_msg
    
    def get_phpmyadmin_url():
        """Get phpMyAdmin URL from NEW_CONFIGS"""
        try:
            with open(NEW_CONFIGS, 'r', encoding='utf-8') as file:
                panel_data = json.load(file)
        except:
            return PHPSQLURL
        
        phpmyadmin_url = None
        
        def search_for_phpmyadmin(data, path=""):
            nonlocal phpmyadmin_url
            if phpmyadmin_url:
                return
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    if isinstance(value, str) and "phpmysqlkdkw.php" in value:
                        phpmyadmin_url = value
                        print(f"🔍 [PHPMYADMIN] Found template reference in: {current_path}")
                        return
                    if isinstance(value, (dict, list)):
                        search_for_phpmyadmin(value, current_path)
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    current_path = f"{path}[{index}]"
                    if isinstance(item, (dict, list)):
                        search_for_phpmyadmin(item, current_path)
        
        search_for_phpmyadmin(panel_data)
        
        if not phpmyadmin_url:
            def search_for_url_with_phpmyadmin(data):
                nonlocal phpmyadmin_url
                if phpmyadmin_url:
                    return
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, str):
                            if value.startswith(('http://', 'https://')) and 'phpmyadmin' in value.lower():
                                phpmyadmin_url = value
                                print(f"🔍 [PHPMYADMIN] Found phpMyAdmin URL in field '{key}': {phpmyadmin_url}")
                                return
                        elif isinstance(value, (dict, list)):
                            search_for_url_with_phpmyadmin(value)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, (dict, list)):
                            search_for_url_with_phpmyadmin(item)
            
            search_for_url_with_phpmyadmin(panel_data)
        
        return phpmyadmin_url if phpmyadmin_url else PHPSQLURL
    
    # Track errors and warnings
    errors_encountered = []
    warnings_encountered = []
    uploadedjpgs_processed = False
    uploaded_jpgs_data = None
    temp_file_path = None
    has_settings_to_update = False
    has_uploadedjpgs_to_update = False
    
    # Ensure both files exist and are valid
    if not ensure_updated_configs_exists():
        error_msg = "The UPDATED_CONFIGS file could not be created or validated. Check file permissions and disk space."
        print(f"❌ [INIT] {error_msg}")
        errors_encountered.append(error_msg)
        append_author_operation_status(f"Sorry, the settings update could not start: {error_msg}")
        return False
    
    if not ensure_new_configs_exists():
        error_msg = "The NEW_CONFIGS file could not be created or validated. Check file permissions and disk space."
        print(f"❌ [INIT] {error_msg}")
        errors_encountered.append(error_msg)
        append_author_operation_status(f"Sorry, the settings update could not start: {error_msg}")
        return False
    
    # Read the updated config data
    try:
        with open(UPDATED_CONFIGS, 'r', encoding='utf-8') as file:
            updated_data = json.load(file)
        
        # ============================================================
        # STAGE 1: Extract uploaded_jpgs_url data and save to temp
        # ============================================================
        print(f"\n{'='*60}")
        print("📸 [STAGE 1] Extracting uploaded_jpgs_url data...")
        print(f"{'='*60}")
        
        filtered_data, uploaded_jpgs_data = extract_uploaded_jpgs_data(updated_data)
        
        # ============================================================
        # PRE-CHECK: Validate if there's any data to update
        # ============================================================
        print(f"\n{'='*60}")
        print("🔍 [PRE-CHECK] Validating data to update...")
        print(f"{'='*60}")
        
        # Check if there's meaningful settings data
        has_settings_to_update = has_meaningful_data(filtered_data)
        print(f"📋 Settings data: {'✅ Has data' if has_settings_to_update else '❌ Empty/no data'}")
        
        # Check if there's meaningful uploaded_jpgs_url data
        has_uploadedjpgs_to_update = has_uploaded_jpgs_data(uploaded_jpgs_data)
        print(f"📸 Uploaded JPGs data: {'✅ Has data' if has_uploadedjpgs_to_update else '❌ Empty/no data'}")
        
        # If both are empty, abort without launching browser
        if not has_settings_to_update and not has_uploadedjpgs_to_update:
            error_msg = "No meaningful data to update. Both settings and uploaded_jpgs_url are empty. Aborting update to prevent writing empty data."
            print(f"❌ [PRE-CHECK] {error_msg}")
            errors_encountered.append(error_msg)
            append_author_operation_status(f"Sorry, the settings update was aborted: {error_msg}")
            return False
        
        # Save uploaded_jpgs_url data to temp file only if it has meaningful data
        if uploaded_jpgs_data is not None and has_uploadedjpgs_to_update:
            temp_success, temp_file_path = save_uploaded_jpgs_to_temp(uploaded_jpgs_data)
            if not temp_success:
                error_msg = "Failed to save uploaded_jpgs_url data to temp file"
                errors_encountered.append(error_msg)
                append_author_operation_status(f"Sorry, the settings update could not save JPG data: {error_msg}")
                return False
            print(f"📸 [STAGE 1] Uploaded JPGs data saved to temp ({len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items)")
        else:
            if uploaded_jpgs_data is not None:
                print("📸 [STAGE 1] No meaningful uploaded_jpgs_url data found - skipping upload")
            else:
                print("📸 [STAGE 1] No uploaded_jpgs_url data found in config")
        
        # Create settings string from filtered data only if it has meaningful data
        if has_settings_to_update:
            settings_string = json.dumps(filtered_data, ensure_ascii=False, separators=(',', ': '))
            print(f"📋 [UPDATE] Filtered settings data: {len(settings_string)} characters")
            print(f"📋 [UPDATE] Preview: {settings_string[:200]}...")
        else:
            settings_string = None
            print(f"📋 [UPDATE] No meaningful settings data to update - skipping settings update")
        
    except json.JSONDecodeError as e:
        error_msg = f"UPDATED_CONFIGS contains invalid JSON: {str(e)}. The file is corrupted and cannot be read."
        print(f"❌ {error_msg}")
        errors_encountered.append(error_msg)
        append_author_operation_status(f"Sorry, the settings update could not read the configuration: {error_msg}")
        return False
    except Exception as e:
        error_msg = f"Failed to read UPDATED_CONFIGS: {str(e)}. Check file permissions."
        print(f"❌ {error_msg}")
        errors_encountered.append(error_msg)
        append_author_operation_status(f"Sorry, the settings update could not read the configuration: {error_msg}")
        return False
    
    # If we get here, we have at least one type of data to update
    print(f"\n✅ [PRE-CHECK] At least one data source has content - proceeding with update")
    
    # Get phpMyAdmin URL
    phpmyadmin_url = get_phpmyadmin_url()
    print(f"🔍 [PHPMYADMIN] Using URL: {phpmyadmin_url}")
    
    # ============================================================
    # WINDOW MANAGEMENT FUNCTIONS
    # ============================================================
    def get_current_monitor():
        try:
            cursor_pos = win32api.GetCursorPos()
            monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint(cursor_pos))
            return monitor_info['Monitor']
        except Exception:
            return (0, 0, win32api.GetSystemMetrics(win32con.SM_CXSCREEN), 
                   win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
    
    def get_edge_window_on_monitor(monitor_bounds):
        monitor_left, monitor_top, monitor_right, monitor_bottom = monitor_bounds
        edge_windows = []
        edge_process_names = ["msedge.exe"]
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process = psutil.Process(pid)
                    if process.name().lower() in edge_process_names:
                        rect = win32gui.GetWindowRect(hwnd)
                        left, top, right, bottom = rect
                        width, height = right - left, bottom - top
                        if width > 200 and height > 200:
                            window_center_x = (left + right) / 2
                            window_center_y = (top + bottom) / 2
                            is_on_current_monitor = (
                                monitor_left <= window_center_x <= monitor_right and
                                monitor_top <= window_center_y <= monitor_bottom
                            )
                            if is_on_current_monitor:
                                windows.append({'hwnd': hwnd, 'width': width, 'height': height})
                except Exception:
                    pass
            return True
        
        win32gui.EnumWindows(enum_windows_callback, edge_windows)
        edge_windows.sort(key=lambda w: w['width'] * w['height'], reverse=True)
        return edge_windows
    
    def close_edge_window(hwnd):
        """Close the Edge window gracefully."""
        try:
            if win32gui.IsWindow(hwnd):
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                time.sleep(0.5)
                
                if win32gui.IsWindow(hwnd):
                    win32gui.DestroyWindow(hwnd)
                    time.sleep(0.3)
                
                return True
            else:
                return False
        except Exception as e:
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                if process.name().lower() == "msedge.exe":
                    process.terminate()
                    time.sleep(0.5)
                    return True
            except:
                pass
            return False
    
    def ensure_edge_window_ready():
        """Ensure Edge window exists and is maximized/focused"""
        check_for_termination()
        
        current_monitor = get_current_monitor()
        print(f"🖥️ [WATCHDOG] Monitor bounds: {current_monitor}")
        
        edge_windows = get_edge_window_on_monitor(current_monitor)
        
        if edge_windows:
            hwnd = edge_windows[0]['hwnd']
            print(f"🪟 [WATCHDOG] Found existing Edge window handle: {hwnd}")
            
            try:
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.3)
                
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                time.sleep(0.5)
                
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                except Exception as e:
                    try:
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.3)
                    except:
                        pass
                
                return hwnd
            except Exception as e:
                return hwnd
        
        subprocess.Popen([edge_path, "about:blank"])
        
        for attempt in range(20):
            check_for_termination()
            time.sleep(0.5)
            edge_windows = get_edge_window_on_monitor(current_monitor)
            if edge_windows:
                hwnd = edge_windows[0]['hwnd']
                
                try:
                    if win32gui.IsIconic(hwnd):
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        time.sleep(0.3)
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    time.sleep(0.5)
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                        time.sleep(0.2)
                    except:
                        pass
                    return hwnd
                except Exception as e:
                    continue
        
        raise RuntimeError("Failed to get or launch Edge window")
    
    def enforce_window_focus(hwnd):
        """Enforce window focus and maximized state"""
        check_for_termination()
        try:
            if not win32gui.IsWindow(hwnd):
                return ensure_edge_window_ready()
            
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.3)
            
            current_foreground = win32gui.GetForegroundWindow()
            if current_foreground != hwnd:
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.15)
                except Exception as e:
                    try:
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.3)
                    except:
                        pass
            
            try:
                placement = win32gui.GetWindowPlacement(hwnd)
                if placement[1] != win32con.SW_SHOWMAXIMIZED:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    time.sleep(0.3)
            except Exception as e:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    time.sleep(0.3)
                except:
                    pass
            
            return hwnd
        except Exception as e:
            return hwnd
    
    def ensure_window_ready_and_focused():
        """Get or create window and ensure it's ready"""
        check_for_termination()
        hwnd = ensure_edge_window_ready()
        return enforce_window_focus(hwnd)
    
    def fast_paste_url(hwnd, url, retry_count=0):
        """Fast paste URL with watchdog and retry"""
        check_for_termination()
        print(f"📋 Pasting URL: {url}")
        pyperclip.copy(url)
        
        try:
            hwnd = enforce_window_focus(hwnd)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.1)
            hwnd = enforce_window_focus(hwnd)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            return True, hwnd
        except Exception as e:
            if retry_count < 3:
                time.sleep(0.5)
                hwnd = ensure_window_ready_and_focused()
                return fast_paste_url(hwnd, url, retry_count + 1)
            else:
                return False, hwnd
    
    def wait_for_clipboard_content(expected_contains=None, timeout=60, check_interval=0.5):
        """Wait for clipboard to contain expected content or have any content."""
        check_for_termination()
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            check_for_termination()
            try:
                current_content = pyperclip.paste()
                if current_content and current_content.strip():
                    if expected_contains:
                        if expected_contains in current_content:
                            return current_content
                    else:
                        return current_content
            except Exception as e:
                pass
            
            time.sleep(check_interval)
        
        return None
    
    def wait_for_clipboard_data_with_retry(max_retries=12, retry_delay=0.5, min_content_length=5, hwnd=None):
        """Wait for clipboard content with retries - DIRECT check, no enter confirmation blocking."""
        print(f"⏳ [CLIPBOARD] Waiting for data with {max_retries} retries...")
        
        previous_content = None
        
        for attempt in range(max_retries):
            check_for_termination()
            
            try:
                current_content = pyperclip.paste()
                
                if current_content and current_content.strip():
                    content_length = len(current_content.strip())
                    
                    # Skip "enter button activated" - we don't wait for it
                    if "enter button activated" in current_content:
                        print(f"ℹ️ [CLIPBOARD] Enter detected, checking for actual data...")
                        time.sleep(retry_delay)
                        continue
                    
                    if current_content != previous_content:
                        print(f"📋 [CLIPBOARD] Attempt {attempt + 1}/{max_retries}: New content found ({content_length} chars)")
                        
                        # Check if it's meaningful data (not just "enter button activated")
                        if content_length > min_content_length and "enter button activated" not in current_content:
                            return current_content
                        else:
                            print(f"ℹ️ [CLIPBOARD] Content is confirmation message, waiting for actual data...")
                    else:
                        print(f"⏳ [CLIPBOARD] Attempt {attempt + 1}/{max_retries}: No new content")
                else:
                    print(f"⏳ [CLIPBOARD] Attempt {attempt + 1}/{max_retries}: Empty clipboard")
                
                previous_content = current_content
                
            except Exception as e:
                print(f"⚠️ [CLIPBOARD] Error reading: {e}")
            
            if attempt > 0 and attempt % 5 == 0 and hwnd:
                try:
                    hwnd = enforce_window_focus(hwnd)
                except:
                    pass
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        
        return None
    
    def execute_update_query(hwnd, settings_string, retry_count=0):
        """
        Execute the UPDATE query with the settings data.
        Includes watchdog and retry logic.
        """
        settings_escaped = settings_string.replace("'", "''")
        sql_query = f"UPDATE serenum_config SET settings = '{settings_escaped}'"
        
        print(f"\n{'='*60}")
        print(f"🚀 [UPDATE] Updating settings in serenum_config (Attempt {retry_count + 1}/{MAX_OPERATION_RETRIES})")
        print(f"📝 [SQL] {sql_query[:200]}...")
        print(f"{'='*60}")
        
        try:
            print("⌨️ [STEP 1] Ensuring window focus...")
            hwnd = enforce_window_focus(hwnd)
            time.sleep(0.3)
            
            print("⌨️ [STEP 2] Pressing Tab to focus textarea...")
            hwnd = enforce_window_focus(hwnd)
            pyautogui.press('tab')
            time.sleep(0.3)
            
            print("⌨️ [STEP 3] Ensuring textarea is empty...")
            hwnd = enforce_window_focus(hwnd)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.2)
            
            print("📋 [STEP 4] Clearing clipboard...")
            try:
                pyperclip.copy("")
                time.sleep(0.2)
            except:
                pass
            
            print(f"⌨️ [STEP 5] Typing UPDATE query...")
            hwnd = enforce_window_focus(hwnd)
            pyperclip.copy(sql_query)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            print("⌨️ [STEP 6] Pressing Enter to execute query...")
            hwnd = enforce_window_focus(hwnd)
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Directly check for data - no enter confirmation blocking
            print("⏳ [STEP 7] Waiting for query result...")
            result = wait_for_clipboard_data_with_retry(
                max_retries=10,
                retry_delay=0.5,
                min_content_length=5,
                hwnd=hwnd
            )
            
            if not result:
                error_msg = f"SQL query '{sql_query[:50]}...' was executed but no result was received. The update may have failed."
                print(f"❌ [STEP 7] {error_msg}")
                
                if retry_count < MAX_OPERATION_RETRIES - 1:
                    print(f"🔄 [RETRY] Update failed, retrying in 2 seconds...")
                    time.sleep(2)
                    hwnd = ensure_window_ready_and_focused()
                    return execute_update_query(hwnd, settings_string, retry_count + 1)
                return False, error_msg
            
            print(f"✅ [STEP 7] Update completed: {result[:150]}...")
            return True, None
            
        except Exception as e:
            error_msg = f"Unexpected error during UPDATE operation: {str(e)}"
            print(f"❌ [UPDATE] {error_msg}")
            import traceback
            traceback.print_exc()
            
            if retry_count < MAX_OPERATION_RETRIES - 1:
                print(f"🔄 [RETRY] Exception occurred, retrying in 2 seconds...")
                time.sleep(2)
                try:
                    hwnd = ensure_window_ready_and_focused()
                    return execute_update_query(hwnd, settings_string, retry_count + 1)
                except:
                    pass
            return False, error_msg
    
    # ============================================================
    # MAIN EXECUTION (Only if we have data to update)
    # ============================================================
    try:
        # Step 1: Get or create Edge window
        hwnd = ensure_window_ready_and_focused()
        
        # Step 2: Navigate to phpMyAdmin URL
        success, hwnd = fast_paste_url(hwnd, phpmyadmin_url)
        if not success:
            error_msg = f"Failed to navigate to '{phpmyadmin_url}'. The browser may have issues loading the page."
            print(f"❌ [NAVIGATION] {error_msg}")
            errors_encountered.append(error_msg)
            append_author_operation_status(f"Sorry, the settings update could not navigate to the database interface: {error_msg}")
            try:
                close_edge_window(hwnd)
            except:
                pass
            return False
        
        # Step 3: Wait for page to load
        print("⏳ [NAVIGATION] Waiting for page to load...")
        
        page_ready = None
        for attempt in range(MAX_OPERATION_RETRIES):
            hwnd = enforce_window_focus(hwnd)
            
            if attempt > 0:
                print(f"🔄 [NAVIGATION] Reloading page (attempt {attempt + 1})...")
                pyautogui.hotkey('ctrl', 'r')
                time.sleep(2)
                hwnd = enforce_window_focus(hwnd)
            
            page_ready = wait_for_clipboard_content(
                expected_contains="page is ready", 
                timeout=15 if attempt == 0 else 10, 
                check_interval=0.5
            )
            
            if page_ready:
                print(f"✅ [NAVIGATION] Page is ready (attempt {attempt + 1})")
                break
            else:
                print(f"⚠️ [NAVIGATION] Page not ready (attempt {attempt + 1})")
                time.sleep(1)
        
        if not page_ready:
            error_msg = f"The phpMyAdmin page at '{phpmyadmin_url}' failed to load after {MAX_OPERATION_RETRIES} attempts. Check if the URL is accessible and the server is running."
            print(f"❌ {error_msg}")
            errors_encountered.append(error_msg)
            append_author_operation_status(f"Sorry, the settings update could not load the database page: {error_msg}")
            try:
                close_edge_window(hwnd)
            except:
                pass
            return False
        
        print("✅ [NAVIGATION] Page is ready")
        hwnd = enforce_window_focus(hwnd)
        
        # ============================================================
        # STAGE 2: EXECUTE UPDATE QUERY (Only if we have settings data)
        # ============================================================
        if has_settings_to_update and settings_string:
            print(f"\n{'='*60}")
            print("📝 [STAGE 2] Updating filtered settings...")
            print(f"{'='*60}")
            
            success, error_msg = execute_update_query(hwnd, settings_string)
            
            if not success:
                if error_msg:
                    errors_encountered.append(error_msg)
                else:
                    error_msg = "The UPDATE operation failed to execute successfully. Check the database connection and query syntax."
                    errors_encountered.append(error_msg)
                
                append_author_operation_status(f"Sorry, the settings update failed: {error_msg}")
                try:
                    close_edge_window(hwnd)
                except:
                    pass
                return False
        else:
            print(f"\n{'='*60}")
            print("📝 [STAGE 2] Skipping settings update - no meaningful data")
            print(f"{'='*60}")
        
        # ============================================================
        # STAGE 3: Handle uploaded_jpgs_url data (Only if we have data)
        # ============================================================
        if has_uploadedjpgs_to_update:
            print(f"\n{'='*60}")
            print("📸 [STAGE 3] Processing uploaded_jpgs_url data...")
            print(f"{'='*60}")
            
            upload_success, upload_msg = send_uploadedjpgs_to_database(hwnd, uploaded_jpgs_data)
            
            if not upload_success:
                errors_encountered.append(upload_msg)
                append_author_operation_status(f"Sorry, the settings update failed to store uploaded JPGs data: {upload_msg}")
                try:
                    close_edge_window(hwnd)
                except:
                    pass
                return False
        else:
            print(f"\n{'='*60}")
            print("📸 [STAGE 3] Skipping uploaded_jpgs_url update - no meaningful data")
            print(f"{'='*60}")
        
        # ============================================================
        # STAGE 4: Reload page and confirm
        # ============================================================
        print(f"\n{'='*60}")
        print("📸 [STAGE 4] Reloading page...")
        print(f"{'='*60}")
        
        # Wait a moment for any background processing
        time.sleep(2)
        
        # Force a refresh to ensure the page shows updated state
        print("🔄 [FINAL] Refreshing page...")
        hwnd = enforce_window_focus(hwnd)
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(2)
        
        # Wait for page reload
        page_ready = wait_for_clipboard_content(
            expected_contains="page is ready",
            timeout=10,
            check_interval=0.5
        )
        
        if page_ready:
            print("✅ [FINAL] Page reloaded successfully")
        else:
            print("⚠️ [FINAL] Page reload may not have completed, but continuing...")
        
        uploadedjpgs_processed = True
        print("✅ [STAGE 4] Page reloaded successfully")
        
        # ============================================================
        # CLOSE EDGE WINDOW ON SUCCESS
        # ============================================================
        print(f"\n{'='*60}")
        print("🪟 [CLEANUP] Closing Edge window...")
        close_success = close_edge_window(hwnd)
        if close_success:
            print("✅ [CLEANUP] Edge window closed successfully")
        else:
            warning_msg = "The Edge browser window could not be closed gracefully. It may need to be closed manually."
            print(f"⚠️ {warning_msg}")
            warnings_encountered.append(warning_msg)
        
        # ============================================================
        # APPEND TO OPERATION_STATUS IN AUTHOR_PATH
        # ============================================================
        # Build success message with details of what was updated
        update_details = []
        if has_settings_to_update:
            update_details.append("settings updated")
        if has_uploadedjpgs_to_update:
            update_details.append(f"uploaded JPGs ({len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items) stored")
        
        # Get existing operation_status for display
        existing_operation = get_existing_operation_status()
        if existing_operation:
            print(f"\n📝 Existing operation_status found: {existing_operation[:100]}...")
        
        if warnings_encountered or errors_encountered:
            detailed_issues = []
            
            if errors_encountered:
                detailed_issues.append(f"Errors ({len(errors_encountered)}): " + "; ".join(errors_encountered))
            
            if warnings_encountered:
                detailed_issues.append(f"Warnings ({len(warnings_encountered)}): " + "; ".join(warnings_encountered))
            
            if errors_encountered:
                operation_msg = f"Sorry, the settings update encountered issues. Details: {'. '.join(detailed_issues)}. Please resolve these issues and try again."
                print(f"\n⚠️ Appending operation_status with error message")
                append_author_operation_status(operation_msg)
            else:
                operation_msg = f"Settings update completed successfully with {len(warnings_encountered)} specific warnings. Updated: {', '.join(update_details)}. Warnings: " + "; ".join(warnings_encountered)
                print(f"\n⚠️ Appending operation_status with warning message")
                append_author_operation_status(operation_msg)
        else:
            operation_msg = f"Settings update completed successfully. Updated: {', '.join(update_details)}."
            print(f"\n✅ Appending operation_status with success message")
            append_author_operation_status(operation_msg)
        
        # ============================================================
        # OPERATION COMPLETE
        # ============================================================
        print(f"\n{'='*60}")
        print("✅ [UPDATE] SETTINGS UPDATED SUCCESSFULLY!")
        
        if has_settings_to_update:
            print("📋 Settings: Updated successfully")
        else:
            print("📋 Settings: No data to update (skipped)")
        
        if has_uploadedjpgs_to_update:
            print(f"📸 Uploaded JPGs: {len(uploaded_jpgs_data) if isinstance(uploaded_jpgs_data, list) else 'unknown'} items stored")
        else:
            print("📸 Uploaded JPGs: No data to update (skipped)")
        
        if temp_file_path:
            print(f"📁 Temp file: {temp_file_path}")
        
        if warnings_encountered:
            print(f"\n⚠️ WARNINGS ({len(warnings_encountered)}):")
            for warning in warnings_encountered[:5]:
                print(f"    - {warning}")
            if len(warnings_encountered) > 5:
                print(f"    ... and {len(warnings_encountered) - 5} more warnings")
        
        if errors_encountered:
            print(f"\n❌ ERRORS ({len(errors_encountered)}):")
            for error in errors_encountered[:5]:
                print(f"    - {error}")
            if len(errors_encountered) > 5:
                print(f"    ... and {len(errors_encountered) - 5} more errors")
        
        print(f"{'='*60}\n")
        
        return len(errors_encountered) == 0
        
    except KeyboardInterrupt:
        print("🛑 [UPDATE] Operation interrupted by user")
        append_author_operation_status('The settings update operation was cancelled by the user. Please restart the process when ready.')
        try:
            close_edge_window(hwnd)
        except:
            pass
        return False
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"❌ [UPDATE] {error_msg}")
        import traceback
        traceback.print_exc()
        append_author_operation_status(f"Sorry, the settings update encountered an unexpected error: {str(e)}. Please check the logs for details.")
        try:
            close_edge_window(hwnd)
        except:
            pass
        return False
#=====


#Global functions
def reset_used_captions_record():
    """
    Resets the used captions tracking file when captions_state is 'mixed'.
    In mixed mode, captions can be reused so tracking is unnecessary.
    Only executes if status is 'pending' and captions_state is 'mixed'.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if critical errors occur
    """
    import os
    import json
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "reset_used_captions_record: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"reset_used_captions_record: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"reset_used_captions_record: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"reset_used_captions_record: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "reset_used_captions_record: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        captions_state = config.get('captions_state', 'mixed').lower().strip()
        
        print(f"reset_used_captions_record: Author: {author}")
        print(f"reset_used_captions_record: Captions State: {captions_state.upper()}")
        
    except Exception as e:
        error_msg = f"reset_used_captions_record: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: CHECK CAPTIONS STATE - Only reset if 'mixed'
    # ============================================================
    if captions_state != 'mixed':
        skip_msg = f"reset_used_captions_record: SKIPPED - Captions state is '{captions_state}', not 'mixed'. No reset needed."
        print(skip_msg)
        update_author_status('pending', skip_msg)
        return
    
    print(f"reset_used_captions_record: Captions state is 'mixed' - proceeding with reset...")

    # ============================================================
    # STEP 4: BUILD USED CAPTIONS FILE PATH
    # ============================================================
    used_captions_path = os.path.join(FILES_ROOT, "captions", author, "used_captions.json")
    
    print(f"reset_used_captions_record: Used captions tracking file: {used_captions_path}")

    # ============================================================
    # STEP 5: CHECK IF FILE EXISTS AND RESET
    # ============================================================
    count = 0
    
    if os.path.exists(used_captions_path):
        try:
            with open(used_captions_path, 'r', encoding='utf-8') as f:
                used_captions = json.load(f)
            
            if isinstance(used_captions, list):
                count = len(used_captions)
            elif isinstance(used_captions, dict):
                count = len(used_captions)
            else:
                count = 1 if used_captions else 0
            
            print(f"reset_used_captions_record: Found {count} used caption record(s)")
        except Exception as e:
            print(f"reset_used_captions_record: Warning - Could not read tracking file: {e}")
            count = 0
    else:
        print(f"reset_used_captions_record: No tracking file exists - nothing to reset")

    # ============================================================
    # STEP 6: RESET THE FILE (empty it)
    # ============================================================
    try:
        os.makedirs(os.path.dirname(used_captions_path), exist_ok=True)
        
        with open(used_captions_path, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2)
        
        if count > 0:
            print(f"✅ reset_used_captions_record: Cleared {count} used caption record(s)")
        else:
            print(f"✅ reset_used_captions_record: Tracking file reset (was already empty)")
        
        print(f"✅ reset_used_captions_record: All captions are now available for reuse")
        
    except Exception as e:
        error_msg = f"reset_used_captions_record: ERROR - Failed to reset tracking file: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 7: UPDATE STATUS
    # ============================================================
    if count > 0:
        operation_msg = (
            f"reset_used_captions_record: Reset used captions for author '{author}'. "
            f"Cleared {count} record(s). Captions state: {captions_state.upper()}. "
            f"SUCCESS: All captions available for reuse."
        )
    else:
        operation_msg = (
            f"reset_used_captions_record: Reset used captions for author '{author}'. "
            f"No records to clear. Captions state: {captions_state.upper()}. "
            f"SUCCESS: Tracking file is clean."
        )
    
    update_author_status('pending', operation_msg)
    
    # ============================================================
    # STEP 8: DISPLAY SUMMARY
    # ============================================================
    print(f"\n{'='*80}")
    print(f"RESET USED CAPTIONS RECORD - SUMMARY")
    print(f"{'='*80}")
    print(f"Author:              {author}")
    print(f"Captions State:      {captions_state.upper()}")
    print(f"Records Cleared:     {count}")
    print(f"Tracking File:       {used_captions_path}")
    print(f"Status:              pending ✅")
    print(f"{'='*80}\n")

def update_calendar():
    """Update the calendar and write to JSON, generating 12 months starting from current month.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if critical errors occur
    """
    import os
    import json
    import calendar
    from datetime import datetime

    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "update_calendar: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"update_calendar: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"update_calendar: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"update_calendar: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "update_calendar: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        time_order = config.get('time_order', '').strip()
        if not time_order:
            error_msg = "update_calendar: ERROR - 'time_order' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        time_order_type = config.get('time_order_type', {})
        if not time_order_type or not isinstance(time_order_type, dict):
            error_msg = "update_calendar: ERROR - 'time_order_type' is missing or invalid in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        if time_order not in time_order_type:
            error_msg = f"update_calendar: ERROR - Time order '{time_order}' not found in time_order_type."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        timeorders = time_order_type[time_order]
        if not timeorders or not isinstance(timeorders, list):
            error_msg = f"update_calendar: ERROR - Invalid time slots for time order '{time_order}'."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"update_calendar: Author: {author}, Time Order: {time_order}")
        print(f"update_calendar: Time slots loaded for '{time_order}':")
        for t in timeorders:
            print(f"  - {t['12hours']} ({t['24hours']})")
        
    except Exception as e:
        error_msg = f"update_calendar: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: GET CURRENT DATE AND TIME
    # ============================================================
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    current_time_12hour = now.strftime("%I:%M %p").lower()
    current_time_24hour = now.strftime("%H:%M")
    current_date = datetime.strptime(f"{current_day:02d}/{current_month:02d}/{current_year}", "%d/%m/%Y")
    
    print(f"\nupdate_calendar: Current date and time: {current_date.strftime('%d/%m/%Y')} {current_time_12hour} ({current_time_24hour})")
    
    # ============================================================
    # STEP 4: SORT TIME SLOTS AND FIND TODAY'S REMAINING SLOTS
    # ============================================================
    sorted_timeorders = sorted(timeorders, key=lambda x: x["24hours"])
    
    time_ahead_today = []
    current_time = datetime.strptime(current_time_24hour, "%H:%M")
    current_datetime = datetime.combine(current_date, current_time.time())
    
    print(f"\nupdate_calendar: Finding time slots after {current_time_24hour} for today...")
    for t in sorted_timeorders:
        slot_time = datetime.strptime(t["24hours"], "%H:%M")
        delta = slot_time - current_time
        minutes_distance = int(delta.total_seconds() / 60)
        
        if minutes_distance >= 0 and t["24hours"] != "00:00":
            consideration = f"passed {t['12hours']}" if minutes_distance >= 50 else f"skip {t['12hours']}"
            slot = {
                "id": f"{current_day:02d}_{t['24hours'].replace(':', '')}",
                "12hours": t["12hours"],
                "24hours": t["24hours"],
                "minutes_distance": minutes_distance,
                "consideration": consideration
            }
            time_ahead_today.append(slot)
            print(f"  Slot TODAY: {t['12hours']} ({t['24hours']}): id={slot['id']}, distance={minutes_distance}min, {consideration}")
    
    # ============================================================
    # STEP 5: GENERATE 12 MONTHS CALENDAR
    # ============================================================
    print(f"\nupdate_calendar: Generating 12-month calendar starting from {calendar.month_name[current_month]} {current_year}...")
    
    calendars = []
    year = current_year
    month = current_month
    total_days_processed = 0

    for i in range(12):
        if month > 12:
            month = 1
            year += 1

        month_name = calendar.month_name[month]
        month_calendar = calendar.monthcalendar(year, month)

        days_list = []
        for week_idx, week in enumerate(month_calendar):
            if any(day != 0 for day in week):
                week_data = {
                    "week": week_idx + 1,
                    "days": []
                }
                for day in week:
                    if day == 0:
                        week_data["days"].append({"day": None})
                        continue

                    date_str = f"{day:02d}/{month:02d}/{year}"
                    is_today = (year == current_year and month == current_month and day == current_day)
                    is_past_day = (year < current_year or 
                                 (year == current_year and month < current_month) or 
                                 (year == current_year and month == current_month and day < current_day))

                    time_12hour_display = current_time_12hour if is_today else "00:00 pm"
                    time_24hour_display = current_time_24hour if is_today else "00:00"

                    if is_today:
                        time_ahead = time_ahead_today
                    elif is_past_day:
                        time_ahead = []
                    else:
                        time_ahead = [
                            {
                                "id": f"{day:02d}_{t['24hours'].replace(':', '')}",
                                "12hours": t["12hours"],
                                "24hours": t["24hours"],
                                "minutes_distance": int((
                                    datetime.strptime(f"{day:02d}/{month:02d}/{year} {t['24hours']}", "%d/%m/%Y %H:%M")
                                    - current_datetime
                                ).total_seconds() / 60),
                                "consideration": f"passed {t['12hours']}"
                            } for t in sorted_timeorders
                        ]

                    day_data = {
                        "day": {
                            "date": date_str,
                            "time_12hour": time_12hour_display,
                            "time_24hour": time_24hour_display,
                            "time_ahead": time_ahead
                        }
                    }
                    week_data["days"].append(day_data)
                    total_days_processed += 1

                days_list.append(week_data)

        calendars.append({
            "year": year,
            "month": month_name,
            "days": days_list
        })

        month += 1

    # ============================================================
    # STEP 6: BUILD CALENDAR DATA STRUCTURE
    # ============================================================
    calendar_data = {
        "calendars": calendars
    }

    # ============================================================
    # STEP 7: SAVE CALENDAR TO JSON
    # ============================================================
    output_path = os.path.join(FILES_ROOT, "next jpg", author, "jsons", f"{time_order}_calendar.json")
    print(f"\nupdate_calendar: Writing calendar data to {output_path}")
    
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(calendar_data, f, indent=4, ensure_ascii=False)
        
        print(f"update_calendar: Calendar data successfully written to {output_path}")
        
    except Exception as e:
        error_msg = f"update_calendar: ERROR - Failed to write calendar JSON to {output_path}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 8: BUILD OPERATION STATUS AND UPDATE
    # ============================================================
    operation_parts = [
        f"update_calendar: Generated 12-month calendar for author '{author}'",
        f"Time Order: {time_order}",
        f"Time slots: {len(timeorders)}",
        f"Days processed: {total_days_processed}",
        f"Current time: {current_time_12hour} ({current_time_24hour})"
    ]
    
    if time_ahead_today:
        operation_parts.append(f"Slots available today: {len(time_ahead_today)}")
    else:
        operation_parts.append("No slots available today")
    
    operation_parts.append(f"Calendar saved to: {output_path}")
    operation_parts.append("SUCCESS: Calendar generated successfully")
    
    operation_msg = '; '.join(operation_parts)
    
    if update_author_status('pending', operation_msg):
        print(f"\n✅ Status updated to 'pending'")
    else:
        print(f"\n⚠️ Failed to update status in AUTHOR_PATH")

    # ============================================================
    # STEP 9: DISPLAY SUMMARY
    # ============================================================
    print(f"\n{'='*80}")
    print(f"UPDATE CALENDAR - SUMMARY")
    print(f"{'='*80}")
    print(f"Author:              {author}")
    print(f"Time Order:          {time_order}")
    print(f"Time Slots:          {len(timeorders)}")
    print(f"Days Processed:      {total_days_processed}")
    print(f"Today's Slots Left:  {len(time_ahead_today)}")
    print(f"Current Time:        {current_time_12hour} ({current_time_24hour})")
    print(f"Calendar Saved:      {output_path}")
    print(f"Status:              pending ✅")
    print(f"{'='*80}\n")
    
    # ============================================================
    # STEP 10: CALL TIMESCHEDULE UPDATE
    # ============================================================
    try:
        print("update_calendar: Calling update_timeschedule()...")
        update_timeschedule()
    except Exception as e:
        error_msg = f"update_calendar: ERROR - Failed to call update_timeschedule(): {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
      
def update_timeschedule():
    """Move next → last (OVERWRITE), generate NEW next_schedule starting AFTER schedule_date.
    
    If schedule_end_date is provided, only generate schedules up to that date.
    schedule_time_count tracks total time slots across the entire period.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if critical errors occur
    """
    import os
    import json
    from datetime import datetime, timedelta

    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "update_timeschedule: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"update_timeschedule: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"update_timeschedule: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"update_timeschedule: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "update_timeschedule: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        time_order = config.get('time_order', '').strip()
        if not time_order:
            error_msg = "update_timeschedule: ERROR - 'time_order' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        cardamount = int(config.get('cardamount', 1))
        schedule_date_str = config.get('schedule_date', '').strip()
        schedule_end_date_str = config.get('schedule_end_date', '').strip()
        
        time_order_type = config.get('time_order_type', {})
        if not time_order_type or not isinstance(time_order_type, dict):
            error_msg = "update_timeschedule: ERROR - 'time_order_type' is missing or invalid in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        if time_order not in time_order_type:
            error_msg = f"update_timeschedule: ERROR - Time order '{time_order}' not found in time_order_type."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        timeorders = time_order_type[time_order]
        if not timeorders or not isinstance(timeorders, list):
            error_msg = f"update_timeschedule: ERROR - Invalid time slots for time order '{time_order}'."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"update_timeschedule: Author: {author}, Time Order: {time_order}, Cardamount: {cardamount}")
        print(f"update_timeschedule: Schedule date: '{schedule_date_str}'")
        print(f"update_timeschedule: Schedule end date: '{schedule_end_date_str}'")
        
    except Exception as e:
        error_msg = f"update_timeschedule: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: VALIDATE SCHEDULE DATE (REQUIRED)
    # ============================================================
    if not schedule_date_str:
        error_msg = "update_timeschedule: ERROR - 'schedule_date' is missing or empty. This is required."
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # Parse schedule_date
    base_datetime = None
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(schedule_date_str.split('.')[0], fmt)
            if ' ' not in schedule_date_str:
                dt = dt.replace(hour=0, minute=0)
            base_datetime = dt
            print(f"update_timeschedule: Using schedule_date: {base_datetime.strftime('%d/%m/%Y %H:%M')}")
            break
        except ValueError:
            continue

    if base_datetime is None:
        error_msg = f"update_timeschedule: ERROR - Invalid schedule_date format: '{schedule_date_str}'. Expected DD/MM/YYYY HH:MM"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # Check if schedule_date is in the past
    now = datetime.now()
    if base_datetime < now:
        error_msg = f"update_timeschedule: ERROR - schedule_date '{base_datetime.strftime('%d/%m/%Y %H:%M')}' is in the past (current: {now.strftime('%d/%m/%Y %H:%M')})"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 4: PARSE SCHEDULE END DATE (OPTIONAL)
    # ============================================================
    end_datetime = None
    has_end_date = False
    
    if schedule_end_date_str:
        for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y"):
            try:
                dt = datetime.strptime(schedule_end_date_str.split('.')[0], fmt)
                if ' ' not in schedule_end_date_str:
                    dt = dt.replace(hour=23, minute=59)
                end_datetime = dt
                has_end_date = True
                print(f"update_timeschedule: Using schedule_end_date: {end_datetime.strftime('%d/%m/%Y %H:%M')}")
                break
            except ValueError:
                continue
        
        if end_datetime is None:
            print(f"update_timeschedule: WARNING - Invalid schedule_end_date format: '{schedule_end_date_str}'. Ignoring and continuing without end date.")
            has_end_date = False
            end_datetime = None
        elif end_datetime <= base_datetime:
            print(f"update_timeschedule: WARNING - schedule_end_date '{end_datetime.strftime('%d/%m/%Y %H:%M')}' is before or equal to schedule_date. Ignoring and continuing without end date.")
            has_end_date = False
            end_datetime = None

    # ============================================================
    # STEP 5: SORT TIME SLOTS AND BUILD TIME MAP
    # ============================================================
    timeorders = sorted(timeorders, key=lambda x: x["24hours"])
    valid_times_24 = [t["24hours"] for t in timeorders]
    time_map = {t["24hours"]: t["12hours"] for t in timeorders}

    print(f"update_timeschedule: Valid time slots for '{time_order}': {', '.join(valid_times_24)}")

    # ============================================================
    # STEP 6: SETUP FILE PATHS (NO post_filter)
    # ============================================================
    base_dir = os.path.join(FILES_ROOT, "next jpg", author, "jsons")
    
    calendar_path = os.path.join(base_dir, f"{time_order}_calendar.json")
    schedules_path = os.path.join(base_dir, f"{time_order}_schedules.json")

    # ============================================================
    # STEP 7: LOAD CALENDAR DATA
    # ============================================================
    if not os.path.exists(calendar_path):
        error_msg = f"update_timeschedule: ERROR - Calendar file missing: {calendar_path}. Run update_calendar() first."
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    try:
        with open(calendar_path, 'r', encoding='utf-8') as f:
            calendar_data = json.load(f)
        print(f"update_timeschedule: Calendar loaded from: {calendar_path}")
    except Exception as e:
        error_msg = f"update_timeschedule: ERROR - Failed to read calendar: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 8: LOAD EXISTING SCHEDULES
    # ============================================================
    old_last_schedule = []
    old_next_schedule = []
    if os.path.exists(schedules_path):
        try:
            with open(schedules_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            old_last_schedule = data.get("last_schedule", [])
            old_next_schedule = data.get("next_schedule", [])
            print(f"update_timeschedule: Loaded existing schedules: {len(old_last_schedule)} last, {len(old_next_schedule)} next")
        except Exception as e:
            print(f"update_timeschedule: Warning - Error reading schedules.json: {e}")

    # ============================================================
    # STEP 9: OVERWRITE LAST_SCHEDULE WITH OLD NEXT_SCHEDULE
    # ============================================================
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
            print(f"update_timeschedule: Migrated legacy: {item} → {migrated}")
        else:
            print(f"update_timeschedule: Skipping invalid schedule item: {item}")

    print(f"update_timeschedule: last_schedule updated with {len(new_last_schedule)} slot(s)")

    # ============================================================
    # STEP 10: BUILD USED IDS FROM NEW LAST_SCHEDULE
    # ============================================================
    used_ids = {slot.get("id") for slot in new_last_schedule if isinstance(slot, dict)}

    # ============================================================
    # STEP 11: GENERATE NEXT_SCHEDULE FROM CALENDAR DATA
    # ============================================================
    next_schedule_list = []
    total_time_slots = 0
    
    all_slots = []
    calendars = calendar_data.get('calendars', [])
    
    for month_data in calendars:
        days_list = month_data.get('days', [])
        
        for week_data in days_list:
            for day_data in week_data.get('days', []):
                day_info = day_data.get('day')
                if day_info is None:
                    continue
                
                date_str = day_info.get('date')
                time_ahead = day_info.get('time_ahead', [])
                
                for slot in time_ahead:
                    slot_id = slot.get('id')
                    slot_time_24 = slot.get('24hours')
                    slot_time_12 = slot.get('12hours')
                    
                    if slot_id and slot_time_24:
                        try:
                            slot_datetime = datetime.strptime(f"{date_str} {slot_time_24}", "%d/%m/%Y %H:%M")
                            
                            # Must be AFTER base_datetime
                            if slot_datetime > base_datetime:
                                # Check if within end date range (if provided)
                                if has_end_date and end_datetime:
                                    if slot_datetime > end_datetime:
                                        continue
                                
                                # Today: apply 50-minute buffer
                                if slot_datetime.date() == base_datetime.date():
                                    minutes_diff = (slot_datetime - base_datetime).total_seconds() / 60
                                    if minutes_diff < 50:
                                        continue
                                
                                if slot_id not in used_ids:
                                    all_slots.append({
                                        "id": slot_id,
                                        "date": date_str,
                                        "time_12hour": slot_time_12,
                                        "time_24hour": slot_time_24,
                                        "datetime": slot_datetime
                                    })
                                    total_time_slots += 1
                        except Exception:
                            continue
    
    # Sort by datetime
    all_slots.sort(key=lambda x: x['datetime'])
    
    # Take up to cardamount
    for slot in all_slots[:cardamount]:
        next_schedule_list.append({
            "id": slot["id"],
            "date": slot["date"],
            "time_12hour": slot["time_12hour"],
            "time_24hour": slot["time_24hour"]
        })
        used_ids.add(slot["id"])
        print(f"update_timeschedule: Added to next: {slot['date']} {slot['time_24hour']} ({slot['id']})")

    if not next_schedule_list:
        error_msg = f"update_timeschedule: ERROR - No available slots found after schedule_date for author '{author}'"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 12: WRITE SCHEDULES.JSON
    # ============================================================
    output_data = {
        "last_schedule": new_last_schedule,
        "next_schedule": next_schedule_list
    }
    
    try:
        os.makedirs(os.path.dirname(schedules_path), exist_ok=True)
        with open(schedules_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"update_timeschedule: Schedules written to {schedules_path}")
    except Exception as e:
        error_msg = f"update_timeschedule: ERROR - Failed to save schedules: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 13: UPDATE SCHEDULE_DATE IN CONFIG (24-hour format)
    # ============================================================
    new_schedule_date = None
    if next_schedule_list:
        last_slot = next_schedule_list[-1]
        try:
            new_schedule_date = datetime.strptime(
                f"{last_slot['date']} {last_slot['time_24hour']}",
                "%d/%m/%Y %H:%M"
            )
            
            # Update the config - write in 24-hour format
            if config_is_list:
                config_data[-1]['schedule_date'] = new_schedule_date.strftime("%d/%m/%Y %H:%M")
            else:
                config_data['schedule_date'] = new_schedule_date.strftime("%d/%m/%Y %H:%M")
            
            # ============================================================
            # STEP 14: HANDLE schedule_time_count (based on end date)
            # ============================================================
            if has_end_date and end_datetime:
                # Calculate total time slots across the entire period
                total_slots_count = 0
                
                # Re-scan all slots from base_datetime to end_datetime
                for month_data in calendars:
                    days_list = month_data.get('days', [])
                    
                    for week_data in days_list:
                        for day_data in week_data.get('days', []):
                            day_info = day_data.get('day')
                            if day_info is None:
                                continue
                            
                            date_str = day_info.get('date')
                            time_ahead = day_info.get('time_ahead', [])
                            
                            for slot in time_ahead:
                                slot_time_24 = slot.get('24hours')
                                
                                if slot_time_24:
                                    try:
                                        slot_datetime = datetime.strptime(f"{date_str} {slot_time_24}", "%d/%m/%Y %H:%M")
                                        
                                        # Count all slots within the range
                                        if base_datetime <= slot_datetime <= end_datetime:
                                            total_slots_count += 1
                                    except Exception:
                                        continue
                
                # Add schedule_time_count field
                if config_is_list:
                    config_data[-1]['schedule_time_count'] = total_slots_count
                else:
                    config_data['schedule_time_count'] = total_slots_count
                
                print(f"update_timeschedule: schedule_time_count set to: {total_slots_count}")
            else:
                # Remove schedule_time_count if it exists (no end date)
                if config_is_list:
                    if 'schedule_time_count' in config_data[-1]:
                        del config_data[-1]['schedule_time_count']
                        print("update_timeschedule: Removed schedule_time_count (no end date)")
                else:
                    if 'schedule_time_count' in config_data:
                        del config_data['schedule_time_count']
                        print("update_timeschedule: Removed schedule_time_count (no end date)")
            
            if save_json_file(AUTHOR_PATH, config_data):
                print(f"update_timeschedule: schedule_date updated to: {new_schedule_date.strftime('%d/%m/%Y %H:%M')}")
            else:
                error_msg = "update_timeschedule: ERROR - Failed to save updated schedule_date to AUTHOR_PATH"
                print(error_msg)
                update_author_status('aborted', error_msg)
                return
                
        except Exception as e:
            error_msg = f"update_timeschedule: ERROR - Failed to update schedule_date: {e}"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return

    # ============================================================
    # STEP 15: BUILD OPERATION STATUS AND UPDATE
    # ============================================================
    operation_parts = [
        f"update_timeschedule: Schedule generated for author '{author}'",
        f"Time Order: {time_order}",
        f"Cardamount: {cardamount}",
        f"Time slots: {len(timeorders)}",
        f"New last_schedule slots: {len(new_last_schedule)}",
        f"New next_schedule slots: {len(next_schedule_list)}",
        f"Start date: {base_datetime.strftime('%d/%m/%Y %H:%M')}",
        f"Last scheduled slot: {new_schedule_date.strftime('%d/%m/%Y %H:%M') if new_schedule_date else 'N/A'}"
    ]
    
    if has_end_date and end_datetime:
        operation_parts.append(f"End date: {end_datetime.strftime('%d/%m/%Y %H:%M')}")
        # Get schedule_time_count safely based on config type
        if config_is_list:
            time_count = config_data[-1].get('schedule_time_count', 0) if isinstance(config_data[-1], dict) else 0
        else:
            time_count = config_data.get('schedule_time_count', 0) if isinstance(config_data, dict) else 0
        operation_parts.append(f"Total time slots in period: {time_count}")
    
    operation_parts.append("SUCCESS: Schedule generated and archived successfully")
    operation_msg = '; '.join(operation_parts)
    
    if update_author_status('pending', operation_msg):
        print(f"\n✅ Status updated to 'pending'")
    else:
        print(f"\n⚠️ Failed to update status in AUTHOR_PATH")

    # ============================================================
    # STEP 16: DISPLAY SUMMARY
    # ============================================================
    print(f"\n{'='*80}")
    print(f"UPDATE TIMESCHEDULE - SUMMARY")
    print(f"{'='*80}")
    print(f"Author:              {author}")
    print(f"Time Order:          {time_order}")
    print(f"Cardamount:          {cardamount}")
    print(f"Time Slots:          {len(timeorders)}")
    print(f"Last Schedule:       {len(new_last_schedule)} slot(s)")
    print(f"Next Schedule:       {len(next_schedule_list)} slot(s)")
    print(f"Start Date:          {base_datetime.strftime('%d/%m/%Y %H:%M')}")
    if new_schedule_date:
        print(f"New Schedule Date:   {new_schedule_date.strftime('%d/%m/%Y %H:%M')}")
    if has_end_date and end_datetime:
        print(f"End Date:            {end_datetime.strftime('%d/%m/%Y %H:%M')}")
        # Get schedule_time_count safely for display
        if config_is_list:
            time_count = config_data[-1].get('schedule_time_count', 0) if isinstance(config_data[-1], dict) else 0
        else:
            time_count = config_data.get('schedule_time_count', 0) if isinstance(config_data, dict) else 0
        print(f"Total Time Slots:    {time_count}")
    else:
        print(f"End Date:            Not set (unlimited)")
    print(f"Schedules Saved:     {schedules_path}")
    print(f"Status:              pending ✅")
    print(f"{'='*80}\n")
    
    # Display next schedule slots
    if next_schedule_list:
        print("Next Schedule Slots:")
        for i, slot in enumerate(next_schedule_list, 1):
            print(f"  {i}. {slot['date']} {slot['time_12hour']} ({slot['time_24hour']}) - ID: {slot['id']}")
        print()

    # ============================================================
    # STEP 17: OPTIONAL - RANDOMIZE MINUTES
    # ============================================================
    try:
        print("update_timeschedule: Calling randomize_next_schedule_minutes()...")
        randomize_next_schedule_minutes()
    except NameError:
        pass
    except Exception as e:
        error_msg = f"update_timeschedule: ERROR - Failed to randomize minutes: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)

    # ============================================================
    # STEP 18: OPTIONAL - RANDOMIZE HOURS
    # ============================================================
    try:
        print("update_timeschedule: Calling randomize_next_schedule_hours()...")
        randomize_next_schedule_hours()
    except NameError:
        pass
    except Exception as e:
        error_msg = f"update_timeschedule: ERROR - Failed to randomize hours: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
           
def randomize_next_schedule_minutes():
    """
    Randomize minutes (01–30) for EACH slot in next_schedule using its OWN hour.
    Preserves original hour, only changes minutes.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending' AND randomize_schedule_minutes is true
    If randomize_schedule_minutes is false, simply skips without changing status
    Sets status to 'aborted' only if critical errors occur during operation
    """
    import os
    import json
    import random
    from datetime import datetime

    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def parse_boolean_value(value):
        """
        Parse a value to boolean, handling strings, booleans, and other types.
        Returns True for: True, 'true', '1', 'yes', 'on'
        Returns False for: False, 'false', '0', 'no', 'off', None, empty
        """
        if value is None:
            return False
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, (int, float)):
            return bool(value)
        
        if isinstance(value, str):
            value_lower = value.lower().strip()
            # True values
            if value_lower in ('true', '1', 'yes', 'on', 'y', 't'):
                return True
            # False values
            if value_lower in ('false', '0', 'no', 'off', 'n', 'f', ''):
                return False
            # If it's any other non-empty string, treat as True
            return bool(value_lower)
        
        # For any other type, convert to boolean
        return bool(value)

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "randomize_next_schedule_minutes: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"randomize_next_schedule_minutes: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"randomize_next_schedule_minutes: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"randomize_next_schedule_minutes: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: CHECK randomize_schedule_minutes FIELD
    # ============================================================
    try:
        # Get the randomize_schedule_minutes value from config
        randomize_enabled = config.get('randomize_schedule_minutes', False)
        
        # Also check in dynamic_values if present
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_randomize = config['dynamic_values'].get('randomize_schedule_minutes')
            if dyn_randomize is not None:
                randomize_enabled = dyn_randomize
        
        # Parse the value (handles string 'false', 'true', etc.)
        randomize_enabled_bool = parse_boolean_value(randomize_enabled)
        
        print(f"randomize_next_schedule_minutes: randomize_schedule_minutes = '{randomize_enabled}' (parsed as: {randomize_enabled_bool})")
        
        if not randomize_enabled_bool:
            print(f"randomize_next_schedule_minutes: SKIPPED - 'randomize_schedule_minutes' is disabled (value: '{randomize_enabled}'). No status changes made.")
            return  # Just skip, don't touch status
        
        print(f"randomize_next_schedule_minutes: 'randomize_schedule_minutes' is enabled - proceeding...")
        
    except Exception as e:
        error_msg = f"randomize_next_schedule_minutes: ERROR - Failed to check randomize_schedule_minutes flag: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "randomize_next_schedule_minutes: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        time_order = config.get('time_order', '').strip()
        if not time_order:
            error_msg = "randomize_next_schedule_minutes: ERROR - 'time_order' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"randomize_next_schedule_minutes: Author: {author}, Time Order: {time_order}")
        
    except Exception as e:
        error_msg = f"randomize_next_schedule_minutes: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 4: BUILD SCHEDULES PATH (NO post_filter)
    # ============================================================
    schedules_path = os.path.join(FILES_ROOT, "next jpg", author, "jsons", f"{time_order}_schedules.json")
    
    print(f"randomize_next_schedule_minutes: Looking for schedules at: {schedules_path}")

    if not os.path.exists(schedules_path):
        error_msg = f"randomize_next_schedule_minutes: ERROR - schedules.json not found: {schedules_path}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 5: READ SCHEDULES
    # ============================================================
    try:
        with open(schedules_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"randomize_next_schedule_minutes: Schedules loaded from: {schedules_path}")
    except Exception as e:
        error_msg = f"randomize_next_schedule_minutes: ERROR - Failed to read schedules: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 6: CHECK NEXT_SCHEDULE EXISTS
    # ============================================================
    if 'next_schedule' not in data or not data['next_schedule']:
        error_msg = f"randomize_next_schedule_minutes: ERROR - No 'next_schedule' found in schedules for author '{author}'"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    schedule_list = data['next_schedule']
    if isinstance(schedule_list, dict):
        schedule_list = [schedule_list]
    
    if not schedule_list:
        error_msg = f"randomize_next_schedule_minutes: ERROR - 'next_schedule' is empty for author '{author}'"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    print(f"randomize_next_schedule_minutes: Found {len(schedule_list)} slot(s) to randomize")

    # ============================================================
    # STEP 7: RANDOMIZE MINUTES FOR EACH SLOT
    # ============================================================
    updated_slots = []
    failed_slots = 0

    for slot in schedule_list:
        try:
            old_time = slot.get('time_24hour')
            if not old_time or ':' not in old_time:
                print(f"randomize_next_schedule_minutes: Invalid time_24hour in slot: {slot}")
                failed_slots += 1
                continue

            # Extract hour from original time
            hour = int(old_time.split(':')[0])
            
            # Generate random minutes (01-30)
            new_min = random.randint(1, 30)
            new_time_24 = f"{hour:02d}:{new_min:02d}"

            # Format 12-hour time
            dt = datetime.strptime(new_time_24, "%H:%M")
            new_time_12 = dt.strftime("%I:%M %p").lstrip("0").lower()
            
            # Clean up formatting
            if new_time_12.startswith("0"):
                new_time_12 = new_time_12[1:]

            # Update slot with new times
            old_time_12 = slot.get('time_12hour', '')
            slot["time_24hour"] = new_time_24
            slot["time_12hour"] = new_time_12
            
            updated_slots.append(f"{slot['date']} {old_time} → {new_time_24}")
            
            print(f"  Randomized: {slot['date']} {old_time} ({old_time_12}) → {new_time_24} ({new_time_12})")

        except Exception as e:
            print(f"randomize_next_schedule_minutes: Failed to process slot {slot}: {e}")
            failed_slots += 1
            continue

    if not updated_slots:
        error_msg = f"randomize_next_schedule_minutes: ERROR - No slots could be randomized for author '{author}'"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 8: WRITE UPDATED SCHEDULES BACK
    # ============================================================
    try:
        with open(schedules_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nrandomize_next_schedule_minutes: Successfully randomized {len(updated_slots)} slot(s)")
        print(f"randomize_next_schedule_minutes: Schedules saved to: {schedules_path}")
    except Exception as e:
        error_msg = f"randomize_next_schedule_minutes: ERROR - Failed to save schedules: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 9: BUILD OPERATION STATUS AND UPDATE
    # ============================================================
    operation_parts = [
        f"randomize_next_schedule_minutes: Randomized schedule for author '{author}'",
        f"Time Order: {time_order}",
        f"Total slots randomized: {len(updated_slots)}",
        f"Failed slots: {failed_slots}"
    ]
    
    # Add sample of randomized times
    if updated_slots:
        sample = updated_slots[:3]
        operation_parts.append(f"Sample: {'; '.join(sample)}")
        if len(updated_slots) > 3:
            operation_parts.append(f"... and {len(updated_slots) - 3} more slots")
    
    if failed_slots > 0:
        operation_parts.append(f"WARNING: {failed_slots} slots failed to randomize")
        status_value = 'pending'  # Still pending but with warnings
    else:
        operation_parts.append("SUCCESS: All slots randomized successfully")
        status_value = 'pending'
    
    operation_msg = '; '.join(operation_parts)
    
    if update_author_status(status_value, operation_msg):
        print(f"\n✅ Status updated to '{status_value}'")
    else:
        print(f"\n⚠️ Failed to update status in AUTHOR_PATH")

    # ============================================================
    # STEP 10: DISPLAY SUMMARY
    # ============================================================
    print(f"\n{'='*80}")
    print(f"RANDOMIZE NEXT SCHEDULE MINUTES - SUMMARY")
    print(f"{'='*80}")
    print(f"Author:              {author}")
    print(f"Time Order:          {time_order}")
    print(f"Slots Randomized:    {len(updated_slots)}")
    print(f"Failed Slots:        {failed_slots}")
    print(f"Schedules Saved:     {schedules_path}")
    print(f"Status:              {status_value} ✅")
    print(f"{'='*80}")
    
    if updated_slots:
        print(f"\nRandomized Slots (first 10):")
        for i, slot in enumerate(updated_slots[:10], 1):
            print(f"  {i}. {slot}")
        if len(updated_slots) > 10:
            print(f"  ... and {len(updated_slots) - 10} more")
        print()
    
    if failed_slots > 0:
        print(f"⚠️ {failed_slots} slot(s) failed to randomize. Check logs above for details.\n")

def randomize_next_schedule_hours():
    """
    Randomize hours (00–23) AND minutes (01–30) for EACH slot in next_schedule.
    Completely randomizes the time while keeping the date.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending' AND randomize_schedule_hours is true
    If randomize_schedule_hours is false, simply skips without changing status
    Sets status to 'aborted' only if critical errors occur during operation
    """
    import os
    import json
    import random
    from datetime import datetime

    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def parse_boolean_value(value):
        """
        Parse a value to boolean, handling strings, booleans, and other types.
        Returns True for: True, 'true', '1', 'yes', 'on'
        Returns False for: False, 'false', '0', 'no', 'off', None, empty
        """
        if value is None:
            return False
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, (int, float)):
            return bool(value)
        
        if isinstance(value, str):
            value_lower = value.lower().strip()
            # True values
            if value_lower in ('true', '1', 'yes', 'on', 'y', 't'):
                return True
            # False values
            if value_lower in ('false', '0', 'no', 'off', 'n', 'f', ''):
                return False
            # If it's any other non-empty string, treat as True
            return bool(value_lower)
        
        # For any other type, convert to boolean
        return bool(value)

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "randomize_next_schedule_hours: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"randomize_next_schedule_hours: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"randomize_next_schedule_hours: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"randomize_next_schedule_hours: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: CHECK randomize_schedule_hours FIELD
    # ============================================================
    try:
        # Get the randomize_schedule_hours value from config
        randomize_enabled = config.get('randomize_schedule_hours', False)
        
        # Also check in dynamic_values if present
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_randomize = config['dynamic_values'].get('randomize_schedule_hours')
            if dyn_randomize is not None:
                randomize_enabled = dyn_randomize
        
        # Parse the value (handles string 'false', 'true', etc.)
        randomize_enabled_bool = parse_boolean_value(randomize_enabled)
        
        print(f"randomize_next_schedule_hours: randomize_schedule_hours = '{randomize_enabled}' (parsed as: {randomize_enabled_bool})")
        
        if not randomize_enabled_bool:
            print(f"randomize_next_schedule_hours: SKIPPED - 'randomize_schedule_hours' is disabled (value: '{randomize_enabled}'). No status changes made.")
            return  # Just skip, don't touch status
        
        print(f"randomize_next_schedule_hours: 'randomize_schedule_hours' is enabled - proceeding...")
        
    except Exception as e:
        error_msg = f"randomize_next_schedule_hours: ERROR - Failed to check randomize_schedule_hours flag: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "randomize_next_schedule_hours: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        time_order = config.get('time_order', '').strip()
        if not time_order:
            error_msg = "randomize_next_schedule_hours: ERROR - 'time_order' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"randomize_next_schedule_hours: Author: {author}, Time Order: {time_order}")
        
    except Exception as e:
        error_msg = f"randomize_next_schedule_hours: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 4: BUILD SCHEDULES PATH (NO post_filter)
    # ============================================================
    schedules_path = os.path.join(FILES_ROOT, "next jpg", author, "jsons", f"{time_order}_schedules.json")
    
    print(f"randomize_next_schedule_hours: Looking for schedules at: {schedules_path}")

    if not os.path.exists(schedules_path):
        error_msg = f"randomize_next_schedule_hours: ERROR - schedules.json not found: {schedules_path}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 5: READ SCHEDULES
    # ============================================================
    try:
        with open(schedules_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"randomize_next_schedule_hours: Schedules loaded from: {schedules_path}")
    except Exception as e:
        error_msg = f"randomize_next_schedule_hours: ERROR - Failed to read schedules: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 6: CHECK NEXT_SCHEDULE EXISTS
    # ============================================================
    if 'next_schedule' not in data or not data['next_schedule']:
        error_msg = f"randomize_next_schedule_hours: ERROR - No 'next_schedule' found in schedules for author '{author}'"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    schedule_list = data['next_schedule']
    if isinstance(schedule_list, dict):
        schedule_list = [schedule_list]
    
    if not schedule_list:
        error_msg = f"randomize_next_schedule_hours: ERROR - 'next_schedule' is empty for author '{author}'"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    print(f"randomize_next_schedule_hours: Found {len(schedule_list)} slot(s) to randomize")

    # ============================================================
    # STEP 7: RANDOMIZE HOURS AND MINUTES FOR EACH SLOT
    # ============================================================
    updated_slots = []
    failed_slots = 0

    for slot in schedule_list:
        try:
            old_time = slot.get('time_24hour')
            old_time_12 = slot.get('time_12hour', '')
            
            if not old_time or ':' not in old_time:
                print(f"randomize_next_schedule_hours: Invalid time_24hour in slot: {slot}")
                failed_slots += 1
                continue

            # Generate random hour (00-23)
            new_hour = random.randint(0, 23)
            
            # Generate random minutes (01-30)
            new_min = random.randint(1, 30)
            
            new_time_24 = f"{new_hour:02d}:{new_min:02d}"

            # Format 12-hour time
            dt = datetime.strptime(new_time_24, "%H:%M")
            new_time_12 = dt.strftime("%I:%M %p").lstrip("0").lower()
            
            # Clean up formatting
            if new_time_12.startswith("0"):
                new_time_12 = new_time_12[1:]

            # Update slot with new times
            slot["time_24hour"] = new_time_24
            slot["time_12hour"] = new_time_12
            
            # Also update the ID to reflect new time
            old_id = slot.get('id', '')
            if old_id and '_' in old_id:
                date_part = old_id.split('_')[0]
                new_id = f"{date_part}_{new_time_24.replace(':', '')}"
                slot['id'] = new_id
            
            updated_slots.append(f"{slot['date']} {old_time} → {new_time_24}")
            
            print(f"  Randomized: {slot['date']} {old_time} ({old_time_12}) → {new_time_24} ({new_time_12})")

        except Exception as e:
            print(f"randomize_next_schedule_hours: Failed to process slot {slot}: {e}")
            failed_slots += 1
            continue

    if not updated_slots:
        error_msg = f"randomize_next_schedule_hours: ERROR - No slots could be randomized for author '{author}'"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 8: WRITE UPDATED SCHEDULES BACK
    # ============================================================
    try:
        with open(schedules_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nrandomize_next_schedule_hours: Successfully randomized {len(updated_slots)} slot(s)")
        print(f"randomize_next_schedule_hours: Schedules saved to: {schedules_path}")
    except Exception as e:
        error_msg = f"randomize_next_schedule_hours: ERROR - Failed to save schedules: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 9: BUILD OPERATION STATUS AND UPDATE
    # ============================================================
    operation_parts = [
        f"randomize_next_schedule_hours: Randomized hours and minutes for author '{author}'",
        f"Time Order: {time_order}",
        f"Total slots randomized: {len(updated_slots)}",
        f"Failed slots: {failed_slots}"
    ]
    
    # Add sample of randomized times
    if updated_slots:
        sample = updated_slots[:3]
        operation_parts.append(f"Sample: {'; '.join(sample)}")
        if len(updated_slots) > 3:
            operation_parts.append(f"... and {len(updated_slots) - 3} more slots")
    
    if failed_slots > 0:
        operation_parts.append(f"WARNING: {failed_slots} slots failed to randomize")
        status_value = 'pending'  # Still pending but with warnings
    else:
        operation_parts.append("SUCCESS: All slots randomized successfully")
        status_value = 'pending'
    
    operation_msg = '; '.join(operation_parts)
    
    if update_author_status(status_value, operation_msg):
        print(f"\n✅ Status updated to '{status_value}'")
    else:
        print(f"\n⚠️ Failed to update status in AUTHOR_PATH")

    # ============================================================
    # STEP 10: DISPLAY SUMMARY
    # ============================================================
    print(f"\n{'='*80}")
    print(f"RANDOMIZE NEXT SCHEDULE HOURS - SUMMARY")
    print(f"{'='*80}")
    print(f"Author:              {author}")
    print(f"Time Order:          {time_order}")
    print(f"Slots Randomized:    {len(updated_slots)}")
    print(f"Failed Slots:        {failed_slots}")
    print(f"Schedules Saved:     {schedules_path}")
    print(f"Status:              {status_value} ✅")
    print(f"{'='*80}")
    
    if updated_slots:
        print(f"\nRandomized Slots (first 10):")
        for i, slot in enumerate(updated_slots[:10], 1):
            print(f"  {i}. {slot}")
        if len(updated_slots) > 10:
            print(f"  ... and {len(updated_slots) - 10} more")
        print()
    
    if failed_slots > 0:
        print(f"⚠️ {failed_slots} slot(s) failed to randomize. Check logs above for details.\n")

def check_schedule_time():
    """Check if the next schedule in schedules.json is behind the current time.
    If behind, calls update_timeschedule() to rebuild.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if critical errors occur
    """
    import os
    import json
    from datetime import datetime

    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "check_schedule_time: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"check_schedule_time: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"check_schedule_time: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"check_schedule_time: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "check_schedule_time: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        time_order = config.get('time_order', '').strip()
        if not time_order:
            error_msg = "check_schedule_time: ERROR - 'time_order' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"check_schedule_time: Author: {author}, Time Order: {time_order}")
        
    except Exception as e:
        error_msg = f"check_schedule_time: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: GET CURRENT DATE AND TIME
    # ============================================================
    now = datetime.now()
    current_time_24hour = now.strftime("%H:%M")
    current_date = now.strftime("%d/%m/%Y")
    current_datetime = datetime.strptime(f"{current_date} {current_time_24hour}", "%d/%m/%Y %H:%M")
    
    print(f"\ncheck_schedule_time: Current time: {current_date} {current_time_24hour}")

    # ============================================================
    # STEP 4: BUILD SCHEDULES PATH (NO post_filter)
    # ============================================================
    schedules_path = os.path.join(FILES_ROOT, "next jpg", author, "jsons", f"{time_order}_schedules.json")
    
    print(f"check_schedule_time: Looking for schedules at: {schedules_path}")

    # ============================================================
    # STEP 5: CHECK IF SCHEDULES FILE EXISTS
    # ============================================================
    if not os.path.exists(schedules_path):
        warning_msg = f"check_schedule_time: WARNING - schedules.json not found at {schedules_path}. Calling update_calendar() to generate..."
        print(warning_msg)
        update_author_status('pending', warning_msg)
        
        try:
            update_calendar()
        except Exception as e:
            error_msg = f"check_schedule_time: ERROR - Failed to call update_calendar(): {e}"
            print(error_msg)
            update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 6: LOAD SCHEDULES
    # ============================================================
    try:
        with open(schedules_path, 'r', encoding='utf-8') as f:
            schedules_data = json.load(f)
        print(f"check_schedule_time: Schedules loaded from: {schedules_path}")
    except json.JSONDecodeError:
        error_msg = f"check_schedule_time: ERROR - schedules.json contains invalid JSON at {schedules_path}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    except Exception as e:
        error_msg = f"check_schedule_time: ERROR - Failed to read schedules: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 7: CHECK FOR NEXT_SCHEDULE
    # ============================================================
    if 'next_schedule' not in schedules_data or not schedules_data['next_schedule']:
        warning_msg = f"check_schedule_time: WARNING - 'next_schedule' missing or empty in schedules. Calling update_timeschedule() to rebuild..."
        print(warning_msg)
        update_author_status('pending', warning_msg)
        
        try:
            update_timeschedule()
        except Exception as e:
            error_msg = f"check_schedule_time: ERROR - Failed to call update_timeschedule(): {e}"
            print(error_msg)
            update_author_status('aborted', error_msg)
        return

    next_schedule_list = schedules_data['next_schedule']

    # ============================================================
    # STEP 8: EXTRACT FIRST SLOT FROM NEXT_SCHEDULE
    # ============================================================
    try:
        if isinstance(next_schedule_list, list):
            if not next_schedule_list:
                warning_msg = "check_schedule_time: WARNING - 'next_schedule' list is empty. Calling update_timeschedule() to rebuild..."
                print(warning_msg)
                update_author_status('pending', warning_msg)
                
                try:
                    update_timeschedule()
                except Exception as e:
                    error_msg = f"check_schedule_time: ERROR - Failed to call update_timeschedule(): {e}"
                    print(error_msg)
                    update_author_status('aborted', error_msg)
                return
            
            next_schedule = next_schedule_list[0]
        elif isinstance(next_schedule_list, dict):
            next_schedule = next_schedule_list
        else:
            error_msg = "check_schedule_time: ERROR - Invalid 'next_schedule' format in schedules."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
            
        next_schedule_date = next_schedule.get('date', '')
        next_schedule_time = next_schedule.get('time_24hour', '')
        
        if not next_schedule_date or not next_schedule_time:
            error_msg = "check_schedule_time: ERROR - Invalid next_schedule format: missing date or time."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
            
        next_schedule_datetime = datetime.strptime(
            f"{next_schedule_date} {next_schedule_time}", 
            "%d/%m/%Y %H:%M"
        )
        
        print(f"check_schedule_time: Next scheduled slot: {next_schedule_date} {next_schedule_time}")
        
    except ValueError as e:
        error_msg = f"check_schedule_time: ERROR - Invalid date or time format in next_schedule: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    except Exception as e:
        error_msg = f"check_schedule_time: ERROR - Failed to parse next_schedule: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 9: COMPARE WITH CURRENT TIME
    # ============================================================
    if next_schedule_datetime < current_datetime:
        # Schedule is behind - needs rebuild
        time_diff_minutes = (current_datetime - next_schedule_datetime).total_seconds() / 60
        
        print(f"\n⚠️ Next schedule is BEHIND current time!")
        print(f"   Current:  {current_date} {current_time_24hour}")
        print(f"   Scheduled: {next_schedule_date} {next_schedule_time}")
        print(f"   Behind by: {time_diff_minutes:.0f} minutes")
        print(f"   Action: Calling update_timeschedule() to rebuild...")
        
        operation_parts = [
            f"check_schedule_time: Schedule behind for author '{author}'",
            f"Time Order: {time_order}",
            f"Current time: {current_date} {current_time_24hour}",
            f"Next scheduled: {next_schedule_date} {next_schedule_time}",
            f"Behind by: {time_diff_minutes:.0f} minutes",
            "Action: Calling update_timeschedule() to rebuild schedule"
        ]
        operation_msg = '; '.join(operation_parts)
        update_author_status('pending', operation_msg)
        
        try:
            update_timeschedule()
        except Exception as e:
            error_msg = f"check_schedule_time: ERROR - Failed to call update_timeschedule(): {e}"
            print(error_msg)
            update_author_status('aborted', error_msg)
        
    else:
        # Schedule is valid - still ahead
        minutes_until = (next_schedule_datetime - current_datetime).total_seconds() / 60
        
        print(f"\n✅ Next schedule is VALID (still ahead)")
        print(f"   Current:  {current_date} {current_time_24hour}")
        print(f"   Scheduled: {next_schedule_date} {next_schedule_time}")
        print(f"   Minutes until: {minutes_until:.0f}")
        print(f"   Action: No action needed - schedule is valid")
        
        operation_parts = [
            f"check_schedule_time: Schedule valid for author '{author}'",
            f"Time Order: {time_order}",
            f"Current time: {current_date} {current_time_24hour}",
            f"Next scheduled: {next_schedule_date} {next_schedule_time}",
            f"Minutes until next slot: {minutes_until:.0f}",
            "SUCCESS: Schedule is on track"
        ]
        operation_msg = '; '.join(operation_parts)
        update_author_status('pending', operation_msg)

    # ============================================================
    # STEP 10: DISPLAY SUMMARY
    # ============================================================
    print(f"\n{'='*80}")
    print(f"CHECK SCHEDULE TIME - SUMMARY")
    print(f"{'='*80}")
    print(f"Author:              {author}")
    print(f"Time Order:          {time_order}")
    print(f"Current Time:        {current_date} {current_time_24hour}")
    print(f"Next Scheduled:      {next_schedule_date} {next_schedule_time}")
    
    if next_schedule_datetime < current_datetime:
        time_diff = (current_datetime - next_schedule_datetime).total_seconds() / 60
        print(f"Status:              ⚠️ BEHIND by {time_diff:.0f} minutes")
        print(f"Action Taken:        Called update_timeschedule()")
    else:
        time_until = (next_schedule_datetime - current_datetime).total_seconds() / 60
        print(f"Status:              ✅ AHEAD by {time_until:.0f} minutes")
        print(f"Action Taken:        None needed")
    
    print(f"Status in Config:    pending ✅")
    print(f"{'='*80}\n")

def validate_image_urls():
    """
    Validates URLs in jpgsurl field by checking if they point to actual images.
    - For HTTP URLs: Uses HEAD requests to check Content-Type
    - For local paths: Opens file with Pillow to verify it's a real image
    Removes invalid URLs from the jpgsurl field in AUTHOR_PATH.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending' AND validate_images_url is True
    Sets status to 'aborted' if critical errors occur or not enough valid URLs remain
    """
    import os
    import json
    import requests
    from urllib.parse import urlparse
    from PIL import Image
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        return default if default is not None else {}
                    return json.loads(content)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def parse_jpgs_url_field(jpgs_field):
        """Parse the jpgsurl field which can be a dict or string. Returns list of URLs/paths."""
        if not jpgs_field:
            return []
        
        if isinstance(jpgs_field, dict):
            urls = []
            for key, value in jpgs_field.items():
                if isinstance(value, str):
                    items = [u.strip() for u in value.split(',') if u.strip()]
                    urls.extend(items)
                elif isinstance(value, list):
                    urls.extend([str(u).strip() for u in value if u])
            return urls
        
        if isinstance(jpgs_field, str):
            return [u.strip() for u in jpgs_field.split(',') if u.strip()]
        
        return []
    
    def rebuild_jpgsurl_field(valid_urls, original_field):
        """Rebuild the jpgsurl field maintaining its original format"""
        if isinstance(original_field, dict):
            # For dict, just use all valid URLs under the first (or only) key
            result = {}
            for key in original_field.keys():
                result[key] = ', '.join(valid_urls)
                break  # Only one key needed
            return result
        elif isinstance(original_field, str):
            return ', '.join(valid_urls)
        return valid_urls
    
    def is_http_url(url):
        """Check if the URL/path is an HTTP/HTTPS URL"""
        return url.lower().startswith(('http://', 'https://'))
    
    def validate_http_url(url, timeout=10):
        """Validate an HTTP URL by checking Content-Type header."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "", "Invalid URL structure"
        except Exception:
            return False, "", "Cannot parse URL"
        
        path = parsed.path.lower()
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg')
        has_image_ext = path.endswith(image_extensions)
        
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        
        content_type = ""
        
        # Try HEAD request first
        try:
            response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '').lower()
            elif response.status_code in (403, 405):
                raise Exception(f"HTTP {response.status_code}")
            elif response.status_code >= 400:
                return False, "", f"HTTP {response.status_code}"
        except Exception:
            # Try GET with stream
            try:
                response = requests.get(
                    url, headers=headers, timeout=timeout, 
                    allow_redirects=True, stream=True
                )
                response.close()
                
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '').lower()
                else:
                    return False, "", f"HTTP {response.status_code}"
            except Exception as e:
                return False, "", f"Connection failed: {str(e)[:50]}"
        
        # Check Content-Type
        if content_type:
            image_mime_types = [
                'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
                'image/webp', 'image/bmp', 'image/svg+xml', 'image/tiff',
                'image/x-icon', 'image/vnd.microsoft.icon'
            ]
            
            is_image_mime = any(content_type.startswith(mime) for mime in image_mime_types)
            
            if is_image_mime:
                return True, f"Valid image: {content_type}", ""
            else:
                if has_image_ext:
                    return True, f"Has image extension (Content-Type: {content_type})", ""
                else:
                    return False, content_type, f"Not an image type: {content_type}"
        else:
            if has_image_ext:
                return True, "Has image extension (no Content-Type)", ""
            else:
                return False, "", "No Content-Type and no image extension"
    
    def validate_local_file(file_path):
        """Validate a local file path by checking if file exists and is a real image."""
        possible_paths = [
            file_path,
            os.path.join(FILES_ROOT, file_path),
        ]
        
        found_path = None
        for path in possible_paths:
            if os.path.exists(path) and os.path.isfile(path):
                found_path = path
                break
        
        if not found_path:
            return False, "", f"File not found: {file_path}"
        
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')
        if not found_path.lower().endswith(image_extensions):
            return False, "", f"Not an image extension: {os.path.splitext(found_path)[1]}"
        
        try:
            with Image.open(found_path) as img:
                img.verify()
            with Image.open(found_path) as img:
                img.load()
                width, height = img.size
                mode = img.mode
            
            file_size = os.path.getsize(found_path)
            return True, f"Valid image: {width}x{height} {mode} ({file_size:,} bytes)", ""
        except Exception as e:
            return False, "", f"Corrupted or invalid image: {str(e)[:50]}"
    
    def parse_boolean_value(value):
        """
        Parse a value to boolean, handling strings, booleans, and other types.
        Returns True for: True, 'true', '1', 'yes', 'on'
        Returns False for: False, 'false', '0', 'no', 'off', None, empty
        """
        if value is None:
            return False
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, (int, float)):
            return bool(value)
        
        if isinstance(value, str):
            value_lower = value.lower().strip()
            # True values
            if value_lower in ('true', '1', 'yes', 'on', 'y', 't'):
                return True
            # False values
            if value_lower in ('false', '0', 'no', 'off', 'n', 'f', ''):
                return False
            # If it's any other non-empty string, treat as True
            return bool(value_lower)
        
        # For any other type, convert to boolean
        return bool(value)
    
    # ============================================================
    # STEP 1: CHECK STATUS FIRST
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "validate_image_urls: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"validate_image_urls: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"validate_image_urls: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"validate_image_urls: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 2: CHECK validate_images_url FLAG
    # ============================================================
    try:
        # Get the validate_images_url value from config
        validate_images_url = config.get('validate_images_url', False)
        
        # Also check in dynamic_values if present
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_validate = config['dynamic_values'].get('validate_images_url')
            if dyn_validate is not None:
                validate_images_url = dyn_validate
        
        # Parse the value (handles string 'false', 'true', etc.)
        validate_images_url_bool = parse_boolean_value(validate_images_url)
        
        print(f"validate_image_urls: validate_images_url = '{validate_images_url}' (parsed as: {validate_images_url_bool})")
        
        if not validate_images_url_bool:
            print(f"validate_image_urls: SKIPPED - 'validate_images_url' is False. Function only executes when this flag is True.")
            return
            
        print(f"validate_image_urls: 'validate_images_url' is True - proceeding...")
        
    except Exception as e:
        error_msg = f"validate_image_urls: ERROR - Failed to check validate_images_url flag: {e}"
        print(error_msg)
        # Don't update status or touch anything, just return
        return
    
    # ============================================================
    # STEP 3: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "validate_image_urls: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        try:
            cardamount = max(1, int(config.get('cardamount', 1)))
        except (ValueError, TypeError):
            print("validate_image_urls: Warning: Invalid cardamount. Using 1.")
            cardamount = 1
        
        jpgs_field = config.get('jpgsurl', '')
        if not jpgs_field:
            jpgs_field = config.get('Jpgsurl', '')
        
        if not jpgs_field:
            error_msg = f"validate_image_urls: ERROR - 'jpgsurl' field is missing or empty in config for author '{author}'."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"validate_image_urls: Found jpgsurl field for author '{author}'")
        
        all_urls = parse_jpgs_url_field(jpgs_field)
        if not all_urls:
            error_msg = f"validate_image_urls: ERROR - No URLs found in 'jpgsurl' field for author '{author}'."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"validate_image_urls: Found {len(all_urls)} URLs/paths to validate for author '{author}'")
        
    except Exception as e:
        error_msg = f"validate_image_urls: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 4: VALIDATE EACH URL/PATH
    # ============================================================
    print(f"\n{'='*80}")
    print(f"VALIDATING {len(all_urls)} URLs/PATHS for author '{author}'")
    print(f"Required cardamount: {cardamount}")
    print(f"{'='*80}\n")
    
    valid_urls = []
    invalid_urls = []
    http_count = 0
    local_count = 0
    
    for i, url in enumerate(all_urls, 1):
        print(f"[{i}/{len(all_urls)}] Validating: {url[:100]}...")
        
        if is_http_url(url):
            http_count += 1
            print(f"  Type: HTTP URL")
            is_valid, info, error = validate_http_url(url)
        else:
            local_count += 1
            print(f"  Type: Local Path")
            is_valid, info, error = validate_local_file(url)
        
        if is_valid:
            valid_urls.append(url)
            print(f"  ✅ VALID - {info}")
        else:
            invalid_urls.append((url, error))
            print(f"  ❌ INVALID - {error}")
        
        print()
    
    # ============================================================
    # STEP 5: ALWAYS SAVE VALID URLs FIRST (even if not enough)
    # ============================================================
    print(f"\n{'='*80}")
    print(f"VALIDATION RESULTS")
    print(f"{'='*80}")
    print(f"Total URLs/paths checked: {len(all_urls)}")
    print(f"  • HTTP URLs checked:     {http_count}")
    print(f"  • Local paths checked:   {local_count}")
    print(f"Valid URLs:                {len(valid_urls)}")
    print(f"Invalid URLs removed:      {len(invalid_urls)}")
    print(f"Required cardamount:       {cardamount}")
    
    # ============================================================
    # STEP 6: UPDATE jpgsurl FIELD - ALWAYS REMOVE INVALID URLs
    # ============================================================
    print(f"\nUpdating jpgsurl field - keeping {len(valid_urls)} valid URLs, removing {len(invalid_urls)} invalid...")
    
    try:
        updated_jpgs_field = rebuild_jpgsurl_field(valid_urls, jpgs_field)
        
        if config_is_list:
            config_data[-1]['jpgsurl'] = updated_jpgs_field
        else:
            config_data['jpgsurl'] = updated_jpgs_field
        
        if save_json_file(AUTHOR_PATH, config_data):
            print(f"✅ jpgsurl field UPDATED - kept {len(valid_urls)} valid URLs, removed {len(invalid_urls)} invalid")
        else:
            error_msg = f"validate_image_urls: ERROR - Failed to save updated config to {AUTHOR_PATH}"
            print(f"❌ {error_msg}")
            update_author_status('aborted', error_msg)
            return
            
    except Exception as e:
        error_msg = f"validate_image_urls: ERROR - Failed to update jpgsurl field: {e}"
        print(f"❌ {error_msg}")
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 7: CHECK IF ENOUGH VALID URLs REMAIN (AFTER SAVING)
    # ============================================================
    if len(valid_urls) < cardamount:
        error_msg = f"validate_image_urls: ERROR - Only {len(valid_urls)} valid URLs remain after removing {len(invalid_urls)} invalid. Need {cardamount}. Not enough valid images!"
        print(f"\n❌ {error_msg}")
        
        if invalid_urls:
            print(f"\nRemoved invalid URLs (first 10):")
            for url, err in invalid_urls[:10]:
                filename = os.path.basename(url.split('?')[0]) if '/' in url or '\\' in url else url
                print(f"  • {filename}: {err}")
            if len(invalid_urls) > 10:
                print(f"  ... and {len(invalid_urls) - 10} more")
        
        print(f"\n⚠️ jpgsurl field was UPDATED (invalid URLs removed) but there aren't enough valid URLs.")
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 8: SUCCESS - UPDATE STATUS
    # ============================================================
    if invalid_urls:
        operation_msg = (
            f"validate_image_urls: Validated {len(all_urls)} URLs/paths for author '{author}'. "
            f"Removed {len(invalid_urls)} invalid URLs. "
            f"Kept {len(valid_urls)} valid URLs (need {cardamount}). "
            f"HTTP: {http_count}, Local: {local_count}. "
            f"SUCCESS: Enough valid URLs remaining."
        )
    else:
        operation_msg = (
            f"validate_image_urls: Validated {len(all_urls)} URLs/paths for author '{author}'. "
            f"All {len(valid_urls)} are valid! No URLs removed. "
            f"HTTP: {http_count}, Local: {local_count}."
        )
    
    update_author_status('pending', operation_msg)
    
    # ============================================================
    # STEP 9: FINAL SUMMARY
    # ============================================================
    print(f"\n{'='*80}")
    print(f"FINAL SUMMARY - Author: {author}")
    print(f"{'='*80}")
    print(f"HTTP URLs checked:    {http_count}")
    print(f"Local paths checked:  {local_count}")
    print(f"Valid URLs remaining: {len(valid_urls)}")
    print(f"Invalid URLs removed: {len(invalid_urls)}")
    print(f"Required cardamount:  {cardamount}")
    print(f"Status: {'pending ✅' if len(valid_urls) >= cardamount else 'aborted ❌'}")
    
    if invalid_urls:
        print(f"\n❌ Removed invalid URLs/paths (first 10):")
        for url, err in invalid_urls[:10]:
            filename = os.path.basename(url.split('?')[0]) if '/' in url or '\\' in url else url
            print(f"  • {filename}: {err}")
        if len(invalid_urls) > 10:
            print(f"  ... and {len(invalid_urls) - 10} more")
    
    print(f"\n✅ jpgsurl field updated in AUTHOR_PATH (invalid URLs removed)")
    print(f"{'='*80}\n")

def download_scheduled_images():
    """
    Downloads images based on the schedule time count.
    
    - Reads jpgsurl field from AUTHOR_PATH
    - Uses schedule_time_count to determine how many images to download
    - Checks downloaded_images_url to skip already downloaded images
    - Downloads images to {FILES_ROOT}/downloaded/{author}/
    - Records each downloaded URL immediately to AUTHOR_PATH under 'downloaded_images_url'
    - Retries failed downloads up to 3 times
    - Verifies each image after download (checks for corruption)
    - Updates operation_status and status in AUTHOR_PATH
    
    ONLY executes if status is 'pending'
    Sets status to 'aborted' only on fatal/critical errors
    """
    import os
    import json
    import requests
    import shutil
    import time
    from urllib.parse import urlparse
    from PIL import Image
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        return default if default is not None else {}
                    return json.loads(content)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"download_scheduled_images: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"download_scheduled_images: {operation_message}"
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = f"download_scheduled_images: {operation_message}"
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = f"download_scheduled_images: {operation_message}"
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def parse_jpgs_url_field(jpgs_field):
        """Parse the jpgsurl field which can be a dict or string. Returns list of URLs/paths."""
        if not jpgs_field:
            return []
        
        if isinstance(jpgs_field, dict):
            urls = []
            for key, value in jpgs_field.items():
                if isinstance(value, str):
                    items = [u.strip() for u in value.split(',') if u.strip()]
                    urls.extend(items)
                elif isinstance(value, list):
                    urls.extend([str(u).strip() for u in value if u])
            return urls
        
        if isinstance(jpgs_field, str):
            return [u.strip() for u in jpgs_field.split(',') if u.strip()]
        
        return []
    
    def is_http_url(url):
        """Check if the URL/path is an HTTP/HTTPS URL"""
        return url.lower().startswith(('http://', 'https://'))
    
    def download_and_verify_image(url, destination_path, timeout=30, max_retries=3):
        """
        Download a single image from URL to destination path with retry logic.
        Returns (success, message, file_size)
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"    Retry attempt {attempt + 1}/{max_retries}...")
                    time.sleep(2)
                
                response = requests.get(url, headers=headers, timeout=timeout, stream=True)
                
                if response.status_code != 200:
                    if attempt < max_retries - 1:
                        continue
                    return False, f"HTTP {response.status_code}", 0
                
                content_type = response.headers.get('Content-Type', '').lower()
                if content_type and not content_type.startswith('image/'):
                    if attempt < max_retries - 1:
                        continue
                    return False, f"Not an image: {content_type}", 0
                
                with open(destination_path, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                
                try:
                    with Image.open(destination_path) as img:
                        img.verify()
                    with Image.open(destination_path) as img:
                        img.load()
                        width, height = img.size
                        mode = img.mode
                except Exception as e:
                    if os.path.exists(destination_path):
                        os.remove(destination_path)
                    if attempt < max_retries - 1:
                        continue
                    return False, f"Corrupted image: {str(e)[:50]}", 0
                
                file_size = os.path.getsize(destination_path)
                return True, f"Downloaded: {width}x{height} {mode} ({file_size:,} bytes)", file_size
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    continue
                return False, f"Timeout after {timeout}s (attempt {attempt + 1})", 0
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    continue
                return False, f"Connection error (attempt {attempt + 1})", 0
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    continue
                return False, f"Request error: {str(e)[:50]}", 0
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                return False, f"Error: {str(e)[:50]}", 0
        
        return False, f"Failed after {max_retries} attempts", 0
    
    def copy_and_verify_local_file(source_path, destination_path, max_retries=3):
        """Copy a local file to destination with retry logic."""
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"    Retry attempt {attempt + 1}/{max_retries}...")
                    time.sleep(1)
                
                possible_paths = [
                    source_path,
                    os.path.join(FILES_ROOT, source_path),
                    os.path.join(FILES_ROOT, "jpgs", author, os.path.basename(source_path)),
                    os.path.join(FILES_ROOT, "jpgfolders", author, os.path.basename(source_path)),
                    os.path.join(FILES_ROOT, "uploaded jpgs", author, os.path.basename(source_path)),
                ]
                
                found_path = None
                for path in possible_paths:
                    if os.path.exists(path) and os.path.isfile(path):
                        found_path = path
                        break
                
                if not found_path:
                    if attempt < max_retries - 1:
                        continue
                    return False, f"File not found: {source_path}", 0
                
                try:
                    with Image.open(found_path) as img:
                        img.verify()
                    with Image.open(found_path) as img:
                        img.load()
                        width, height = img.size
                        mode = img.mode
                except Exception as e:
                    if attempt < max_retries - 1:
                        continue
                    return False, f"Corrupted image: {str(e)[:50]}", 0
                
                shutil.copy2(found_path, destination_path)
                file_size = os.path.getsize(destination_path)
                
                return True, f"Copied: {width}x{height} {mode} ({file_size:,} bytes)", file_size
                
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                return False, f"Copy error: {str(e)[:50]}", 0
        
        return False, f"Failed after {max_retries} attempts", 0

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "download_scheduled_images: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status == 'aborted':
            print(f"download_scheduled_images: SKIPPED - Status is 'aborted'. No action taken.")
            return
        
        if current_status != 'pending':
            print(f"download_scheduled_images: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"download_scheduled_images: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"download_scheduled_images: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "download_scheduled_images: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        schedule_time_count = config.get('schedule_time_count', 0)
        
        if isinstance(schedule_time_count, str):
            try:
                schedule_time_count = int(schedule_time_count)
            except ValueError:
                schedule_time_count = 0
        
        try:
            schedule_time_count = int(schedule_time_count)
        except (ValueError, TypeError):
            schedule_time_count = 0
        
        print(f"download_scheduled_images: Author: {author}")
        print(f"download_scheduled_images: Schedule time count: {schedule_time_count}")
        print(f"download_scheduled_images: 📥 Downloading {schedule_time_count} images needed for the operation")
        
        if schedule_time_count <= 0:
            print(f"download_scheduled_images: SKIPPED - schedule_time_count is {schedule_time_count}. No images to download.")
            return
        
        jpgs_field = config.get('jpgsurl', '')
        if not jpgs_field:
            jpgs_field = config.get('Jpgsurl', '')
        
        if not jpgs_field:
            error_msg = f"download_scheduled_images: ERROR - 'jpgsurl' field is missing or empty in config for author '{author}'."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"download_scheduled_images: Found jpgsurl field for author '{author}'")
        
        all_urls = parse_jpgs_url_field(jpgs_field)
        if not all_urls:
            error_msg = f"download_scheduled_images: ERROR - No URLs found in 'jpgsurl' field for author '{author}'."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"download_scheduled_images: Found {len(all_urls)} URLs/paths available")
        
    except Exception as e:
        error_msg = f"download_scheduled_images: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: CHECK WHAT'S ALREADY DOWNLOADED (CHECK DUPLICATES)
    # ============================================================
    downloaded_urls = config.get('downloaded_images_url', [])
    if not isinstance(downloaded_urls, list):
        downloaded_urls = []
    
    print(f"download_scheduled_images: Already downloaded {len(downloaded_urls)} images")
    
    # Filter out already downloaded URLs
    available_urls = [url for url in all_urls if url not in downloaded_urls]
    skipped_count = len(all_urls) - len(available_urls)
    
    if skipped_count > 0:
        print(f"download_scheduled_images: Skipping {skipped_count} already downloaded URLs")
    
    print(f"download_scheduled_images: {len(available_urls)} new URLs available")

    # ============================================================
    # STEP 4: CHECK IF ENOUGH NEW URLs AVAILABLE
    # ============================================================
    if len(available_urls) < schedule_time_count:
        print(f"download_scheduled_images: Only {len(available_urls)} new URLs available, need {schedule_time_count}")
        print(f"download_scheduled_images: Resetting downloaded tracking to allow reuse...")
        
        # Reset downloaded tracking
        if config_is_list:
            config_data[-1]['downloaded_images_url'] = []
        else:
            config_data['downloaded_images_url'] = []
        
        if save_json_file(AUTHOR_PATH, config_data):
            print(f"download_scheduled_images: Reset downloaded_images_url")
            available_urls = all_urls.copy()
        else:
            error_msg = "download_scheduled_images: ERROR - Failed to reset downloaded_images_url"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        if len(available_urls) < schedule_time_count:
            error_msg = f"download_scheduled_images: ERROR - Only {len(available_urls)} total URLs available, need {schedule_time_count}."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return

    # ============================================================
    # STEP 5: SETUP DOWNLOAD DIRECTORY
    # ============================================================
    download_dir = os.path.join(FILES_ROOT, "downloaded", author)
    
    try:
        os.makedirs(download_dir, exist_ok=True)
        print(f"download_scheduled_images: Download directory: {download_dir}")
    except Exception as e:
        error_msg = f"download_scheduled_images: ERROR - Failed to create download directory {download_dir}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 6: SELECT URLs TO DOWNLOAD (FIRST N)
    # ============================================================
    urls_to_download = available_urls[:schedule_time_count]
    print(f"download_scheduled_images: Selected {len(urls_to_download)} URLs to download")

    # ============================================================
    # STEP 7: DOWNLOAD EACH IMAGE (WITH RETRY AND DUPLICATE CHECK)
    # ============================================================
    print(f"\n{'='*80}")
    print(f"📥 DOWNLOADING {len(urls_to_download)} IMAGES for author '{author}'")
    print(f"   {len(urls_to_download)} of {schedule_time_count} images needed")
    print(f"{'='*80}\n")
    
    successful_downloads = []
    failed_downloads = []
    downloaded_count = 0
    total_files_size = 0
    
    for i, url in enumerate(urls_to_download, 1):
        print(f"[{i}/{len(urls_to_download)}] Processing: {url[:100]}...")
        
        # DOUBLE CHECK: Skip if already downloaded (safety check)
        current_config = load_json_file(AUTHOR_PATH, {})
        if isinstance(current_config, list) and len(current_config) > 0:
            current_downloaded = current_config[-1].get('downloaded_images_url', [])
        else:
            current_downloaded = current_config.get('downloaded_images_url', [])
        
        if not isinstance(current_downloaded, list):
            current_downloaded = []
        
        if url in current_downloaded:
            print(f"  ⏭️ SKIPPED - URL already downloaded")
            continue
        
        # Generate filename from URL
        parsed = urlparse(url)
        base_name = os.path.basename(parsed.path) if parsed.path else "image"
        
        if not base_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')):
            base_name += '.jpg'
        
        dest_path = os.path.join(download_dir, base_name)
        root, ext = os.path.splitext(base_name)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(download_dir, f"{root}_{counter}{ext}")
            counter += 1
        
        # Download or copy with retry
        if is_http_url(url):
            print(f"  Type: HTTP URL - Downloading...")
            success, message, file_size = download_and_verify_image(url, dest_path, max_retries=3)
        else:
            print(f"  Type: Local Path - Copying...")
            success, message, file_size = copy_and_verify_local_file(url, dest_path, max_retries=3)
        
        if success:
            successful_downloads.append({
                "url": url,
                "path": dest_path,
                "filename": os.path.basename(dest_path)
            })
            downloaded_count += 1
            total_files_size += file_size
            print(f"  ✅ SUCCESS - {message}")
            print(f"  Saved to: {dest_path}")
            
            # ============================================================
            # RECORD URL IMMEDIATELY AFTER SUCCESSFUL DOWNLOAD
            # ============================================================
            try:
                current_config = load_json_file(AUTHOR_PATH, {})
                
                if isinstance(current_config, list) and len(current_config) > 0:
                    current_downloaded = current_config[-1].get('downloaded_images_url', [])
                    if not isinstance(current_downloaded, list):
                        current_downloaded = []
                    if url not in current_downloaded:
                        current_downloaded.append(url)
                    current_config[-1]['downloaded_images_url'] = current_downloaded
                else:
                    current_downloaded = current_config.get('downloaded_images_url', [])
                    if not isinstance(current_downloaded, list):
                        current_downloaded = []
                    if url not in current_downloaded:
                        current_downloaded.append(url)
                    current_config['downloaded_images_url'] = current_downloaded
                
                if save_json_file(AUTHOR_PATH, current_config):
                    print(f"  📝 Recorded URL to downloaded_images_url (total: {len(current_downloaded)})")
                else:
                    print(f"  ⚠️ Failed to record URL to downloaded_images_url")
                    
            except Exception as e:
                print(f"  ⚠️ Error recording URL: {e}")
        else:
            failed_downloads.append({
                "url": url,
                "error": message
            })
            print(f"  ❌ FAILED after 3 attempts - {message}")
        
        print()
    
    # ============================================================
    # STEP 8: UPDATE CONFIG WITH FINAL DOWNLOADED URLS (if any were missed)
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            current_downloaded = config_data[-1].get('downloaded_images_url', [])
            if not isinstance(current_downloaded, list):
                current_downloaded = []
            
            for item in successful_downloads:
                if item["url"] not in current_downloaded:
                    current_downloaded.append(item["url"])
            
            config_data[-1]['downloaded_images_url'] = current_downloaded
        else:
            current_downloaded = config_data.get('downloaded_images_url', [])
            if not isinstance(current_downloaded, list):
                current_downloaded = []
            
            for item in successful_downloads:
                if item["url"] not in current_downloaded:
                    current_downloaded.append(item["url"])
            
            config_data['downloaded_images_url'] = current_downloaded
        
        if save_json_file(AUTHOR_PATH, config_data):
            print(f"✅ Final downloaded_images_url updated in AUTHOR_PATH")
            print(f"   Total downloaded: {len(current_downloaded)} images")
    except Exception as e:
        print(f"⚠️ Warning - Could not finalize downloaded_images_url: {e}")

    # ============================================================
    # STEP 9: CHECK RESULTS
    # ============================================================
    total_size_mb = total_files_size / (1024 * 1024) if total_files_size > 0 else 0
    
    print(f"\n{'='*80}")
    print(f"📥 DOWNLOAD SUMMARY - Author: {author}")
    print(f"{'='*80}")
    print(f"Images needed for operation:  {schedule_time_count}")
    print(f"URLs selected for download:   {len(urls_to_download)}")
    print(f"Successfully downloaded:      {len(successful_downloads)}")
    print(f"Failed downloads:             {len(failed_downloads)}")
    print(f"Skipped (already done):       {skipped_count if 'skipped_count' in locals() else 0}")
    print(f"Total download size:          {total_size_mb:.2f} MB")
    print(f"Download directory:           {download_dir}")
    
    # Progress percentage
    progress_percent = (len(successful_downloads) / schedule_time_count * 100) if schedule_time_count > 0 else 0
    print(f"Progress:                      {len(successful_downloads)}/{schedule_time_count} ({progress_percent:.1f}%)")
    
    if failed_downloads:
        print(f"\n❌ Failed downloads:")
        for item in failed_downloads[:5]:
            filename = os.path.basename(item['url'].split('?')[0]) if '/' in item['url'] else item['url']
            print(f"  • {filename[:50]}: {item['error']}")
        if len(failed_downloads) > 5:
            print(f"  ... and {len(failed_downloads) - 5} more")
    
    if successful_downloads:
        print(f"\n✅ Downloaded files:")
        for item in successful_downloads[:5]:
            print(f"  • {item['filename']}")
        if len(successful_downloads) > 5:
            print(f"  ... and {len(successful_downloads) - 5} more")
    
    # ============================================================
    # STEP 10: UPDATE STATUS
    # ============================================================
    if len(successful_downloads) == schedule_time_count:
        operation_msg = (
            f"Successfully downloaded {len(successful_downloads)}/{schedule_time_count} scheduled images for author '{author}'. "
            f"Total size: {total_size_mb:.2f} MB"
        )
        update_author_status('pending', operation_msg)
        print(f"\n✅ Status updated to 'pending' - All images downloaded successfully")
        
    elif len(successful_downloads) > 0:
        operation_msg = (
            f"Partially downloaded: {len(successful_downloads)}/{schedule_time_count} scheduled images for author '{author}'. "
            f"{len(failed_downloads)} failed. Continuing with {len(successful_downloads)} images."
        )
        update_author_status('pending', operation_msg)
        print(f"\n⚠️ Status updated to 'pending' - Partial download: {len(successful_downloads)}/{schedule_time_count}")
        
    else:
        error_msg = (
            f"ERROR - Failed to download any of the {schedule_time_count} scheduled images for author '{author}'. "
            f"All {len(failed_downloads)} downloads failed."
        )
        print(f"\n❌ {error_msg}")
        update_author_status('aborted', error_msg)
        return
    
    print(f"{'='*80}\n")
    
    return len(successful_downloads) == schedule_time_count
#====


           
#CSV ENGINE 
def generate_final_csv():
    """FINAL JARVEE-COMPATIBLE CSV – UNLIMITED POSTS WITH RANDOM CAPTION REUSE + 100 PER FILE SPLIT
    
    Reads captions, image URLs, and all config from AUTHOR_PATH.
    Only needs schedule from external JSON file.
    On success: 
    - Reads generated CSV files to CONFIRM used URLs
    - Removes confirmed URLs from jpgsurl field
    - Archives confirmed URLs to uploaded_jpgs_url field
    - Sets status to 'completed'
    - Opens the CSV folder in file manager
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' on any failure, 'completed' on success
    """
    
    import os
    import json
    import csv
    import random
    import string
    import subprocess
    import sys
    import platform
    from datetime import datetime
    import pytz

    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def open_folder_in_file_manager(folder_path):
        """Open a folder in the system's file manager"""
        try:
            if not os.path.exists(folder_path):
                print(f"⚠️ Folder does not exist: {folder_path}")
                return False
            
            system = platform.system()
            
            if system == 'Windows':
                # Windows: Use explorer
                subprocess.Popen(['explorer', folder_path])
                print(f"📂 Opened folder in Windows Explorer: {folder_path}")
                return True
                
            elif system == 'Darwin':
                # macOS: Use open
                subprocess.Popen(['open', folder_path])
                print(f"📂 Opened folder in Finder: {folder_path}")
                return True
                
            elif system == 'Linux':
                # Linux: Try different file managers
                file_managers = ['nautilus', 'dolphin', 'thunar', 'nemo', 'pcmanfm']
                for fm in file_managers:
                    try:
                        subprocess.Popen([fm, folder_path])
                        print(f"📂 Opened folder in {fm}: {folder_path}")
                        return True
                    except FileNotFoundError:
                        continue
                # Fallback: try xdg-open
                try:
                    subprocess.Popen(['xdg-open', folder_path])
                    print(f"📂 Opened folder using xdg-open: {folder_path}")
                    return True
                except:
                    print(f"⚠️ Could not open folder. Please navigate to: {folder_path}")
                    return False
            else:
                print(f"⚠️ Unsupported OS: {system}. Please navigate to: {folder_path}")
                return False
                
        except Exception as e:
            print(f"⚠️ Failed to open folder: {e}")
            print(f"📁 CSV folder location: {folder_path}")
            return False

    def get_uploaded_jpgs_url_from_config(config):
        """Extract uploaded_jpgs_url from config"""
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            return config['dynamic_values'].get('uploaded_jpgs_url', [])
        return config.get('uploaded_jpgs_url', [])

    def set_uploaded_jpgs_url_in_config(config, value):
        """Set uploaded_jpgs_url in config"""
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            config['dynamic_values']['uploaded_jpgs_url'] = value
        else:
            config['uploaded_jpgs_url'] = value
        return config

    def parse_jpgs_url_field(jpgs_field):
        """Parse jpgsurl field into list of URLs"""
        if not jpgs_field:
            return []
        if isinstance(jpgs_field, dict):
            urls = []
            for key, value in jpgs_field.items():
                if isinstance(value, str):
                    items = [u.strip() for u in value.split(',') if u.strip()]
                    urls.extend(items)
                elif isinstance(value, list):
                    urls.extend([str(u).strip() for u in value if u])
            return urls
        if isinstance(jpgs_field, str):
            return [u.strip() for u in jpgs_field.split(',') if u.strip()]
        return []

    def rebuild_jpgsurl_field(remaining_urls, original_field):
        """Rebuild jpgsurl field maintaining original format"""
        if not remaining_urls:
            if isinstance(original_field, dict):
                result = {}
                for key in original_field.keys():
                    result[key] = ""
                return result
            return ""
        
        if isinstance(original_field, dict):
            result = {}
            for key in original_field.keys():
                result[key] = ', '.join(remaining_urls)
            return result
        elif isinstance(original_field, str):
            return ', '.join(remaining_urls)
        return remaining_urls

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "generate_final_csv: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"generate_final_csv: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"generate_final_csv: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"generate_final_csv: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD ALL CONFIG FROM AUTHOR_PATH
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "generate_final_csv: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        time_order = config.get('time_order', '').strip()
        if not time_order:
            error_msg = "generate_final_csv: ERROR - 'time_order' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        try:
            cardamount = max(1, int(config.get('cardamount', 1)))
        except (ValueError, TypeError):
            error_msg = "generate_final_csv: ERROR - 'cardamount' is invalid in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        captions_state = config.get('captions_state', 'mixed').lower().strip()
        if captions_state not in ['fixed', 'mixed']:
            error_msg = f"generate_final_csv: ERROR - Invalid 'captions_state': {captions_state}. Must be 'fixed' or 'mixed'."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"generate_final_csv: Author: {author}")
        print(f"generate_final_csv: Time Order: {time_order}")
        print(f"generate_final_csv: Cardamount: {cardamount}")
        print(f"generate_final_csv: Captions State: {captions_state.upper()}")
        
    except Exception as e:
        error_msg = f"generate_final_csv: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: LOAD CAPTIONS FROM AUTHOR_PATH (author_caption field)
    # ============================================================
    author_caption = config.get('author_caption', [])
    
    if not author_caption or not isinstance(author_caption, list):
        error_msg = f"generate_final_csv: ERROR - 'author_caption' is missing, empty, or invalid in config for author '{author}'."
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    captions = []
    for item in author_caption:
        if isinstance(item, str):
            cleaned = item.strip()
            if cleaned:
                captions.append(cleaned)
        elif isinstance(item, dict):
            caption_text = item.get('description', '') or item.get('caption', '') or item.get('text', '')
            if not caption_text:
                for key, value in item.items():
                    if key.lower() not in ['key-name', 'id'] and isinstance(value, str) and value.strip():
                        caption_text = value
                        break
            
            if caption_text and isinstance(caption_text, str):
                cleaned = caption_text.strip()
                cleaned = cleaned.replace('\u201c', '"').replace('\u201d', '"')
                cleaned = cleaned.replace('\u2018', "'").replace('\u2019', "'")
                cleaned = cleaned.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
                cleaned = ' '.join(cleaned.split())
                cleaned = ''.join(ch for ch in cleaned if ord(ch) >= 32 or ch in '\t')
                if cleaned:
                    captions.append(cleaned)
    
    if not captions:
        error_msg = f"generate_final_csv: ERROR - No valid captions found in 'author_caption' for author '{author}'."
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    print(f"generate_final_csv: Loaded {len(captions)} captions from author_caption")

    # ============================================================
    # STEP 4: LOAD IMAGE URLs FROM AUTHOR_PATH (jpgsurl field)
    # ============================================================
    jpgs_field = config.get('jpgsurl', '')
    if not jpgs_field:
        jpgs_field = config.get('Jpgsurl', '')
    
    if not jpgs_field:
        error_msg = f"generate_final_csv: ERROR - 'jpgsurl' field is missing or empty in config for author '{author}'."
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # Parse all available URLs
    all_available_urls = parse_jpgs_url_field(jpgs_field)
    
    if not all_available_urls:
        error_msg = f"generate_final_csv: ERROR - No valid image URLs found in 'jpgsurl' for author '{author}'."
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # Take first N for CSV generation
    images = all_available_urls[:cardamount]
    print(f"generate_final_csv: Loaded {len(images)} image URLs from jpgsurl (total available: {len(all_available_urls)})")

    # ============================================================
    # STEP 5: FIXED MODE CHECK
    # ============================================================
    if captions_state == "fixed":
        print(f"\ngenerate_final_csv: FIXED CAPTIONS MODE - Checking caption count...")
        print(f"   Required: {cardamount} captions needed")
        print(f"   Available: {len(captions)} captions")
        
        if len(captions) < cardamount:
            error_msg = f"generate_final_csv: ERROR - Not enough captions for FIXED mode. Need {cardamount}, only have {len(captions)}. Captions cannot be reused in fixed mode."
            print(f"   ❌ {error_msg}")
            update_author_status('aborted', error_msg)
            return
        else:
            print(f"   ✅ Sufficient captions available")
    else:
        print(f"\ngenerate_final_csv: MIXED CAPTIONS MODE - Captions can be reused")

    # ============================================================
    # STEP 6: CHECK IMAGE COUNT
    # ============================================================
    if len(images) < cardamount:
        error_msg = f"generate_final_csv: ERROR - Not enough image URLs. Need {cardamount}, only have {len(images)}."
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 7: LOAD SCHEDULE FROM JSON FILE
    # ============================================================
    schedules_path = os.path.join(FILES_ROOT, "next jpg", author, "jsons", f"{time_order}_schedules.json")
    
    print(f"\ngenerate_final_csv: Looking for schedules at: {schedules_path}")
    
    if not os.path.exists(schedules_path):
        error_msg = f"generate_final_csv: ERROR - schedules.json not found: {schedules_path}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    try:
        with open(schedules_path, 'r', encoding='utf-8') as f:
            schedule_data = json.load(f)
        
        if 'next_schedule' not in schedule_data or not schedule_data['next_schedule']:
            error_msg = f"generate_final_csv: ERROR - No 'next_schedule' found in schedules for author '{author}'"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        next_schedule = schedule_data['next_schedule']
        if isinstance(next_schedule, dict):
            next_schedule = [next_schedule]
        
        schedule = next_schedule[:cardamount]
        
        if len(schedule) < cardamount:
            error_msg = f"generate_final_csv: ERROR - Not enough schedule slots. Need {cardamount}, only have {len(schedule)}."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"generate_final_csv: Loaded {len(schedule)} schedule slots")
        
    except Exception as e:
        error_msg = f"generate_final_csv: ERROR - Failed to read schedules: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 8: FINAL COUNT CHECK
    # ============================================================
    final_count = min(cardamount, len(images), len(schedule))
    if final_count == 0:
        error_msg = f"generate_final_csv: ERROR - Nothing to generate for author '{author}'"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    print(f"\ngenerate_final_csv: Building {final_count} JARVEE-READY posts...\n")

    # ============================================================
    # STEP 9: BUILD ALL ROWS
    # ============================================================
    rows = []
    expected_used_urls = []  # URLs we expect to see in the CSV
    random.seed()
    
    if captions_state == "fixed":
        captions_pool = captions.copy()
        random.shuffle(captions_pool)
        if len(captions_pool) < final_count:
            error_msg = f"generate_final_csv: ERROR - Not enough unique captions for FIXED mode. Need {final_count}, only have {len(captions_pool)}."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
    else:
        captions_pool = None

    for i in range(final_count):
        if captions_state == "fixed":
            caption = captions_pool[i % len(captions_pool)]
        else:
            caption = random.choice(captions)
        
        caption = caption.replace('\u201c', '"').replace('\u201d', '"')
        caption = caption.replace('\u2018', "'").replace('\u2019', "'")
        caption = caption.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
        caption = ' '.join(caption.split())
        caption = ''.join(ch for ch in caption if ord(ch) >= 32 or ch in '\t')
        
        img_url = images[i]
        expected_used_urls.append(img_url)  # Track expected URL
        slot = schedule[i]

        date_parts = slot['date'].split('/')
        yyyy_mm_dd = f"{date_parts[2]}-{date_parts[1].zfill(2)}-{date_parts[0].zfill(2)}"
        post_time = f"{yyyy_mm_dd} {slot['time_24hour']}"

        rows.append({
            "Text": caption,
            "Image URL": img_url,
            "Tags": "",
            "Posting Time": post_time
        })

        card = img_url.split('/')[-1].split('?')[0]
        print(f"  {i+1:3}. {post_time} → {card}")

    # ============================================================
    # STEP 10: SETUP CSV DIRECTORY
    # ============================================================
    csv_dir = os.path.join(FILES_ROOT, "csv", author)
    
    try:
        os.makedirs(csv_dir, exist_ok=True)
        print(f"\ngenerate_final_csv: CSV directory: {csv_dir}")
    except Exception as e:
        error_msg = f"generate_final_csv: ERROR - Failed to create CSV directory {csv_dir}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    base_csv_name = f"{author}_posts"

    # ============================================================
    # STEP 11: DELETE OLD CSVs + SPLIT & SAVE NEW ONES (100 per file)
    # ============================================================
    try:
        deleted_count = 0
        if os.path.exists(csv_dir):
            for file in os.listdir(csv_dir):
                if file.startswith(base_csv_name) and file.endswith('.csv'):
                    os.remove(os.path.join(csv_dir, file))
                    deleted_count += 1
        print(f"generate_final_csv: Deleted {deleted_count} old CSV file(s)")

        CHUNK_SIZE = 100
        total_files = (len(rows) + CHUNK_SIZE - 1) // CHUNK_SIZE
        saved_files = []

        for idx in range(total_files):
            chunk = rows[idx * CHUNK_SIZE : (idx + 1) * CHUNK_SIZE]
            
            if total_files == 1:
                csv_filename = f"{base_csv_name}.csv"
            else:
                suffix = '' if idx == 0 else '_' + string.ascii_lowercase[idx - 1]
                csv_filename = f"{base_csv_name}{suffix}.csv"
            
            csv_fullpath = os.path.join(csv_dir, csv_filename)

            with open(csv_fullpath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["Text", "Image URL", "Tags", "Posting Time"],
                    quoting=csv.QUOTE_ALL,
                    lineterminator='\n'
                )
                writer.writeheader()
                writer.writerows(chunk)

            saved_files.append(csv_fullpath)
            print(f"generate_final_csv: Saved: {csv_filename} ({len(chunk)} posts)")

    except Exception as e:
        error_msg = f"generate_final_csv: ERROR - Failed to save CSV files: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 12: CONFIRM URLs FROM GENERATED CSV FILES
    # ============================================================
    print(f"\ngenerate_final_csv: Confirming URLs from generated CSV files...")
    
    confirmed_urls = []
    confirmation_errors = []
    
    for csv_file_path in saved_files:
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get('Image URL', '').strip()
                    if url:
                        confirmed_urls.append(url)
            print(f"  ✅ Read {csv_file_path}")
        except Exception as e:
            error = f"Failed to read {csv_file_path}: {e}"
            confirmation_errors.append(error)
            print(f"  ❌ {error}")
    
    if confirmation_errors:
        error_msg = f"generate_final_csv: ERROR - Failed to confirm URLs from CSV files: {'; '.join(confirmation_errors[:3])}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # Deduplicate confirmed URLs
    confirmed_urls_unique = list(dict.fromkeys(confirmed_urls))
    
    print(f"\ngenerate_final_csv: URL Confirmation Results:")
    print(f"   Expected URLs:      {len(expected_used_urls)}")
    print(f"   Confirmed in CSV:   {len(confirmed_urls)}")
    print(f"   Unique confirmed:   {len(confirmed_urls_unique)}")
    
    # Verify expected URLs are in confirmed URLs
    missing_from_csv = [url for url in expected_used_urls if url not in confirmed_urls]
    extra_in_csv = [url for url in confirmed_urls_unique if url not in expected_used_urls]
    
    if missing_from_csv:
        print(f"   ⚠️ URLs expected but NOT found in CSV: {len(missing_from_csv)}")
        for url in missing_from_csv[:5]:
            print(f"      - {url[:80]}")
    
    if extra_in_csv:
        print(f"   ℹ️ Extra URLs found in CSV (not in expected): {len(extra_in_csv)}")
    
    # Use confirmed URLs as the source of truth
    final_used_urls = confirmed_urls_unique
    
    if not final_used_urls:
        error_msg = "generate_final_csv: ERROR - No URLs confirmed from CSV files."
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 13: REMOVE USED URLs FROM jpgsurl FIELD
    # ============================================================
    print(f"\ngenerate_final_csv: Removing {len(final_used_urls)} confirmed URLs from jpgsurl...")
    
    # Calculate remaining URLs
    remaining_urls = [url for url in all_available_urls if url not in final_used_urls]
    removed_count = len(all_available_urls) - len(remaining_urls)
    
    print(f"   Original URLs:     {len(all_available_urls)}")
    print(f"   URLs to remove:    {removed_count}")
    print(f"   URLs remaining:    {len(remaining_urls)}")
    
    # Update jpgsurl field
    try:
        updated_jpgs_field = rebuild_jpgsurl_field(remaining_urls, jpgs_field)
        
        if config_is_list:
            config_data[-1]['jpgsurl'] = updated_jpgs_field
        else:
            config_data['jpgsurl'] = updated_jpgs_field
        
        print(f"   ✅ jpgsurl field updated - {len(remaining_urls)} URLs remaining")
    except Exception as e:
        error_msg = f"generate_final_csv: ERROR - Failed to update jpgsurl field: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 14: ARCHIVE CONFIRMED URLs TO uploaded_jpgs_url FIELD
    # ============================================================
    print(f"\ngenerate_final_csv: Archiving {len(final_used_urls)} confirmed URLs to uploaded_jpgs_url...")
    
    try:
        # Get existing uploaded URLs
        existing_uploaded = get_uploaded_jpgs_url_from_config(config)
        
        # Extract existing URL strings (filter out metadata objects)
        if isinstance(existing_uploaded, list):
            existing_urls = [item for item in existing_uploaded if isinstance(item, str)]
        elif isinstance(existing_uploaded, str):
            try:
                existing_urls = json.loads(existing_uploaded)
                if isinstance(existing_urls, list):
                    existing_urls = [item for item in existing_urls if isinstance(item, str)]
                else:
                    existing_urls = []
            except:
                existing_urls = [u.strip() for u in existing_uploaded.split(',') if u.strip()]
        else:
            existing_urls = []
        
        # Combine and deduplicate
        all_uploaded = existing_urls + final_used_urls
        unique_uploaded = list(dict.fromkeys(all_uploaded))
        newly_added = len(unique_uploaded) - len(existing_urls)
        
        # Build the uploaded_jpgs_url array
        timestamp = datetime.now(pytz.timezone('Africa/Lagos')).isoformat()
        
        uploaded_jpgs_array = [{"folder": author}] + unique_uploaded
        uploaded_jpgs_array.append({
            "_timestamp": timestamp,
            "_total_urls": len(unique_uploaded),
            "_added_this_time": len(final_used_urls),
            "_new_unique": newly_added,
            "_csv_generated": True,
            "_csv_files": [os.path.basename(f) for f in saved_files],
            "_csv_location": csv_dir,
            "_confirmation": "URLs confirmed from generated CSV files"
        })
        
        # Update the config
        if config_is_list:
            config_data[-1] = set_uploaded_jpgs_url_in_config(config_data[-1], uploaded_jpgs_array)
        else:
            config_data = set_uploaded_jpgs_url_in_config(config_data, uploaded_jpgs_array)
        
        # Save ALL updates to AUTHOR_PATH
        if save_json_file(AUTHOR_PATH, config_data):
            print(f"generate_final_csv: ✅ Archived {len(final_used_urls)} confirmed URLs to uploaded_jpgs_url")
            print(f"   Existing: {len(existing_urls)}, New: {len(final_used_urls)}, Unique: {len(unique_uploaded)}")
            print(f"   jpgsurl: {len(remaining_urls)} URLs remaining (removed {removed_count})")
        else:
            error_msg = f"generate_final_csv: ERROR - Failed to save updates to {AUTHOR_PATH}"
            print(f"❌ {error_msg}")
            update_author_status('aborted', error_msg)
            return
            
    except Exception as e:
        error_msg = f"generate_final_csv: ERROR - Failed to archive URLs: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 15: SUCCESS - Update status to 'completed'
    # ============================================================
    print(f"\n{'='*80}")
    print(f"GENERATE FINAL CSV - COMPLETED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"Author:              {author}")
    print(f"Time Order:          {time_order}")
    print(f"Captions State:      {captions_state.upper()}")
    print(f"Total Posts:         {len(rows)}")
    print(f"Total Files:         {total_files}")
    print(f"Files:               {', '.join([os.path.basename(f) for f in saved_files])}")
    print(f"Captions Available:  {len(captions)}")
    print(f"Images Used:         {len(final_used_urls)}")
    print(f"Schedule Slots:      {len(schedule)}")
    print(f"CSV Location:        {csv_dir}")
    print(f"Old Files Deleted:   {deleted_count}")
    print(f"URLs Confirmed:      {len(final_used_urls)} from CSV files")
    print(f"URLs Removed:        {removed_count} from jpgsurl")
    print(f"URLs Archived:       {len(unique_uploaded)} total unique in uploaded_jpgs_url")
    print(f"URLs Remaining:      {len(remaining_urls)} in jpgsurl")
    print(f"Status:              completed ✅")
    print(f"{'='*80}\n")

    operation_parts = [
        f"generate_final_csv: CSV generation completed for author '{author}'",
        f"Time Order: {time_order}",
        f"Total posts: {len(rows)}",
        f"Files: {total_files} ({', '.join([os.path.basename(f) for f in saved_files])})",
        f"Captions: {len(captions)} available, mode: {captions_state.upper()}",
        f"URLs confirmed from CSV: {len(final_used_urls)}",
        f"URLs removed from jpgsurl: {removed_count}",
        f"URLs archived to uploaded_jpgs_url: {len(unique_uploaded)} total unique",
        f"URLs remaining in jpgsurl: {len(remaining_urls)}",
        f"Location: {csv_dir}",
        f"SUCCESS: CSV files generated, URLs confirmed from CSV, removed from jpgsurl, archived to uploaded_jpgs_url"
    ]
    operation_msg = '; '.join(operation_parts)
    
    # THIS IS THE ONLY FUNCTION THAT SETS STATUS TO 'completed'
    update_author_status('completed', operation_msg)
    print(f"✅ Status updated to 'completed'")
    
    # ============================================================
    # STEP 16: OPEN CSV FOLDER IN FILE MANAGER
    # ============================================================
    print(f"\n📂 Opening CSV folder in file manager...")
    open_folder_in_file_manager(csv_dir)
    
    return

def csv_engine():
    update_calendar()
    validate_image_urls()
    generate_final_csv()
#===============# 

   


#=====DRIVER AUTOMATION
# FORCE SSL BYPASS: This fixes "Could not reach host" in 90% of cases
os.environ['WDM_SSL_VERIFY'] = '0'
def initialize_driver(mode="headed"):
    """
    Full fix: Bypasses SSL issues, forces version matching, 
    and falls back to local cache if offline.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if driver initialization fails
    """
    import os
    import time
    import shutil
    import json
    import psutil
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from webdriver_manager.chrome import ChromeDriverManager
    
    global driver, wait

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    # Check current status
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
        elif isinstance(config_data, dict):
            config = config_data
        else:
            error_msg = "initialize_driver: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return None, None
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"initialize_driver: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return None, None
        
        print(f"initialize_driver: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"initialize_driver: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return None, None

    # ============================================================
    # STEP 2: INITIALIZE DRIVER
    # ============================================================
    print(f"initialize_driver: Starting driver initialization (mode: {mode})")
    
    try:
        # --- Process Cleanup ---
        print("Closing existing Chrome instances...")
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() in ['chrome.exe', 'chromedriver.exe']:
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(1)
        
        # --- Path Configuration ---
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        selenium_profile = os.path.expanduser(r"~\.chrome_selenium_profile")
        wdm_home = os.path.join(os.path.expanduser("~"), ".wdm")
        
        # --- Profile Setup ---
        if not os.path.exists(selenium_profile):
            real_user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
            source_profile = os.path.join(real_user_data, "Profile 1")
            if os.path.exists(source_profile):
                print("Copying Profile 1 to Selenium directory...")
                shutil.copytree(source_profile, selenium_profile, dirs_exist_ok=True)
        
        # --- Chrome Options ---
        chrome_options = Options()
        chrome_options.binary_location = chrome_path
        chrome_options.add_argument(f"--user-data-dir={selenium_profile}")
        chrome_options.add_argument("--profile-directory=Default")
        
        if mode == "headless":
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
        else:
            chrome_options.add_argument("--start-maximized")
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        # --- Driver Acquisition ---
        driver_path = None
        try:
            print("Attempting to download ChromeDriver v144...")
            driver_path = ChromeDriverManager().install()
            print(f"Driver downloaded successfully: {driver_path}")
            update_author_status('pending', f"initialize_driver: Driver v144 downloaded successfully")
        except Exception as e:
            error_msg = f"initialize_driver: Network download failed: {e}"
            print(error_msg)
            print("Searching local .wdm cache for the newest available driver...")
            update_author_status('pending', f"initialize_driver: Network failed, searching local cache")
            
            found_drivers = []
            for root, _, files in os.walk(wdm_home):
                for file in files:
                    if file.lower() == "chromedriver.exe":
                        found_drivers.append(os.path.join(root, file))
            
            if found_drivers:
                driver_path = max(found_drivers, key=os.path.getmtime)
                print(f"Using latest cached driver: {driver_path}")
                update_author_status('pending', f"initialize_driver: Using cached driver from {driver_path}")
            else:
                error_msg = "initialize_driver: ERROR - No driver found online or in cache. Please check your firewall/internet connection."
                print(error_msg)
                update_author_status('aborted', error_msg)
                return None, None
        
        # --- Start WebDriver ---
        try:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            wait = WebDriverWait(driver, 15)
            print("ChromeDriver initialized successfully.")
            
            # Update status on success
            success_msg = f"initialize_driver: ChromeDriver initialized successfully (mode: {mode})"
            update_author_status('pending', success_msg)
            
            return driver, wait
            
        except Exception as e:
            error_msg = f"initialize_driver: ERROR - Failed to start ChromeDriver: {e}"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return None, None
            
    except Exception as e:
        error_msg = f"initialize_driver: ERROR - Critical failure: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return None, None
    
def load_urls():
    """Load URLs from config based on author from AUTHOR_PATH.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if critical errors occur
    DOES NOT change status on success
    """
    import os
    import json
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "load_urls: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            raise Exception(error_msg)
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"load_urls: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return None
        
        print(f"load_urls: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"load_urls: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        raise Exception(error_msg)

    # ============================================================
    # STEP 2: GET AUTHOR AND ACCOUNT_URL FROM CONFIG
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "load_urls: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            raise Exception(error_msg)
        
        print(f"load_urls: Author found: {author}")
        
        # Get account_url from config
        account_url = config.get('account_url', {})
        if not account_url:
            error_msg = f"load_urls: ERROR - 'account_url' missing for author '{author}' in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            raise Exception(error_msg)
        
        # If account_url is a dict, get the value for this author
        if isinstance(account_url, dict):
            url = account_url.get(author, '')
            if not url:
                error_msg = f"load_urls: ERROR - No URL found for author '{author}' in account_url."
                print(error_msg)
                update_author_status('aborted', error_msg)
                raise Exception(error_msg)
        else:
            url = str(account_url)
        
        if not url:
            error_msg = f"load_urls: ERROR - Empty URL for author '{author}'."
            print(error_msg)
            update_author_status('aborted', error_msg)
            raise Exception(error_msg)
        
        # SUCCESS - DO NOT CHANGE STATUS
        print(f"load_urls: URL loaded successfully for author '{author}'")
        return url
        
    except Exception as e:
        error_msg = f"load_urls: Failed to load URL: {str(e)}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        raise

def launch_profile():
    """Navigate to the upload post URL, confirm it, and continuously recheck every 2 seconds.
    
    UPDATES operation_status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' ONLY if critical errors occur
    If schedule_end_date is older than schedule_date, just updates operation_status and returns
    DOES NOT change status on success or completion
    """
    global driver, wait
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "launch_profile: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"launch_profile: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"launch_profile: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"launch_profile: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD CONFIG DETAILS
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "launch_profile: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        schedule_date = config.get('schedule_date', '')
        schedule_end_date = config.get('schedule_end_date', '')
        
        print(f"launch_profile: Author: {author}")
        print(f"launch_profile: Schedule Date: {schedule_date}")
        print(f"launch_profile: Schedule End Date: {schedule_end_date}")
        
    except Exception as e:
        error_msg = f"launch_profile: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: CHECK SCHEDULE END DATE
    # If schedule_end_date is older than schedule_date -> operation is done
    # Just update operation_status and return - DO NOT CHANGE status
    # ============================================================
    if schedule_date and schedule_end_date:
        try:
            from datetime import datetime
            date_format = "%d/%m/%Y %H:%M"
            schedule_dt = datetime.strptime(schedule_date, date_format)
            schedule_end_dt = datetime.strptime(schedule_end_date, date_format)
            
            # If schedule_end_date is older than or equal to schedule_date -> operation is DONE
            if schedule_end_dt <= schedule_dt:
                msg = f"launch_profile: schedule end date ({schedule_end_date}) is older than schedule date ({schedule_date}), operation for the config is completed. closing operation."
                print(msg)
                # Update ONLY operation_status, status remains whatever it is
                update_author_status('pending', msg)
                return  # Exit the function, don't proceed with automation
            else:
                # schedule_end_date is newer than schedule_date -> operation is still ongoing
                print(f"launch_profile: schedule_end_date ({schedule_end_date}) is newer than schedule_date ({schedule_date}). Operation is ongoing - proceeding...")
                
        except ValueError as e:
            error_msg = f"launch_profile: ERROR - Invalid date format in schedule_date or schedule_end_date: {str(e)}"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        except Exception as e:
            error_msg = f"launch_profile: ERROR - Failed to parse dates: {str(e)}"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return

    # ============================================================
    # STEP 4: GET UPLOAD URL AND NAVIGATE
    # ============================================================
    try:
        # Get URL from config
        uploadpost_url = load_urls()
        if not uploadpost_url:
            error_msg = f"launch_profile: ERROR - Failed to get URL for author '{author}'"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"launch_profile: Upload URL: {uploadpost_url}")
        post_completed = False
        
        # Initial navigation attempt
        while True:
            current_url = driver.current_url
            if uploadpost_url == current_url or (uploadpost_url in current_url and len(uploadpost_url) > len(current_url) * 0.8):
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

        # ============================================================
        # STEP 5: CONTINUOUS RECHECKING LOOP
        # ============================================================
        last_url = driver.current_url
        
        while not post_completed:
            try:
                current_url = driver.current_url
                print("Checking if URL is correct...")

                if uploadpost_url in current_url:
                    if current_url != last_url:
                        print(f"URL changed: {last_url} → {current_url}. Resetting trackers.")
                        reset_trackers()
                        last_url = current_url

                    # Update progress JSON using FILES_ROOT
                    driver_progress_path = os.path.join(FILES_ROOT, "driverprogress.json")
                    progress_data = {"driver": "started", "scheduled": "waiting"}
                    try:
                        os.makedirs(os.path.dirname(driver_progress_path), exist_ok=True)
                        with open(driver_progress_path, 'w') as f:
                            json.dump(progress_data, f, indent=4)
                        print(f"Updated {driver_progress_path}")
                    except Exception as e:
                        print(f"Failed to write progress: {e}")

                    print(f"URL correct. Proceeding with post actions...")
                    sequence()
                    
                    # Check if post was successful
                    try:
                        success_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'post') or contains(text(), 'published')]")),
                            timeout=10
                        )
                        print("launch_profile: Post successful!")
                        post_completed = True
                        break
                    except:
                        print("Post may not be complete. Continuing to check...")
                    
                else:
                    print(f"URL MISMATCH: {current_url} ≠ {uploadpost_url}")
                    print("Forcing navigation to correct URL...")
                    reset_trackers()
                    last_url = current_url

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
                # Don't refresh if we're already on the correct URL
                if uploadpost_url not in driver.current_url:
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
                else:
                    print("On correct URL despite error. Continuing...")
                
                time.sleep(2)

    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            raise
        error_msg = f"launch_profile: Fatal error: {str(e)}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        raise
       
def reset_trackers():
    """Reset all function trackers to their initial state, excluding update_calendar.
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if critical errors occur
    Updates operation_status on success or failure
    """
    import os
    import json
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "reset_trackers: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            print(f"reset_trackers: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"reset_trackers: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"reset_trackers: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: RESET TRACKERS
    # ============================================================
    try:
        # ---- Caption writers ----
        writecaption_ocr.last_written_caption = None
        if hasattr(writecaption_element, 'last_written_caption'):
            writecaption_element.last_written_caption = None
        writecaption_element.has_written = False

        # ---- set_webschedule ----
        if hasattr(set_webschedule, 'has_set'):
            set_webschedule.has_set = False

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
        
        # SUCCESS - Update operation_status only, keep status as pending
        update_author_status('pending', "reset_trackers: All trackers reset successfully")
        return
        
    except Exception as e:
        error_msg = f"reset_trackers: ERROR - Failed to reset trackers: {str(e)}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
def copy_downloaded_to_nextjpg():
    """
    Copies images from 'downloaded' to 'next jpg' with cropping if needed.
    
    - Checks each image for borders and crops if detected
    - Copies (not moves) the processed image to next jpg
    - Creates filename.json with original filename before renaming
    - Renames to card_x.jpg after recording
    - Does NOT delete from source
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if critical errors occur
    """
    import os
    import json
    import re
    import shutil
    import numpy as np
    from PIL import Image
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, FILES_ROOT are already defined globally
    
    CROP_THRESHOLD = 40
    CROP_TOP = 10
    CROP_BOTTOM = 40
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        return default if default is not None else {}
                    return json.loads(content)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"copy_cropped_to_nextjpg: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"copy_cropped_to_nextjpg: {operation_message}"
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = f"copy_cropped_to_nextjpg: {operation_message}"
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = f"copy_cropped_to_nextjpg: {operation_message}"
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def process_image_with_crop(src_path, dst_path, threshold, crop_top, crop_bottom):
        """
        Process image: crop borders if detected, apply fixed crop, save to destination.
        Returns (success, action_type, filename)
        """
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
                img.save(dst_path, quality=95)
                print(f"[COPIED] As-is → {os.path.basename(dst_path)}")
                return True, "no_content", os.path.basename(src_path)

            y0, x0 = coords.min(axis=0)
            y1, x1 = coords.max(axis=0)

            # Case 2: Content fills entire image → no border
            if x0 == 0 and y0 == 0 and x1 == w - 1 and y1 == h - 1:
                print(f"[CHECK] No borders detected. Moving as-is.")
                img.save(dst_path, quality=95)
                print(f"[COPIED] As-is → {os.path.basename(dst_path)}")
                return True, "no_border", os.path.basename(src_path)

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
                print(f"[SAVED] Border-only → {os.path.basename(dst_path)}")
                return True, "border_only", os.path.basename(src_path)

            new_top = crop_top
            new_bottom = content_h - crop_bottom
            if new_bottom <= new_top:
                print(f"[WARN] Fixed crop would remove all. Saving border-cropped only.")
                cropped.save(dst_path, quality=95)
                print(f"[SAVED] Border-only → {os.path.basename(dst_path)}")
                return True, "border_only", os.path.basename(src_path)

            final_cropped = cropped.crop((0, new_top, content_w, new_bottom))
            final_h = new_bottom - new_top
            print(f"[FIXED] Cropped: {crop_top}px top, {crop_bottom}px bottom → {final_h}px tall")
            final_cropped.save(dst_path, quality=95)
            print(f"[SAVED] Fully cropped → {os.path.basename(dst_path)}")
            return True, "full_crop", os.path.basename(src_path)

        except Exception as e:
            print(f"[ERROR] Failed: {e}")
            return False, "error", None

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "copy_cropped_to_nextjpg: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status == 'aborted':
            print(f"copy_cropped_to_nextjpg: SKIPPED - Status is 'aborted'. No action taken.")
            return
        
        if current_status != 'pending':
            print(f"copy_cropped_to_nextjpg: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"copy_cropped_to_nextjpg: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"copy_cropped_to_nextjpg: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD AUTHOR FROM CONFIG
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "copy_cropped_to_nextjpg: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"copy_cropped_to_nextjpg: Author: {author}")
        
    except Exception as e:
        error_msg = f"copy_cropped_to_nextjpg: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 3: SETUP DIRECTORIES USING FILES_ROOT
    # ============================================================
    downloaded_dir = os.path.join(FILES_ROOT, "downloaded", author)
    next_jpg_dir = os.path.join(FILES_ROOT, "next jpg", author)
    
    print(f"copy_cropped_to_nextjpg: Downloaded directory: {downloaded_dir}")
    print(f"copy_cropped_to_nextjpg: Next JPG directory: {next_jpg_dir}")
    
    # Create directories if they don't exist
    try:
        os.makedirs(next_jpg_dir, exist_ok=True)
        print(f"copy_cropped_to_nextjpg: Created/verified next jpg directory")
    except Exception as e:
        error_msg = f"copy_cropped_to_nextjpg: ERROR - Failed to create next jpg directory {next_jpg_dir}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 4: CHECK DOWNLOADED DIRECTORY
    # ============================================================
    if not os.path.exists(downloaded_dir):
        warning_msg = f"Downloaded directory does not exist: {downloaded_dir}"
        print(warning_msg)
        update_author_status('pending', warning_msg)
        return
    
    # Supported image extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    
    # Get all image files from downloaded directory
    try:
        all_files = os.listdir(downloaded_dir)
        image_files = [f for f in all_files if f.lower().endswith(image_extensions)]
        image_files.sort()
    except Exception as e:
        error_msg = f"copy_cropped_to_nextjpg: ERROR - Failed to read downloaded directory {downloaded_dir}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    if not image_files:
        warning_msg = f"No image files found in downloaded directory: {downloaded_dir}"
        print(warning_msg)
        update_author_status('pending', warning_msg)
        return
    
    print(f"copy_cropped_to_nextjpg: Found {len(image_files)} image files in downloaded directory")
    
    # ============================================================
    # STEP 5: TAKE THE FIRST IMAGE AND PROCESS IT
    # ============================================================
    target_file = image_files[0]
    src_path = os.path.join(downloaded_dir, target_file)
    
    # Generate filename for destination
    base_name, ext = os.path.splitext(target_file)
    dest_filename = f"{base_name}.jpg"
    temp_dst_path = os.path.join(next_jpg_dir, dest_filename)
    
    # Ensure unique filename
    root, ext = os.path.splitext(dest_filename)
    counter = 1
    while os.path.exists(temp_dst_path):
        temp_dst_path = os.path.join(next_jpg_dir, f"{root}_{counter}{ext}")
        counter += 1
    
    print(f"\n{'='*60}")
    print(f"PROCESSING: {target_file}")
    print(f"{'='*60}")
    
    # ============================================================
    # STEP 6: PROCESS IMAGE (CROP IF NEEDED)
    # ============================================================
    success, action_type, original_filename = process_image_with_crop(
        src_path, temp_dst_path, CROP_THRESHOLD, CROP_TOP, CROP_BOTTOM
    )
    
    if not success:
        error_msg = f"Failed to process image: {target_file}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 7: CREATE filename.json BEFORE RENAMING
    # ============================================================
    filename_json_path = os.path.join(next_jpg_dir, "filename.json")
    
    try:
        # Load existing filename.json if it exists
        if os.path.exists(filename_json_path):
            with open(filename_json_path, 'r', encoding='utf-8') as f:
                filename_data = json.load(f)
        else:
            filename_data = {}
        
        # Store the original filename (before renaming to card_x.jpg)
        filename_data["original_filename"] = os.path.basename(temp_dst_path)
        filename_data["original_source"] = os.path.basename(src_path)
        filename_data["action"] = action_type
        filename_data["timestamp"] = __import__('time').strftime('%Y-%m-%d %H:%M:%S')
        filename_data["author"] = author
        
        with open(filename_json_path, 'w', encoding='utf-8') as f:
            json.dump(filename_data, f, indent=4)
        
        print(f"copy_cropped_to_nextjpg: Created filename.json with: {filename_data}")
        
    except Exception as e:
        error_msg = f"copy_cropped_to_nextjpg: ERROR - Failed to create filename.json: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 8: RENAME TO card_x.jpg
    # ============================================================
    dst_path = os.path.join(next_jpg_dir, "card_x.jpg")
    
    try:
        # Remove existing card_x.jpg if it exists
        if os.path.exists(dst_path):
            os.remove(dst_path)
            print(f"copy_cropped_to_nextjpg: Removed existing card_x.jpg")
        
        # Rename the processed file to card_x.jpg
        os.rename(temp_dst_path, dst_path)
        print(f"copy_cropped_to_nextjpg: RENAMED → card_x.jpg (from {os.path.basename(temp_dst_path)})")
        
    except Exception as e:
        error_msg = f"copy_cropped_to_nextjpg: ERROR - Failed to rename to card_x.jpg: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 9: UPDATE STATUS AND RETURN
    # ============================================================
    print(f"\ncopy_cropped_to_nextjpg: COMPLETED SUCCESSFULLY")
    print(f"  • Source: {src_path}")
    print(f"  • Destination: {dst_path}")
    print(f"  • Action: {action_type}")
    print(f"  • Original filename recorded in filename.json")
    print(f"  • Source file KEPT in downloaded directory")
    
    success_msg = f"Successfully processed '{target_file}' ({action_type}) and copied to card_x.jpg for author '{author}'"
    update_author_status('pending', success_msg)
    print(f"copy_cropped_to_nextjpg: {success_msg}")

def randomize_group_types():
    """
    Check AUTHOR_PATH for group_types field and manage randomization of group types.
    
    This function:
    1. ONLY executes if status is 'pending'
    2. Prioritizes group_types over groups/group
    3. Supports both list format ["group1","group2"] and string format "group1, group2"
    4. Processes ONLY ONE group at a time
    5. If group_types has 2+ groups, reset tracker with all groups
    6. If tracker is empty and group_types has 1 group, use it
    7. If group_types is empty, check for 'groups' or 'group' fields
    8. When all groups used, restart the revolution
    9. group_types is NEVER empty
    10. Sets status to 'aborted' ONLY on critical errors
    11. Updates operation_status with success/error messages
    
    Returns:
        bool: True if successful, False if error
    """
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH - PRESERVES ALL DATA AND FORMAT"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = operation_message
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = operation_message
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = operation_message
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = operation_message
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def extract_groups_from_field(value):
        """
        Extract groups from a field value that can be either:
        - String: "group1, group2, group3"
        - List: ["group1", "group2", "group3"]
        
        Returns:
            list: Extracted groups, or empty list if none found
        """
        if not value:
            return []
        
        if isinstance(value, list):
            # It's already a list
            return [str(item).strip() for item in value if str(item).strip()]
        elif isinstance(value, str):
            # It's a string - split by comma
            return [g.strip() for g in value.split(',') if g.strip()]
        else:
            return []
    
    def get_groups_from_config(config):
        """
        Get groups from config with priority:
        1. group_types (highest priority)
        2. groups
        3. group (lowest priority)
        
        Returns:
            tuple: (source_field_name, groups_list)
        """
        # Priority 1: group_types
        if 'group_types' in config:
            group_types_value = config.get('group_types')
            groups = extract_groups_from_field(group_types_value)
            if groups:
                return ('group_types', groups)
        
        # Priority 2: groups
        if 'groups' in config:
            groups_value = config.get('groups')
            groups = extract_groups_from_field(groups_value)
            if groups:
                return ('groups', groups)
        
        # Priority 3: group
        if 'group' in config:
            group_value = config.get('group')
            groups = extract_groups_from_field(group_value)
            if groups:
                return ('group', groups)
        
        # No groups found
        return (None, [])
    
    # ============================================================
    # STEP 1: LOAD AND CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        author_data = load_json_file(AUTHOR_PATH, {})
        
        # Handle both list and dict formats
        if isinstance(author_data, list) and len(author_data) > 0:
            config = author_data[-1]
            is_list_format = True
        elif isinstance(author_data, dict):
            config = author_data
            is_list_format = False
        else:
            error_msg = "randomize_group_types: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return False
        
        # Check status - only proceed if 'pending'
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status != 'pending':
            return False
        
        print(f"randomize_group_types: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"randomize_group_types: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return False
    
    # ============================================================
    # STEP 2: GET GROUPS FROM CONFIG WITH PRIORITY
    # ============================================================
    try:
        # Get groups with priority (group_types > groups > group)
        source_field, current_groups = get_groups_from_config(config)
        
        if not current_groups:
            # No groups found in any field
            msg = "randomize_group_types: No groups found in group_types, groups, or group fields."
            print(msg)
            update_author_status('pending', msg)
            return False
        
        print(f"randomize_group_types: Using '{source_field}' as source: {current_groups}")
        
        # Get tracker
        tracker = config.get('randomizing_group_tracker', {})
        
        # ============================================================
        # STEP 3: HANDLE EMPTY OR INVALID GROUPS
        # ============================================================
        if not current_groups:
            # Clear tracker if no groups
            print("randomize_group_types: No valid groups found. Clearing tracker...")
            config['group_types'] = ''  # Clear main field
            config['randomizing_group_tracker'] = {}
            
            if is_list_format:
                author_data[-1] = config
            else:
                author_data = config
            
            if save_json_file(AUTHOR_PATH, author_data):
                msg = "randomize_group_types: No valid groups found. Tracker cleared."
                print(msg)
                update_author_status('pending', msg)
                return False
            else:
                error_msg = "randomize_group_types: ERROR - Failed to save config after clearing tracker."
                print(error_msg)
                update_author_status('aborted', error_msg)
                return False
        
        print(f"randomize_group_types: Current groups: {current_groups}")
        
        # ============================================================
        # STEP 4: DECIDE SOURCE OF TRUTH
        # ============================================================
        tracker_groups = tracker.get('original_groups', [])
        should_reset = False
        
        # Condition 1: If group_types has 2+ groups, reset tracker
        if len(current_groups) >= 2:
            should_reset = True
            print(f"randomize_group_types: Source has {len(current_groups)} groups. Resetting tracker...")
            groups_to_process = current_groups
            
            # Create new tracker with all groups
            tracker = {
                'original_groups': groups_to_process.copy(),
                'remaining_groups': groups_to_process[1:].copy(),  # All except first
                'used_groups': [groups_to_process[0]],  # First group is used
                'current_group': groups_to_process[0],
                'total_groups': len(groups_to_process),
                'used_count': 1,
                'is_complete': False,
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
                'source_field': source_field  # Track which field we're using
            }
            
            # Update the source field with first group (ONLY ONE group)
            config[source_field] = groups_to_process[0]
            # Also update group_types for backward compatibility
            config['group_types'] = groups_to_process[0]
            
            msg = f"randomize_group_types: Tracker reset with {len(groups_to_process)} groups from '{source_field}'. Using first group: {groups_to_process[0]}. Remaining: {len(tracker['remaining_groups'])}"
            print(msg)
            update_author_status('pending', msg)
            
        # Condition 2: Tracker is empty but source has 1 group
        elif not tracker_groups and len(current_groups) == 1:
            print("randomize_group_types: Tracker empty, source has 1 group. Initializing tracker...")
            groups_to_process = current_groups
            
            # Create tracker with this single group
            tracker = {
                'original_groups': groups_to_process.copy(),
                'remaining_groups': [],
                'used_groups': [groups_to_process[0]],
                'current_group': groups_to_process[0],
                'total_groups': 1,
                'used_count': 1,
                'is_complete': True,  # Only group is already used
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
                'source_field': source_field
            }
            
            # Keep source field as is (single group)
            config[source_field] = groups_to_process[0]
            config['group_types'] = groups_to_process[0]
            
            msg = f"randomize_group_types: Tracker initialized with single group: {groups_to_process[0]} from '{source_field}'"
            print(msg)
            update_author_status('pending', msg)
            
        # Condition 3: Use existing tracker
        elif tracker_groups:
            print(f"randomize_group_types: Using existing tracker as source of truth (originally from '{tracker.get('source_field', 'unknown')}')...")
            groups_to_process = tracker_groups
            
            # Check if all groups have been used (revolution complete)
            if tracker.get('is_complete', False) or len(tracker.get('used_groups', [])) >= len(groups_to_process):
                print("randomize_group_types: All groups used. Restarting revolution...")
                
                # Reset the revolution - move all used groups to remaining
                tracker['remaining_groups'] = groups_to_process.copy()
                tracker['used_groups'] = []
                tracker['used_count'] = 0
                tracker['is_complete'] = False
                tracker['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
                
                # Pick first group as current
                next_group = groups_to_process[0]
                tracker['current_group'] = next_group
                tracker['remaining_groups'] = groups_to_process[1:].copy()
                tracker['used_groups'] = [next_group]
                tracker['used_count'] = 1
                
                # Update source field with first group
                source_field_to_use = tracker.get('source_field', 'group_types')
                config[source_field_to_use] = next_group
                config['group_types'] = next_group
                
                msg = f"randomize_group_types: Revolution restarted! Using first group: {next_group}. Remaining: {len(tracker['remaining_groups'])}"
                print(msg)
                update_author_status('pending', msg)
            else:
                # Normal flow - get next unused group
                remaining = tracker.get('remaining_groups', [])
                
                if remaining:
                    # Get next group
                    next_group = remaining[0]
                    tracker['current_group'] = next_group
                    tracker['used_groups'].append(next_group)
                    tracker['remaining_groups'] = remaining[1:] if len(remaining) > 1 else []
                    tracker['used_count'] = len(tracker['used_groups'])
                    tracker['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Check if this was the last group
                    if not tracker['remaining_groups']:
                        tracker['is_complete'] = True
                        msg = f"randomize_group_types: Last group used: {next_group}. Revolution complete!"
                        print(msg)
                    else:
                        msg = f"randomize_group_types: Using next group: {next_group}. Used: {tracker['used_count']}/{tracker['total_groups']}. Remaining: {len(tracker['remaining_groups'])}"
                        print(msg)
                    
                    # Update source field with next group (ONLY ONE group)
                    source_field_to_use = tracker.get('source_field', 'group_types')
                    config[source_field_to_use] = next_group
                    config['group_types'] = next_group
                    update_author_status('pending', msg)
                    
                else:
                    # No remaining groups but not marked complete - this shouldn't happen
                    # Force restart
                    print("randomize_group_types: No remaining groups but not complete. Forcing restart...")
                    tracker['is_complete'] = True
                    source_field_to_use = tracker.get('source_field', 'group_types')
                    config[source_field_to_use] = tracker.get('current_group', groups_to_process[0])
                    config['group_types'] = tracker.get('current_group', groups_to_process[0])
                    msg = "randomize_group_types: No remaining groups. Marking as complete."
                    update_author_status('pending', msg)
        
        # ============================================================
        # STEP 5: SAVE UPDATED CONFIG
        # ============================================================
        # Save the updated tracker back to config
        config['randomizing_group_tracker'] = tracker
        
        # Update the author data structure
        if is_list_format:
            author_data[-1] = config
        else:
            author_data = config
        
        if save_json_file(AUTHOR_PATH, author_data):
            final_msg = f"randomize_group_types: SUCCESS - '{source_field if source_field else 'group_types'}' set to '{config['group_types']}'. Tracker: {tracker['used_count']}/{tracker['total_groups']} groups used. Remaining: {len(tracker.get('remaining_groups', []))}"
            print(final_msg)
            update_author_status('pending', final_msg)
            return True
        else:
            error_msg = "randomize_group_types: ERROR - Failed to save updated config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return False
            
    except Exception as e:
        error_msg = f"randomize_group_types: ERROR - Failed to process: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return False
                
def selectgroups():
    """Locate and click the dropdown element associated with 'Post to' text, check pageandgroupauthors.json for page, group, and post_filter fields, select or unselect page profile under 'Post to Facebook and Instagram' based on page field, and based on group and post_filter fields: if group is 'include', select the groups listed in post_filter array (case-insensitive, ignoring spaces and special characters). If group is 'none', unselect all groups. Verify selections, save to AUTHOR_PATH, and click Save.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Sets status to 'aborted' if groups cannot be selected
    Stores group selections in 'groups_selected' field in AUTHOR_PATH
    """
    global driver, wait
    
    import os
    import json
    import re
    import time
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
    
    # ===== USE CENTRALIZED CONFIGURATION =====
    # AUTHOR_PATH is already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"selectgroups: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"selectgroups: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False
    
    def save_groups_selection_to_author_path(groups_list, status_message):
        """Save group selections directly to AUTHOR_PATH in the 'groups_selected' field"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            
            # Handle both list and dict formats
            if isinstance(author_data, list) and len(author_data) > 0:
                config = author_data[-1]
                is_list_format = True
            elif isinstance(author_data, dict):
                config = author_data
                is_list_format = False
            else:
                print("selectgroups: ERROR - Invalid config format in AUTHOR_PATH")
                return False
            
            # Create groups_selected structure
            if not groups_list:
                groups_selected = {
                    "1st": "",
                    "2nd": "",
                    "3rd": ""
                }
            else:
                groups_selected = {
                    "1st": groups_list[0] if len(groups_list) > 0 else "",
                    "2nd": groups_list[1] if len(groups_list) > 1 else "",
                    "3rd": groups_list[2] if len(groups_list) > 2 else ""
                }
            
            # Save to config
            config['groups_selected'] = {
                "current_selected": groups_selected,
                "status": status_message,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Update the author data structure
            if is_list_format:
                author_data[-1] = config
            else:
                author_data = config
            
            if save_json_file(AUTHOR_PATH, author_data):
                print(f"selectgroups: Saved groups_selected to AUTHOR_PATH: {groups_selected}")
                return True
            else:
                print("selectgroups: ERROR - Failed to save groups_selected to AUTHOR_PATH")
                return False
                
        except Exception as e:
            print(f"selectgroups: ERROR - Failed to save groups_selection: {e}")
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"selectgroups: SKIPPED - Status is 'aborted'. No action taken.")
        return False

    print(f"selectgroups: Starting group selection process")
    update_author_status('pending', f"Starting group selection process")
    
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

    # Check if function should retry or skip
    if selectgroups.is_dropdown_opened or selectgroups.is_see_more_clicked or selectgroups.groups_selected:
        selectgroups.failed_attempts += 1
        if selectgroups.failed_attempts >= 3:
            print("selectgroups has failed too many times (3 attempts). Skipping to prevent blocking other functions.")
            update_author_status('aborted', f"Failed after 3 attempts - group selection could not be completed")
            return False
        print(f"Retry attempt {selectgroups.failed_attempts} due to prior state (is_dropdown_opened={selectgroups.is_dropdown_opened}, is_see_more_clicked={selectgroups.is_see_more_clicked}, groups_selected={selectgroups.groups_selected})")

    # ===== READ CONFIG FROM AUTHOR_PATH =====
    page_config = 'none'
    group_config = 'none'
    target_group_list = []
    
    try:
        with open(AUTHOR_PATH, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            
            # Handle both list and dict formats
            if isinstance(config_data, list) and len(config_data) > 0:
                config = config_data[-1]
            elif isinstance(config_data, dict):
                config = config_data
            else:
                print(f"selectgroups: ERROR - Invalid config format in AUTHOR_PATH")
                update_author_status('aborted', f"Invalid config format in AUTHOR_PATH")
                return False
            
            page_config = config.get('page', 'none')
            group_config = config.get('group', 'none')
            
            # ===== GET GROUPS WITH PRIORITY (group_types > groups > group) =====
            raw_group_types = config.get('group_types', '')
            raw_groups = config.get('groups', '')
            raw_group = config.get('group', '')
            
            # Priority 1: group_types
            if raw_group_types:
                if isinstance(raw_group_types, list):
                    target_group_list = [str(g).strip() for g in raw_group_types if str(g).strip()]
                elif isinstance(raw_group_types, str):
                    if ',' in raw_group_types:
                        target_group_list = [g.strip() for g in raw_group_types.split(',') if g.strip()]
                    else:
                        target_group_list = [raw_group_types.strip()] if raw_group_types.strip() else []
                print(f"Using group_types as source: {target_group_list}")
            
            # Priority 2: groups (if group_types empty or invalid)
            elif raw_groups and not target_group_list:
                if isinstance(raw_groups, list):
                    target_group_list = [str(g).strip() for g in raw_groups if str(g).strip()]
                elif isinstance(raw_groups, str):
                    if ',' in raw_groups:
                        target_group_list = [g.strip() for g in raw_groups.split(',') if g.strip()]
                    else:
                        target_group_list = [raw_groups.strip()] if raw_groups.strip() else []
                print(f"Using groups as source: {target_group_list}")
            
            # Priority 3: group (if both group_types and groups empty/invalid)
            elif raw_group and not target_group_list:
                if isinstance(raw_group, list):
                    target_group_list = [str(g).strip() for g in raw_group if str(g).strip()]
                elif isinstance(raw_group, str):
                    if ',' in raw_group:
                        target_group_list = [g.strip() for g in raw_group.split(',') if g.strip()]
                    else:
                        target_group_list = [raw_group.strip()] if raw_group.strip() else []
                print(f"Using group as source: {target_group_list}")
            
            print(f"Read config from {AUTHOR_PATH}: page={page_config}, group={group_config}, target_groups={target_group_list}")
            
            # Validate target_group_list
            if not target_group_list and group_config == 'include':
                print("Warning: group is 'include' but no groups found in group_types, groups, or group fields!")
                
    except Exception as e:
        print(f"Error reading JSON file {AUTHOR_PATH}: {str(e)}")
        page_config = 'none'
        group_config = 'none'
        target_group_list = []

    # Function to normalize group names for comparison
    def normalize_group_name(name):
        """Remove spaces, special characters, and convert to lowercase for comparison"""
        if not name:
            return ""
        # Convert to lowercase
        normalized = name.lower()
        # Remove special characters (keep alphanumeric)
        normalized = re.sub(r'[^a-z0-9]', '', normalized)
        return normalized

    # Pre-normalize target group list
    normalized_targets = {}
    for target in target_group_list:
        norm = normalize_group_name(target)
        normalized_targets[norm] = target
        print(f"Target group: '{target}' normalized to: '{norm}'")

    # ==================== SUB-FUNCTIONS ====================   
    def toggle_dropdown():
        """Open the dropdown associated with 'Post to' text"""
        if selectgroups.is_dropdown_opened:
            print("Dropdown already opened. Skipping dropdown click operation.")
            return True
        
        try:
            print("Looking for 'Post to' section and dropdown...")
            
            # First, find the visible 'Post to' text element
            post_to_label = None
            try:
                # Find visible element containing 'Post to' (not script)
                elements = driver.find_elements(By.XPATH, 
                    "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'post to') and not(self::script) and not(self::style)]")
                
                for elem in elements:
                    if elem.is_displayed():
                        post_to_label = elem
                        print(f"✓ Found visible 'Post to' label: <{post_to_label.tag_name}>")
                        break
            except Exception as e:
                print(f"Error finding label: {e}")
            
            if not post_to_label:
                print("✗ Could not find 'Post to' label")
                return False
            
            # NEW APPROACH: Look for the dropdown by its actual characteristics
            dropdown = None
            
            # Method 1: Look for the div that shows the current selection (e.g., "Jena26" or "Public")
            # This is usually the clickable element that opens the dropdown
            print("Method 1: Looking for clickable element with text (current selection)...")
            try:
                # Find all clickable divs with non-empty text in the same general area
                potential_dropdowns = driver.find_elements(By.XPATH, 
                    "//div[@role='button' and string-length(normalize-space(text())) > 0] | "
                    "//div[@role='combobox' and string-length(normalize-space(text())) > 0] | "
                    "//div[contains(@class, 'x1i10hfl') and string-length(normalize-space(text())) > 0]")
                
                for elem in potential_dropdowns:
                    if elem.is_displayed() and elem.is_enabled():
                        # Check if it's near the 'Post to' label (within reasonable distance)
                        try:
                            label_y = post_to_label.location['y']
                            elem_y = elem.location['y']
                            # Dropdown should be within 100 pixels vertically from the label
                            if abs(elem_y - label_y) < 100:
                                dropdown = elem
                                print(f"✓ Found dropdown with text: '{elem.text[:50]}' (y={elem_y}, label y={label_y})")
                                break
                        except:
                            pass
            except Exception as e:
                print(f"  Method 1 failed: {e}")
            
            # Method 2: Find the parent container that holds both label and dropdown by going up more levels
            if not dropdown:
                print("Method 2: Searching parent containers at multiple levels...")
                try:
                    # Try different parent levels (1-5)
                    for level in range(1, 6):
                        try:
                            parent = post_to_label.find_element(By.XPATH, f"./ancestor::div[{level}]")
                            # Look for any clickable element within this parent
                            clickable = parent.find_elements(By.XPATH, 
                                ".//div[@role='button'] | .//div[@role='combobox'] | .//div[contains(@class, 'x1i10hfl')]")
                            
                            for elem in clickable:
                                if elem.is_displayed() and elem.is_enabled() and elem != post_to_label:
                                    # Check if it has text or is likely the dropdown
                                    if elem.text.strip() or 'combobox' in elem.get_attribute('role'):
                                        dropdown = elem
                                        print(f"✓ Found dropdown in parent level {level}: text='{elem.text[:30]}'")
                                        break
                            if dropdown:
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"  Method 2 failed: {e}")
            
            # Method 3: Look for the element immediately after 'Post to' in the DOM
            if not dropdown:
                print("Method 3: Looking for adjacent element after 'Post to'...")
                try:
                    # Find the next sibling or following div
                    next_element = post_to_label.find_element(By.XPATH, 
                        "./following-sibling::div[1] | ./following::div[contains(@class, 'x1i10hfl')][1]")
                    if next_element and next_element.is_displayed():
                        dropdown = next_element
                        print(f"✓ Found adjacent dropdown: <{next_element.tag_name}> text='{next_element.text[:30]}'")
                except:
                    pass
            
            # Method 4: Direct search for Facebook's audience selector
            if not dropdown:
                print("Method 4: Looking for Facebook's audience selector directly...")
                try:
                    # Facebook often has aria-label for audience selector
                    dropdown = driver.find_element(By.XPATH, 
                        "//div[@aria-label='Post to' and @role='combobox'] | "
                        "//div[@aria-label='Audience' and @role='combobox'] | "
                        "//div[contains(@aria-label, 'audience') and @role='combobox']")
                    if dropdown and dropdown.is_displayed():
                        print("✓ Found dropdown via aria-label")
                except:
                    pass
            
            # Method 5: Look for any combobox on the page and check if it's relevant
            if not dropdown:
                print("Method 5: Checking all comboboxes on page...")
                try:
                    comboboxes = driver.find_elements(By.XPATH, "//div[@role='combobox']")
                    for cb in comboboxes:
                        if cb.is_displayed() and cb.is_enabled():
                            # Check if it's in the top half of the page (where Post to usually is)
                            if cb.location['y'] < 400:
                                dropdown = cb
                                print(f"✓ Found combobox at y={cb.location['y']}, text='{cb.text[:30]}'")
                                break
                except:
                    pass
            
            # Method 6: Last resort - look for any div with specific Facebook class patterns
            if not dropdown:
                print("Method 6: Looking for Facebook dropdown by class patterns...")
                try:
                    # Facebook's dropdown trigger has specific classes
                    dropdowns = driver.find_elements(By.XPATH, 
                        "//div[contains(@class, 'x1i10hfl') and contains(@class, 'x1qjc9v5') and contains(@class, 'x1ypdohk')]")
                    for dd in dropdowns:
                        if dd.is_displayed() and dd.is_enabled():
                            dropdown = dd
                            print(f"✓ Found dropdown by Facebook classes")
                            break
                except:
                    pass
            
            if not dropdown:
                print("✗ Could not find dropdown using any method")
                
                # Final debug: Print all clickable elements on the page
                print("\n=== DEBUG: All clickable elements on page (first 10) ===")
                all_clickable = driver.find_elements(By.XPATH, 
                    "//div[@role='button'] | //div[@role='combobox'] | //button")
                for idx, elem in enumerate(all_clickable[:10]):
                    try:
                        print(f"{idx+1}. <{elem.tag_name}> role='{elem.get_attribute('role')}' text='{elem.text[:30]}' y={elem.location['y']}")
                    except:
                        print(f"{idx+1}. [Unable to read]")
                return False
            
            # Print element details before clicking
            print("\n" + "="*60)
            print("ELEMENT TO BE CLICKED:")
            print("="*60)
            try:
                print(f"• Tag name: <{dropdown.tag_name}>")
                element_id = dropdown.get_attribute('id')
                if element_id:
                    print(f"• ID: {element_id}")
                element_class = dropdown.get_attribute('class')
                if element_class:
                    class_preview = element_class[:100] + "..." if len(element_class) > 100 else element_class
                    print(f"• Class: {class_preview}")
                element_role = dropdown.get_attribute('role')
                if element_role:
                    print(f"• Role: {element_role}")
                element_aria = dropdown.get_attribute('aria-label')
                if element_aria:
                    print(f"• Aria-label: {element_aria}")
                element_text = dropdown.text.strip()
                if element_text:
                    print(f"• Text: '{element_text}'")
                print(f"• Is displayed: {dropdown.is_displayed()}")
                print(f"• Is enabled: {dropdown.is_enabled()}")
                location = dropdown.location
                print(f"• Location: (x={location['x']}, y={location['y']})")
            except Exception as e:
                print(f"  Could not get all details: {str(e)}")
            print("="*60 + "\n")
            
            # Click the dropdown
            for attempt in range(3):
                try:
                    # Scroll into view
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dropdown)
                    time.sleep(0.5)
                    
                    # Try normal click
                    dropdown.click()
                    print(f"✓ Successfully clicked on element: <{dropdown.tag_name}>")
                    print("✓ Dropdown opened successfully.")
                    selectgroups.is_dropdown_opened = True
                    time.sleep(2)
                    return True
                    
                except Exception as e:
                    print(f"✗ Click attempt {attempt + 1} failed: {str(e)}")
                    if attempt == 2:
                        # Try JavaScript click as last resort
                        try:
                            driver.execute_script("arguments[0].click();", dropdown)
                            print(f"✓ Successfully clicked via JavaScript: <{dropdown.tag_name}>")
                            selectgroups.is_dropdown_opened = True
                            time.sleep(2)
                            return True
                        except Exception as js_e:
                            print(f"✗ JavaScript click also failed: {str(js_e)}")
                            return False
                    time.sleep(1)
            
            return False
            
        except Exception as e:
            print(f"✗ Failed to process dropdown operation: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def handle_page_selection(page_config):
        """Handle page profile selection/unselection based on config"""
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
                    return True
                
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
        
        return True

    def click_see_more_groups():
        """Click the 'See more groups' button to open the groups popup"""
        if selectgroups.is_see_more_clicked:
            print("'See more groups' already clicked. Skipping click operation.")
            return True
        
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
            return True
        except Exception as e:
            print(f"Failed to process 'See more groups' operation: {str(e)}")
            return False

    def handle_groups(group_config, target_group_list, normalized_targets):
        """Handle group selection/unselection based on config"""
        if group_config == 'none':
            return handle_unselect_all_groups()
        elif group_config == 'include':
            return handle_select_target_groups(target_group_list, normalized_targets)
        else:
            print(f"Invalid group config: '{group_config}'. Defaulting to no group selection.")
            return False

    def handle_unselect_all_groups():
        """Unselect all groups and save to AUTHOR_PATH"""
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
            
            # Print header for groups list
            print("\n" + "="*80)
            print("ALL GROUPS FOUND IN POPUP WINDOW (in order as seen):")
            print("="*80)
            
            selected_groups = []
            group_element_map = {}
            seen_texts = set()
            group_number = 0
            
            for i, elem in enumerate(group_elements, 1):
                try:
                    text = elem.text.strip() or elem.get_attribute('aria-label') or ''
                    lines = text.split('\n')
                    group_name = lines[0].strip() if lines else text
                    
                    # Extract member count
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
                        group_element_map[group_name] = elem
                        group_number += 1
                        
                        # Check if selected
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
                            print(f"Error checking selection for group {group_number}: {sel_e}")
                        
                        selection_status = "✓ SELECTED" if is_selected else "○ NOT SELECTED"
                        
                        # Print group information
                        print(f"\n{group_number}. {group_name}")
                        print(f"   Members: {member_count:,}" if member_count > 0 else "   Members: Unknown")
                        print(f"   Status: {selection_status}")
                        print(f"   Raw text: {text[:200]}..." if len(text) > 200 else f"   Raw text: {text}")
                        
                        if is_selected:
                            selected_groups.append(group_name)
                            
                except Exception as e:
                    print(f"Group {i}: Error extracting text - {str(e)}")
            
            print("\n" + "="*80)
            print(f"SUMMARY: Total groups found: {group_number}")
            print(f"Selected groups: {len(selected_groups)}")
            if selected_groups:
                print(f"Selected group names: {', '.join(selected_groups)}")
            print("="*80 + "\n")

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

            # Click Save and save empty selection to AUTHOR_PATH
            if click_save_button(popup_window, []):
                # Save empty selection to AUTHOR_PATH
                return save_groups_selection_to_author_path([], "no groups selected - all unselected")
            return False

        except Exception as e:
            print(f"Failed to locate popup window or process groups: {str(e)}")
            update_author_status('aborted', f"Failed to unselect groups - {str(e)}")
            return False

    def handle_select_target_groups(target_group_list, normalized_targets):
        """Select target groups based on config"""
        if not target_group_list:
            print("No target groups specified. Skipping group selection.")
            update_author_status('aborted', f"No target groups specified")
            return False
        
        if selectgroups.groups_selected:
            print("Groups already selected. Skipping selection operation.")
            selectgroups.failed_attempts = 0
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
            
            # Print header for groups list
            print("\n" + "="*80)
            print("ALL GROUPS FOUND IN POPUP WINDOW (in order as seen):")
            print("="*80)
            
            group_data = []
            group_element_map = {}
            selected_groups = []
            seen_texts = set()
            group_number = 0
            
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
                        group_element_map[group_name] = elem
                        group_number += 1
                        
                        # Check if selected
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
                            print(f"Error checking selection for group {group_number}: {sel_e}")
                        
                        selection_status = "✓ SELECTED" if is_selected else "○ NOT SELECTED"
                        
                        # Print group information
                        print(f"\n{group_number}. {group_name}")
                        print(f"   Members: {member_count:,}" if member_count > 0 else "   Members: Unknown")
                        print(f"   Status: {selection_status}")
                        print(f"   Raw text: {text[:200]}..." if len(text) > 200 else f"   Raw text: {text}")
                        
                        if is_selected:
                            selected_groups.append(group_name)
                        
                        group_data.append((group_name, member_count, elem, is_selected))
                            
                except Exception as e:
                    print(f"Group {i}: Error extracting text - {str(e)}")
            
            print("\n" + "="*80)
            print(f"SUMMARY: Total groups found: {group_number}")
            print(f"Selected groups: {len(selected_groups)}")
            if selected_groups:
                print(f"Selected group names: {', '.join(selected_groups)}")
            print("="*80 + "\n")
            
            group_count = len(group_data)
            print(f"Total groups found in popup: {group_count}")
            print(f"Number of selected groups: {len(selected_groups)}")

            # Match groups against target list using normalized comparison
            print("\n" + "="*80)
            print("MATCHING TARGET GROUPS:")
            print("="*80)
            
            matched_groups = []  # List of (original_name, element, member_count)
            unmatched_targets = list(target_group_list)  # Copy of targets to track unmatched
            
            for group_name, member_count, elem, is_selected in group_data:
                normalized_group = normalize_group_name(group_name)
                
                # Check if this group matches any target
                for norm_target, original_target in normalized_targets.items():
                    if normalized_group == norm_target:
                        print(f"✓ MATCH FOUND: '{group_name}' matches target '{original_target}'")
                        matched_groups.append((group_name, member_count, elem, is_selected))
                        if original_target in unmatched_targets:
                            unmatched_targets.remove(original_target)
                        break
                else:
                    print(f"✗ No match: '{group_name}'")
            
            print(f"\nMatched groups found: {len(matched_groups)}")
            print(f"Unmatched targets: {unmatched_targets if unmatched_targets else 'None'}")
            print("="*80 + "\n")
            
            # Determine which groups to select (up to 3, in order of target list)
            groups_to_select = []
            for target in target_group_list:
                if len(groups_to_select) >= 3:
                    break
                # Find matched group for this target
                for group_name, member_count, elem, is_selected in matched_groups:
                    norm_group = normalize_group_name(group_name)
                    norm_target = normalize_group_name(target)
                    if norm_group == norm_target and group_name not in groups_to_select:
                        groups_to_select.append(group_name)
                        print(f"Target '{target}' will be selected (matched with '{group_name}')")
                        break
                else:
                    print(f"Target '{target}' not found in available groups - skipping")
            
            # ===== CHECK IF ALL TARGETS WERE FOUND =====
            if not groups_to_select:
                error_msg = f"No target groups found in the popup window. Targets: {target_group_list}"
                print(error_msg)
                update_author_status('aborted', error_msg)
                return False
            
            # Check if any targets were unmatched
            if unmatched_targets:
                warning_msg = f"Some targets not found: {unmatched_targets}"
                print(warning_msg)
                # Don't abort if we found at least some groups
            
            print(f"\nFinal groups to select (up to 3): {groups_to_select}")

            # Unselect all currently selected groups that are not in our target list
            for group_name, member_count, elem, is_selected in group_data:
                if is_selected and group_name not in groups_to_select:
                    try:
                        clickable = elem.find_elements(By.XPATH, ".//input[@type='checkbox']") or \
                                   elem.find_elements(By.XPATH, ".//label | .//div[@role='checkbox'] | .//div[@data-testid or contains(@class, 'clickable') or contains(@class, 'selectable')]") or \
                                   [elem]
                        clickable = clickable[0]
                        
                        print(f"Attempting to unselect non-target group: {group_name}")
                        for attempt in range(3):
                            try:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clickable)
                                time.sleep(1.0)
                                driver.execute_script("arguments[0].click();", clickable)
                                time.sleep(1.5)
                                
                                # Verify unselection
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
                    except Exception as e:
                        print(f"Failed to process unselection for group {group_name}: {str(e)}")

            # Select target groups
            current_selected = []
            for group_name in groups_to_select:
                # Find the element for this group
                elem = None
                for g_name, m_count, g_elem, is_sel in group_data:
                    if g_name == group_name:
                        elem = g_elem
                        break
                
                if not elem:
                    print(f"Could not find element for group: {group_name}")
                    continue
                
                try:
                    clickable = elem.find_elements(By.XPATH, ".//input[@type='checkbox']") or \
                               elem.find_elements(By.XPATH, ".//label | .//div[@role='checkbox'] | .//div[@data-testid or contains(@class, 'clickable') or contains(@class, 'selectable')]") or \
                               [elem]
                    clickable = clickable[0]
                    
                    print(f"Attempting to select group: {group_name}")
                    
                    for attempt in range(3):
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clickable)
                            time.sleep(1.0)
                            driver.execute_script("arguments[0].click();", clickable)
                            time.sleep(1.5)
                            
                            # Verify selection
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
                                current_selected.append(group_name)
                                print(f"Selected group: {group_name} (Verified)")
                                break
                            else:
                                print(f"Attempt {attempt + 1} failed to verify selection for group: {group_name}")
                        except Exception as click_e:
                            print(f"Attempt {attempt + 1} failed to click group {group_name}: {str(click_e)}")
                except Exception as e:
                    print(f"Failed to process group {group_name}: {str(e)}")
            
            print(f"\nFinal number of selected groups: {len(current_selected)}")
            if current_selected:
                print(f"Final selected groups: {', '.join(current_selected)}")

            # ===== CHECK IF WE SELECTED ALL TARGETS =====
            if len(current_selected) < len(target_group_list):
                missing = [t for t in target_group_list if t not in current_selected]
                warning_msg = f"Could not select all target groups. Selected: {len(current_selected)}/{len(target_group_list)}. Missing: {missing}"
                print(warning_msg)
                # Don't abort - we selected some groups
            
            # Click Save and save selection to AUTHOR_PATH
            if click_save_button(popup_window, current_selected):
                # Save selection to AUTHOR_PATH
                status_msg = f"selection verified (target groups: {len(current_selected)} selected)"
                return save_groups_selection_to_author_path(current_selected, status_msg)
            return False

        except Exception as e:
            error_msg = f"Failed to locate popup window or process groups: {str(e)}"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return False

    def click_save_button(popup_window, current_selected):
        """Click the Save button"""
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
                    return True
                else:
                    print("Popup window did not close after clicking Save.")
                    return False
            except Exception as e:
                print(f"Error verifying popup closure: {str(e)}")
                return False

        except Exception as e:
            print(f"Failed to locate or click 'Save' button: {str(e)}")
            return False

    # ==================== MAIN EXECUTION ====================
    
    def main():
        """Main execution function that orchestrates all steps"""
        print("\n" + "="*80)
        print("STARTING SELECTGROUPS FUNCTION")
        print("="*80)
        
        # Step 1: Toggle dropdown
        if not toggle_dropdown():
            print("Failed to open dropdown. Exiting.")
            update_author_status('aborted', f"Failed to open dropdown")
            return False
        
        # Step 2: Handle page selection
        if not handle_page_selection(page_config):
            print("Failed to handle page selection. Exiting.")
            update_author_status('aborted', f"Failed to handle page selection")
            return False
        
        # Step 3: Click 'See more groups' if needed
        if group_config in ['none', 'include']:
            if not click_see_more_groups():
                print("Failed to click 'See more groups'. Exiting.")
                update_author_status('aborted', f"Failed to click 'See more groups'")
                return False
        
        # Step 4: Handle groups based on config
        if not handle_groups(group_config, target_group_list, normalized_targets):
            print("Failed to handle groups. Exiting.")
            return False
        
        # Update trackers
        selectgroups.groups_selected = True
        selectgroups.failed_attempts = 0
        print("Updated tracker: groups_selected set to True, failed_attempts reset to 0")
        
        # Build success message
        if group_config == 'include' and target_group_list:
            success_msg = f"Successfully selected {len(target_group_list)} groups"
            update_author_status('pending', success_msg)
        elif group_config == 'none':
            success_msg = f"Successfully unselected all groups"
            update_author_status('pending', success_msg)
        else:
            success_msg = f"Group selection completed"
            update_author_status('pending', success_msg)
        
        print("="*80)
        print("SELECTGROUPS FUNCTION COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
        
        return True
    
    # Execute main function
    return main()

def toggleaddphoto():
    """
    Toggle the 'Add photo/video' button using image matching.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses GUI_PATH for image templates
    Stores last state in AUTHOR_PATH under 'toggleaddphoto_last_state'
    """
    import os
    import json
    import random
    import time
    import pyautogui
    from PIL import ImageGrab
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, GUI_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"toggleaddphoto: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"toggleaddphoto: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"toggleaddphoto: SKIPPED - Status is 'aborted'. No action taken.")
        return

    print(f"toggleaddphoto: Starting toggle add photo/video")
    update_author_status('pending', f"Starting toggle add photo/video")

    # ---- STATE TRACKER ----
    if getattr(toggleaddphoto, 'is_toggled', False):
        print("'Add photo/video' button already toggled. Skipping.")
        return

    print("Searching for 'Add photo/video' button via image matching...")
    try:
        retry_count = 0
        max_retries = 3

        # ---- USE GLOBAL PATHS ----
        addphoto_path = os.path.join(GUI_PATH, "addphoto.png")
        addmedia_path = os.path.join(GUI_PATH, "addmedia.png")

        if not os.path.exists(addphoto_path) and not os.path.exists(addmedia_path):
            error_msg = "Neither addphoto.png nor addmedia.png found in gui folder!"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return

        # ---- LOAD OR CREATE LAST STATE IN AUTHOR_PATH ----
        config = author_data[-1] if author_data and isinstance(author_data[-1], dict) else {}
        full_state = config.get('toggleaddphoto_last_state', {})
        
        if full_state:
            print(f"Loaded last state from AUTHOR_PATH: {full_state}")
        else:
            print("No last state found in AUTHOR_PATH. Will create new.")

        last_region = full_state.get("last_region")
        print(f"Last visited region: {last_region}")

        while retry_count < max_retries:
            # ---- 1. Locate the button using image matching ----
            button_location = None
            confidence = 0.85

            for template_path in [addphoto_path, addmedia_path]:
                if not os.path.exists(template_path):
                    continue
                try:
                    loc = pyautogui.locateOnScreen(template_path, confidence=confidence)
                    if loc is not None:
                        button_location = loc
                        print(f"Found match: {os.path.basename(template_path)} at {loc}")
                        break
                except pyautogui.ImageNotFoundException:
                    continue
                except Exception as e:
                    print(f"Error during locateOnScreen({os.path.basename(template_path)}): {e}")

            if button_location is None:
                os.makedirs(GUI_PATH, exist_ok=True)
                screenshot_file = os.path.join(GUI_PATH, "windowstext_debug.png")
                screenshot = ImageGrab.grab()
                screenshot.save(screenshot_file)
                print(f"Button not found on attempt {retry_count + 1}. Screenshot saved: {screenshot_file}")

                retry_count += 1
                if retry_count >= max_retries:
                    error_msg = "Max retries reached – giving up."
                    print(error_msg)
                    update_author_status('aborted', error_msg)
                else:
                    time.sleep(1)
                continue

            # ---- 2. Calculate center of the detected button ----
            center_x = button_location.left + button_location.width // 2
            center_y = button_location.top + button_location.height // 2
            w = button_location.width
            h = button_location.height

            print(f"Detected button at center ({center_x}, {center_y})")

            # ---- Human-like mouse path ----
            screen_w, screen_h = pyautogui.size()

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

            num_moves = random.randint(0, 2)
            print(f"Performing {num_moves} random movement(s)...")

            used_regions = []
            if isinstance(last_region, (list, tuple)) and len(last_region) == 2:
                used_regions.append(tuple(last_region))

            current_region = None
            for _ in range(num_moves):
                available = [r for r in region_centers if r not in used_regions]
                if not available:
                    available = region_centers
                region = random.choice(available)
                used_regions.append(region)
                current_region = region

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

            jitter_x = random.randint(-w // 4, w // 4)
            jitter_y = random.randint(-h // 4, h // 4)
            final_x = max(0, min(center_x + jitter_x, screen_w))
            final_y = max(0, min(center_y + jitter_y, screen_h))

            print(f"Final click at: ({final_x}, {final_y})")
            pyautogui.moveTo(final_x, final_y, duration=0.2)
            time.sleep(0.2)
            pyautogui.click()
            print("Clicked 'Add photo/video' button")

            # ---- Mark as toggled & persist last state to AUTHOR_PATH ----
            toggleaddphoto.is_toggled = True

            # Update state
            full_state = {
                "last_region": list(current_region) if current_region else None,
                "last_click_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "button_found": True,
                "method": "image_matching"
            }

            # Save to AUTHOR_PATH
            author_data = load_json_file(AUTHOR_PATH, [])
            if author_data and isinstance(author_data, list) and len(author_data) > 0:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['toggleaddphoto_last_state'] = full_state
                    if save_json_file(AUTHOR_PATH, author_data):
                        print(f"SAVED: last state to AUTHOR_PATH: {full_state}")

            success_msg = "Successfully clicked 'Add photo/video' button"
            print(success_msg)
            update_author_status('pending', success_msg)

            time.sleep(3)
            selectmedia()
            return

    except Exception as e:
        error_msg = f"ERROR - {str(e)}"
        print(error_msg)
        update_author_status('aborted', error_msg)

def toggleaddphoto_ocr():
    """
    Toggle the 'Add photo/video' button using OCR text detection.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Stores last state in AUTHOR_PATH under 'toggleaddphoto_last_state'
    Falls back to image-based toggle if OCR fails
    """
    import os
    import json
    import random
    import time
    import cv2
    import numpy as np
    import pyautogui
    import pytesseract
    from PIL import ImageGrab
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, GUI_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"toggleaddphoto_: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"toggleaddphoto_: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"toggleaddphoto_: SKIPPED - Status is 'aborted'. No action taken.")
        return

    print(f"toggleaddphoto_: Starting toggle add photo/video via OCR")
    update_author_status('pending', f"Starting toggle add photo/video via OCR")

    # ---- STATE TRACKER ----
    if getattr(toggleaddphoto, 'is_toggled', False):
        print("'Add photo/video' button already toggled. Skipping.")
        return

    print("Searching for 'Add photo' or 'Add photo/video' text content")
    try:
        retry_count = 0
        max_retries = 3

        # ---- LOAD OR CREATE LAST STATE IN AUTHOR_PATH ----
        config = author_data[-1] if author_data and isinstance(author_data[-1], dict) else {}
        full_state = config.get('toggleaddphoto_last_state', {})
        
        if full_state:
            print(f"Loaded last state from AUTHOR_PATH: {full_state}")
        else:
            print("No last state found in AUTHOR_PATH. Will create new.")

        last_region = full_state.get("last_region")
        print(f"Last visited region: {last_region}")

        while retry_count < max_retries:
            # ---- 1. Capture screenshot ----
            screenshot = ImageGrab.grab()
            screenshot_cv = cv2.cvtColor(np.array(screenshot, dtype=np.uint8), cv2.COLOR_RGB2BGR)

            # Save for debugging
            os.makedirs(GUI_PATH, exist_ok=True)
            screenshot_file = os.path.join(GUI_PATH, "windowstext.png")
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

                num_moves = random.randint(0, 2)
                print(f"Performing {num_moves} random movement(s)...")

                used_regions = []
                if isinstance(last_region, (list, tuple)) and len(last_region) == 2:
                    used_regions.append(tuple(last_region))

                current_region = None
                for _ in range(num_moves):
                    available = [r for r in region_centers if r not in used_regions]
                    if not available:
                        available = region_centers
                    region = random.choice(available)
                    used_regions.append(region)
                    current_region = region

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

                jitter_x = random.randint(-w // 4, w // 4)
                jitter_y = random.randint(-h // 4, h // 4)
                final_x = max(0, min(center_x + jitter_x, screen_w))
                final_y = max(0, min(center_y + jitter_y, screen_h))

                print(f"Final click at: ({final_x}, {final_y})")
                pyautogui.moveTo(final_x, final_y, duration=0.2)
                time.sleep(0.2)
                pyautogui.click()
                print("Clicked 'Add photo/video'")

                # ---- Mark as toggled & persist last state to AUTHOR_PATH ----
                toggleaddphoto.is_toggled = True

                # Update state
                full_state = {
                    "last_region": list(current_region) if current_region else None,
                    "last_click_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "button_found": True,
                    "method": "ocr",
                    "detected_phrase": detected_phrase
                }

                # Save to AUTHOR_PATH
                author_data = load_json_file(AUTHOR_PATH, [])
                if author_data and isinstance(author_data, list) and len(author_data) > 0:
                    if isinstance(author_data[-1], dict):
                        author_data[-1]['toggleaddphoto_last_state'] = full_state
                        if save_json_file(AUTHOR_PATH, author_data):
                            print(f"SAVED: last state to AUTHOR_PATH: {full_state}")

                success_msg = "Successfully clicked 'Add photo/video' via OCR"
                print(success_msg)
                update_author_status('pending', success_msg)

                time.sleep(3)
                selectmedia()
                return

            # ---- Not found → retry logic ----
            retry_count += 1
            print(f"Retry {retry_count}/{max_retries}: Button not found")
            if retry_count >= max_retries:
                if any("loading" in t for t in text_lower):
                    print("Detected 'loading' – giving it one more second...")
                    time.sleep(1)
                    continue
                error_msg = "Max retries reached – giving up. Falling back to image-based toggle."
                print(error_msg)
                update_author_status('pending', error_msg)
                toggleaddphoto()
                return
                
            time.sleep(1)

    except Exception as e:
        error_msg = f"ERROR - {str(e)}"
        print(error_msg)
        update_author_status('aborted', error_msg)

def selectmedia():
    """
    Select media by COPYING the file path and PASTING it (faster & more reliable).
    Adds randomized human-like delays:
      - Before paste: 0.8–2.1 sec
      - Before Enter: 0.5–2.0 sec
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses FILES_ROOT for media file path
    """
    import os
    import json
    import random
    import time
    import pyautogui
    import pyperclip
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, GUI_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"selectmedia: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"selectmedia: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"selectmedia: SKIPPED - Status is 'aborted'. No action taken.")
        return

    # Initialize tracker if not already set
    if not hasattr(selectmedia, 'has_uploaded'):
        selectmedia.has_uploaded = False

    # Check if media has already been selected
    if selectmedia.has_uploaded:
        print("Media path already entered and submitted. Skipping operation.")
        return

    print(f"selectmedia: Starting media selection")
    update_author_status('pending', f"Starting media selection")

    try:
        # Load configuration to get author
        author_data = load_json_file(AUTHOR_PATH, [])
        if not author_data or not isinstance(author_data, list) or len(author_data) == 0:
            error_msg = "No author data found in AUTHOR_PATH"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
            
        config = author_data[-1] if isinstance(author_data[-1], dict) else {}
        author = config.get('author', '')
        
        if not author:
            error_msg = "No author found in config"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
            
        # ==== USE FILES_ROOT FOR MEDIA PATH ====
        file_path = os.path.join(FILES_ROOT, "next jpg", author, "card_x.jpg")

        # Ensure the file exists before attempting to input the path
        if not os.path.exists(file_path):
            error_msg = f"Media file does not exist: {file_path}"
            print(error_msg)
            update_author_status('aborted', error_msg)
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
        
        success_msg = f"Successfully selected media for author '{author}'"
        print(success_msg)
        update_author_status('pending', success_msg)

        time.sleep(3)  # Final wait for upload dialog to process
        confirmselectedmedia()

    except Exception as e:
        error_msg = f"ERROR - Failed to select media: {str(e)}"
        print(error_msg)
        selectmedia.has_uploaded = True  # Prevent retry loop
        update_author_status('aborted', error_msg)

def confirmselectedmedia():
    """
    Confirm media selection with progressive patience:
    Retry #1 → 2s, #2 → 3s, #3 → 4s, #5 → 10s
    Max 5 retries. Resets on success or full failure.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses GUI_PATH for template images
    """
    import os
    import json
    import time
    import pyautogui
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, GUI_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"confirmselectedmedia: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"confirmselectedmedia: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"confirmselectedmedia: SKIPPED - Status is 'aborted'. No action taken.")
        return False

    screen_width, screen_height = pyautogui.size()
    top = (0, 0, screen_width, screen_height)
    
    # Initialize retry tracker
    if not hasattr(confirmselectedmedia, 'retry_count'):
        confirmselectedmedia.retry_count = 0
    
    MAX_RETRIES = 5
    
    # === FAILURE: All retries used ===
    if confirmselectedmedia.retry_count >= MAX_RETRIES:
        error_msg = "All 5 retries exhausted - MEDIA SELECTION FAILED"
        print("BREAKDOWN REPORT: All 5 retries exhausted - MEDIA SELECTION FAILED")
        print(f"   Total retries attempted: {MAX_RETRIES}")
        print(f"   cropandfilter.png NOT FOUND after all attempts")
        print(f"   RECOMMENDED ACTION: Manual intervention required")
        
        update_author_status('aborted', error_msg)
        
        # Reset for next post
        confirmselectedmedia.retry_count = 0
        if hasattr(selectmedia, 'has_uploaded'):
            selectmedia.has_uploaded = False
        return False
    
    # === INCREMENT & LOG RETRY ===
    confirmselectedmedia.retry_count += 1
    attempt = confirmselectedmedia.retry_count
    print(f"RETRY #{attempt}/{MAX_RETRIES} - Looking for cropandfilter.png...")

    # === PROGRESSIVE WAIT TIMES ===
    wait_times = {1: 2, 2: 3, 3: 4, 4: 6, 5: 10}
    wait_sec = wait_times.get(attempt, 4)

    # === SEARCH FOR cropandfilter.png USING GUI_PATH ===
    try:
        template_path = os.path.join(GUI_PATH, "cropandfilter.png")
        editmedia = pyautogui.locateOnScreen(
            template_path,
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
            success_msg = f"Media confirmed selected on retry #{attempt}"
            print(success_msg)
            update_author_status('pending', success_msg)
            return True
    except Exception as e:
        print(f"   Search error on retry #{attempt}: {e}")

    # === NOT FOUND → WAIT & RETRY ===
    print(f"   cropandfilter.png NOT FOUND → waiting {wait_sec} sec before retry...")
    time.sleep(wait_sec)
    
    # Recursive call (safe: max depth 5)
    return confirmselectedmedia()

def confirm_fileisready():
    """
    Confirm file dialog is ready by looking for various UI elements.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses GUI_PATH for template images
    """
    import os
    import json
    import time
    import pyautogui
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, GUI_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"confirm_fileisready: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"confirm_fileisready: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"confirm_fileisready: SKIPPED - Status is 'aborted'. No action taken.")
        return False

    print(f"confirm_fileisready: Checking file dialog")
    update_author_status('pending', f"Checking file dialog")

    try:
        # === USE GUI_PATH FOR ALL TEMPLATES ===
        templates = [
            "file_name.png",
            "pc.png", 
            "new_folder.png",
            "customised_files.png"
        ]
        
        found_template = None
        for template in templates:
            template_path = os.path.join(GUI_PATH, template)
            if os.path.exists(template_path):
                try:
                    result = pyautogui.locateOnScreen(template_path, confidence=0.8)
                    if result:
                        found_template = template
                        print(f"✅ Found template: {template}")
                        break
                except Exception as e:
                    print(f"   Error searching for {template}: {e}")
            else:
                print(f"   Template not found: {template_path}")
        
        if found_template:
            print(f"✅ File dialog confirmed - selecting media")
            success_msg = f"File dialog confirmed via '{found_template}' - proceeding to select media"
            print(success_msg)
            update_author_status('pending', success_msg)
            selectmedia()
            print("✅ File selected")
            return True
        else:
            print("❌ File dialog not confirmed - closing")
            pyautogui.hotkey('alt', 'f4')
            warning_msg = "File dialog not found - closed dialog"
            print(warning_msg)
            update_author_status('pending', warning_msg)
            return False
    except Exception as e:
        error_msg = f"ERROR - {str(e)}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return False
      
def writecaption_element():
    """
    Write caption to the composer element using Selenium with human-like typing.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses FILES_ROOT for caption files
    Uses AUTHOR_PATH for config/status
    """
    reset_used_captions_record()
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, GUI_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"writecaption_element: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"writecaption_element: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"writecaption_element: SKIPPED - Status is 'aborted'. No action taken.")
        return None

    print(f"writecaption_element: Starting caption writing")
    update_author_status('pending', f"Starting caption writing")

    # Initialize function attributes if not already set
    if not hasattr(writecaption_element, 'has_written'):
        writecaption_element.has_written = False
    if not hasattr(writecaption_element, 'last_written_caption'):
        writecaption_element.last_written_caption = None
    
    # ---- EARLY EXIT ----
    if writecaption_element.has_written:
        print("\nCAPTION ALREADY WRITTEN. SKIPPING.")
        return None

    print("\nLOCATING COMPOSER (NIGERIA FAST MODE - TYPING ONLY)")

    # --------------------------------------------------------------------- #
    # Helper: Extract caption values from any structure
    # --------------------------------------------------------------------- #
    def extract_captions(data):
        """Extract caption values from various JSON structures."""
        captions_list = []
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    captions_list.append(item)
                elif isinstance(item, dict):
                    for key, value in item.items():
                        if key.lower() != 'id' and isinstance(value, str) and value.strip():
                            captions_list.append(value)
            return captions_list
        
        elif isinstance(data, dict):
            if 'id' in data:
                for key, value in data.items():
                    if key.lower() != 'id' and isinstance(value, str) and value.strip():
                        captions_list.append(value)
            else:
                for key, value in data.items():
                    if isinstance(value, str) and value.strip():
                        captions_list.append(value)
                    elif isinstance(value, dict):
                        captions_list.extend(extract_captions(value))
                    elif isinstance(value, list):
                        captions_list.extend(extract_captions(value))
            return captions_list
        
        return captions_list

    def get_caption_id(entry):
        """Get a unique identifier for a caption entry (skips 'id' key)."""
        if isinstance(entry, str):
            return entry
        elif isinstance(entry, dict):
            for key, value in entry.items():
                if key.lower() != 'id' and isinstance(value, str) and value.strip():
                    return value
        return None

    def get_caption_description(entry):
        """Get the caption text from an entry (skips 'id' key)."""
        if isinstance(entry, str):
            return entry
        elif isinstance(entry, dict):
            for key, value in entry.items():
                if key.lower() != 'id' and isinstance(value, str) and value.strip():
                    return value
        return None

    # --------------------------------------------------------------------- #
    # 0. Load caption and config
    # --------------------------------------------------------------------- #
    try:
        config = author_data[-1] if author_data and isinstance(author_data[-1], dict) else {}
        
        author = config.get('author', '').strip()
        if not author:
            error_msg = "No author found in config"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return None
            
        author_lower = author.lower()
        
        include_profile_link = config.get('include_profile_link', False)
        tag = config.get('tag', '').strip()
        captions_state = config.get('captions_state', 'mixed').lower().strip()
        
        post_filter = config.get('post_filter', 'others').lower().strip()
        if post_filter not in ['uk', 'others']:
            post_filter = 'others'
        
        # ==== USE FILES_ROOT FOR CAPTION PATH ====
        captions_dir = os.path.join(FILES_ROOT, "captions")
        json_path = os.path.join(captions_dir, f"{author}({post_filter}).json")
        
        if not os.path.exists(json_path):
            alt_path = os.path.join(captions_dir, f"{author_lower}({post_filter}).json")
            if os.path.exists(alt_path):
                json_path = alt_path
            else:
                error_msg = f"Caption file not found: {json_path}"
                print(error_msg)
                update_author_status('aborted', error_msg)
                return None

        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        captions = extract_captions(raw_data)
        
        if not captions:
            error_msg = f"No captions found in {json_path}"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return None
        
        print(f"✅ Extracted {len(captions)} captions from {json_path}")

        # --------------------------------------------------------------------- #
        # Handle FIXED captions state - track used captions
        # --------------------------------------------------------------------- #
        used_captions_path = os.path.join(captions_dir, f"{author}({post_filter})_used.json")
        used_captions = []
        available_captions = []
        
        if captions_state == "fixed":
            print(f"\n📌 FIXED CAPTIONS MODE ENABLED - Tracking used captions")
            
            if os.path.exists(used_captions_path):
                try:
                    with open(used_captions_path, 'r', encoding='utf-8') as f:
                        used_captions = json.load(f)
                    print(f"📊 Loaded {len(used_captions)} used captions from: {used_captions_path}")
                except Exception as e:
                    print(f"⚠️ Error loading used_captions.json: {e}")
                    used_captions = []
            
            available_captions = []
            for caption_entry in captions:
                caption_id = get_caption_id(caption_entry)
                if caption_id not in used_captions:
                    available_captions.append(caption_entry)
            
            print(f"📊 Total captions: {len(captions)}, Used: {len(used_captions)}, Available: {len(available_captions)}")
            
            if len(available_captions) == 0:
                print("⚠️ ALL CAPTIONS HAVE BEEN USED! Resetting used captions list...")
                used_captions = []
                available_captions = captions.copy()
                print(f"📊 Reset - Available captions: {len(available_captions)}")
                
                try:
                    with open(used_captions_path, 'w', encoding='utf-8') as f:
                        json.dump([], f, indent=2)
                    print("✅ Reset used_captions.json")
                except Exception as e:
                    print(f"⚠️ Error resetting used_captions.json: {e}")
            
            selected_caption_entry = random.choice(available_captions)
            selected_caption = get_caption_description(selected_caption_entry)
            caption_id = get_caption_id(selected_caption_entry)
            
            print(f"📝 Selected caption (ID: {caption_id[:50] if caption_id else 'N/A'}...): '{selected_caption[:100] if selected_caption else ''}...'")
            
        else:
            print(f"\n🔄 MIXED CAPTIONS MODE - No tracking")
            selected_caption_entry = random.choice(captions)
            selected_caption = get_caption_description(selected_caption_entry)
            caption_id = get_caption_id(selected_caption_entry)
            print(f"Selected caption: '{selected_caption}'")
        
        print(f"Caption: '{selected_caption}'")
        
        # --------------------------------------------------------------------- #
        # Load profile link if needed
        # --------------------------------------------------------------------- #
        profile_link = None
        if include_profile_link:
            print("PROFILE LINK ENABLED - Fetching from pageandgroupaccounts.json")
            try:
                page_group_path = os.path.join(os.path.dirname(AUTHOR_PATH), "pageandgroupaccounts.json")
                if os.path.exists(page_group_path):
                    with open(page_group_path, 'r', encoding='utf-8') as pg_file:
                        page_group_data = json.load(pg_file)
                    
                    found = False
                    for key in page_group_data.keys():
                        if key.lower() == author_lower:
                            if 'profile_link' in page_group_data[key]:
                                profile_link = page_group_data[key]['profile_link']
                                if isinstance(profile_link, list):
                                    profile_link = profile_link[0]
                                print(f"✅ Found profile link for '{author}': {profile_link}")
                                found = True
                            else:
                                print(f"⚠️ No profile_link found for '{author}' in pageandgroupaccounts.json")
                            break
                    
                    if not found:
                        print(f"⚠️ Author '{author}' not found in pageandgroupaccounts.json")
                else:
                    print(f"⚠️ pageandgroupaccounts.json not found at: {page_group_path}")
            except Exception as e:
                print(f"⚠️ Error loading profile link: {e}")

    except Exception as e:
        error_msg = f"ERROR - {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
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
        if 'driver' not in globals() and 'driver' not in locals():
            error_msg = "Selenium driver not found. Make sure driver is initialized."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return None
            
        candidates = WebDriverWait(driver, 8).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        print(f"Found {len(candidates)} candidate(s).")
    except Exception as e:
        print(f"No candidates found or error: {e}")
        update_author_status('pending', f"No candidates found")
        return None

    # --------------------------------------------------------------------- #
    # 2. SPEED TYPING ENGINE
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

        total_len = len(text)
        p1 = total_len // 3
        p2 = (total_len - p1) // 2
        p3 = total_len - p1 - p2

        parts = [text[:p1], text[p1:p1+p2], text[p1+p2:]]

        if len(speed_profile) < 3:
            speed_profile = ["fast", "fast", "fast"]

        for i, part in enumerate(parts):
            if not part:
                continue
            min_d, max_d = speed_map[speed_profile[i]]
            for char in part:
                ActionChains(driver).send_keys(char).perform()
                time.sleep(random.uniform(min_d, max_d))

    # --------------------------------------------------------------------- #
    # 3. 5 BEHAVIORS (SPEED PROFILES ONLY)
    # --------------------------------------------------------------------- #
    def b1_s_f_s(el, text):
        print("  [1] Slow-Fast-Slow | Profile: ['slow', 'fast', 'slow']")
        type_with_speed(el, text, ["slow", "fast", "slow"])

    def b2_f_s_f(el, text):
        print("  [2] Fast-Slow-Fast | Profile: ['fast', 'slow', 'fast']")
        type_with_speed(el, text, ["fast", "slow", "fast"])

    def b3_s_s_f(el, text):
        print("  [3] Slow-Slow-Fast | Profile: ['slow', 'slow', 'fast']")
        type_with_speed(el, text, ["slow", "slow", "fast"])

    def b4_f_s_s(el, text):
        print("  [4] Fast-Slow-Slow | Profile: ['fast', 'slow', 'slow']")
        type_with_speed(el, text, ["fast", "slow", "slow"])

    def b5_f_f_s(el, text):
        print("  [5] Fast-Fast-Slow | Profile: ['fast', 'fast', 'slow']")
        type_with_speed(el, text, ["fast", "fast", "slow"])
    
    behaviors = [
        ("s_f_s", b1_s_f_s),
        ("f_s_f", b2_f_s_f),
        ("s_s_f", b3_s_s_f),
        ("f_s_s", b4_f_s_s),
        ("f_f_s", b5_f_f_s),
    ]
    behavior_order = [b[0] for b in behaviors]
    MAX_BEHAVIORS = len(behavior_order)

    # --------------------------------------------------------------------- #
    # 4. LOAD laststate.json - Use FILES_ROOT
    # --------------------------------------------------------------------- #
    laststate_path = os.path.join(os.path.dirname(AUTHOR_PATH), "laststate.json")
    used_behaviors = []
    last_used_behavior = None

    if os.path.exists(laststate_path):
        try:
            with open(laststate_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                used = data.get("write_caption_previous_behaviors", [])
                used_behaviors = [s for s in used if s in behavior_order]
                last_used_behavior = data.get("caption_last_used")
                if last_used_behavior not in behavior_order:
                    last_used_behavior = None
        except Exception as e:
            print(f"ERROR reading laststate.json: {e}")

    print(f"Used: {len(used_behaviors)}/{MAX_BEHAVIORS} → {used_behaviors}")
    print(f"Last: {last_used_behavior}")

    # --------------------------------------------------------------------- #
    # 5. PICK NEXT BEHAVIOR
    # --------------------------------------------------------------------- #
    next_behavior_key = None
    if len(used_behaviors) < MAX_BEHAVIORS:
        for key in behavior_order:
            if key not in used_behaviors:
                next_behavior_key = key
                break
    else:
        if last_used_behavior and last_used_behavior in behavior_order:
            last_index = behavior_order.index(last_used_behavior)
            next_index = (last_index + 1) % MAX_BEHAVIORS
            next_behavior_key = behavior_order[next_index]
        else:
            next_behavior_key = behavior_order[0]

    chosen_func = dict(behaviors)[next_behavior_key]
    print(f"USING: {next_behavior_key.upper()}")

    # --------------------------------------------------------------------- #
    # 6. Helper functions
    # --------------------------------------------------------------------- #
    def get_element_text(el):
        return driver.execute_script(
            "return arguments[0].textContent || arguments[0].innerText || '';", el
        ).strip()
    
    def check_mention_exists(el, tag):
        if not tag:
            return False
        
        tag_clean = tag.lstrip('@').strip()
        
        try:
            mention_xpaths = [
                ".//span[contains(@class, 'mention')]",
                ".//a[contains(@class, 'mention')]",
                ".//div[contains(@class, 'mention')]",
                ".//span[@data-username]",
                ".//a[@data-username]",
                ".//span[contains(@class, 'atwho')]",
                ".//span[contains(@class, 'Mention')]",
                ".//span[@data-type='mention']",
                ".//a[contains(@href, 'profile')]",
                ".//span[contains(@data-offset-key, 'mention')]",
                ".//span[contains(@data-text, '@')]",
                ".//div[contains(@data-type, 'mention')]",
                ".//span[contains(@class, 'rq0escxv') and contains(@class, 'mentions')]",
                ".//span[contains(@class, 'Igw0E') and contains(@class, 'mentions')]",
                ".//span[contains(@data-testid, 'mention')]",
                ".//span[contains(@role, 'button') and contains(@class, 'mention')]",
            ]
            
            for xpath in mention_xpaths:
                try:
                    mentions = el.find_elements(By.XPATH, xpath)
                    for mention in mentions:
                        if mention.is_displayed():
                            mention_text = mention.text.strip().lower()
                            mention_username = mention.get_attribute('data-username') or ''
                            mention_text_content = mention.get_attribute('textContent') or ''
                            
                            if (tag_clean in mention_text or 
                                tag_clean in mention_username or 
                                tag_clean in mention_text_content or
                                mention_text in tag_clean or
                                mention_username in tag_clean):
                                print(f"  ✅ Found mention element: '{mention_text}'")
                                return True
                except:
                    continue
            
            try:
                script = """
                var elements = arguments[0].getElementsByTagName('*');
                var tag = arguments[1].toLowerCase();
                for (var i = 0; i < elements.length; i++) {
                    var el = elements[i];
                    var text = el.textContent || el.innerText || '';
                    if (text && text.toLowerCase().includes(tag)) {
                        return true;
                    }
                }
                return false;
                """
                result = driver.execute_script(script, el, tag_clean)
                if result:
                    print(f"  ✅ Found text containing tag in element tree")
                    return True
            except:
                pass
            
            return False
            
        except Exception as e:
            print(f"  Error checking mentions: {e}")
            return False
    
    def clear_composer_content(el):
        try:
            ActionChains(driver).click(el).perform()
            time.sleep(0.1)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
            ActionChains(driver).send_keys(Keys.DELETE).perform()
            time.sleep(0.3)
            print("  ✅ Composer cleared")
            return True
        except Exception as e:
            print(f"  ❌ Error clearing composer: {e}")
            return False
    
    def add_line_breaks(el, count=5):
        try:
            ActionChains(driver).click(el).perform()
            time.sleep(0.2)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
            
            print(f"  Adding {count} line breaks...")
            for line_num in range(1, count + 1):
                ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                time.sleep(0.05)
                print(f"    Line break {line_num}/{count} added")
            return True
        except Exception as e:
            print(f"  ❌ Error adding line breaks: {e}")
            return False
    
    def add_tag_with_autocomplete(driver, el, tag, max_attempts=3):
        if not tag:
            return True
        
        print(f"  ADDING TAG: {tag}")
        tag_without_at = tag.lstrip('@')
        
        for attempt in range(max_attempts):
            print(f"  Attempt {attempt + 1}/{max_attempts}")
            
            try:
                ActionChains(driver).click(el).perform()
                time.sleep(0.2)
                ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
                time.sleep(0.1)
                
                if check_mention_exists(el, tag):
                    print(f"  ✅ Mention already exists: {tag}")
                    return True
                
                for char in tag:
                    ActionChains(driver).send_keys(char).perform()
                    time.sleep(random.uniform(0.02, 0.05))
                
                print(f"  Waiting 2 seconds for suggestions to load...")
                time.sleep(2)
                
                suggestion_selected = False
                
                suggestion_xpaths = [
                    "//div[contains(@class, 'suggestions')]//li",
                    "//div[contains(@class, 'autocomplete')]//li",
                    "//ul[contains(@class, 'suggestions')]//li",
                    "//div[contains(@role, 'listbox')]//li",
                    "//div[contains(@class, 'menu')]//div[contains(@role, 'option')]",
                    "//div[contains(@class, 'typeahead')]//li",
                    "//div[contains(@class, 'dropdown-menu')]//li",
                    "//div[contains(@class, 'mention-suggestions')]//li",
                    "//div[@data-testid='typeahead']//li",
                    "//div[@aria-label='Suggestions']//li",
                    "//div[contains(@class, 'Igw0E')]//li",
                    "//div[contains(@class, 'rq0escxv')]//li",
                ]
                
                for xpath in suggestion_xpaths:
                    try:
                        suggestions = driver.find_elements(By.XPATH, xpath)
                        visible_suggestions = [s for s in suggestions if s.is_displayed()]
                        
                        if visible_suggestions:
                            for suggestion in visible_suggestions:
                                try:
                                    suggestion_text = suggestion.text.strip().lower()
                                    if (tag_without_at.lower() in suggestion_text or 
                                        suggestion_text in tag_without_at.lower()):
                                        suggestion.click()
                                        print(f"  ✅ Selected matching suggestion: '{suggestion_text}'")
                                        suggestion_selected = True
                                        break
                                except:
                                    continue
                            
                            if not suggestion_selected:
                                visible_suggestions[0].click()
                                print(f"  ✅ Selected first suggestion")
                                suggestion_selected = True
                            break
                    except:
                        continue
                
                if not suggestion_selected:
                    print("  No clickable suggestions found, trying keyboard navigation...")
                    try:
                        ActionChains(driver).send_keys(Keys.TAB).perform()
                        suggestion_selected = True
                        print("  ✅ Used keyboard navigation")
                        time.sleep(0.3)
                    except:
                        pass
                
                if not suggestion_selected:
                    print("  No suggestions, pressing Enter...")
                    ActionChains(driver).send_keys(Keys.ENTER).perform()
                    time.sleep(0.3)
                
                print("  Confirming tag selection...")
                time.sleep(1)
                
                if check_mention_exists(el, tag):
                    print(f"  ✅ Tag successfully confirmed as mention: {tag}")
                    return True
                
                final_text = get_element_text(el)
                if tag in final_text:
                    print(f"  ⚠️ Tag found as text (not mention), but acceptable")
                    return True
                
                print(f"  ⚠️ Tag not properly added. Retrying...")
                continue
                    
            except Exception as e:
                print(f"  ❌ Error on attempt {attempt + 1}: {e}")
                continue
        
        print(f"  ❌ Failed to add tag after {max_attempts} attempts")
        return False
    
    def add_profile_link_with_typing(el, link):
        if not link:
            return True
        
        print(f"  ADDING PROFILE LINK: {link}")
        try:
            ActionChains(driver).click(el).perform()
            time.sleep(0.2)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
            
            for char in link:
                ActionChains(driver).send_keys(char).perform()
                time.sleep(random.uniform(0.02, 0.05))
            
            time.sleep(0.3)
            print(f"  ✅ Profile link added successfully")
            return True
        except Exception as e:
            print(f"  ❌ Error adding profile link: {e}")
            return False

    # --------------------------------------------------------------------- #
    # 7. Test candidates
    # --------------------------------------------------------------------- #
    working_element = None
    selected_caption_lower = selected_caption.lower()

    for i, el in enumerate(candidates):
        try:
            if not el.is_displayed():
                continue

            print(f"  [{i}] Testing → {next_behavior_key}")

            current = driver.execute_script(
                "return arguments[0].textContent || arguments[0].innerText || '';", el
            ).strip()

            if selected_caption_lower in current.lower():
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

            if selected_caption_lower in final.lower():
                print(f"  SUCCESS! Composer locked.")
                working_element = el
                writecaption_element.has_written = True
                writecaption_element.last_written_caption = selected_caption
                
                if not add_line_breaks(el, 5):
                    print("  ❌ Failed to add line breaks, clearing and restarting...")
                    clear_composer_content(el)
                    continue
                
                if tag:
                    tag_success = add_tag_with_autocomplete(driver, el, tag, max_attempts=3)
                    if not tag_success:
                        print("  ❌ Failed to add tag, clearing and restarting...")
                        clear_composer_content(el)
                        continue
                
                if include_profile_link and profile_link:
                    if not add_profile_link_with_typing(el, profile_link):
                        print("  ❌ Failed to add profile link, clearing and restarting...")
                        clear_composer_content(el)
                        continue
                
                final_text = get_element_text(el)
                print(f"  Final text: '{final_text[:100]}...'")
                
                caption_ok = selected_caption_lower in final_text.lower()
                tag_ok = not tag or check_mention_exists(el, tag)
                if not tag_ok:
                    tag_ok = tag in final_text
                link_ok = not include_profile_link or not profile_link or (profile_link in final_text)
                
                if caption_ok and tag_ok and link_ok:
                    print("  ✅ All content successfully added!")
                    
                    if captions_state == "fixed":
                        try:
                            if caption_id not in used_captions:
                                used_captions.append(caption_id)
                            
                            with open(used_captions_path, 'w', encoding='utf-8') as f:
                                json.dump(used_captions, f, indent=2)
                            print(f"✅ Saved used caption to: {used_captions_path}")
                            print(f"📊 Total used captions: {len(used_captions)}")
                        except Exception as e:
                            print(f"⚠️ Error saving used caption: {e}")
                else:
                    print("  ⚠️ Some content may not have been added correctly, clearing and restarting...")
                    if not caption_ok:
                        print("    - Caption missing")
                    if not tag_ok:
                        print("    - Tag missing or not properly tagged")
                    if not link_ok:
                        print("    - Profile link missing")
                    
                    clear_composer_content(el)
                    continue

                if next_behavior_key not in used_behaviors:
                    used_behaviors.append(next_behavior_key)
                else:
                    used_behaviors.remove(next_behavior_key)
                    used_behaviors.append(next_behavior_key)
                used_behaviors = used_behaviors[-MAX_BEHAVIORS:]

                state_data = {}
                if os.path.exists(laststate_path):
                    try:
                        with open(laststate_path, 'r', encoding='utf-8') as f:
                            state_data = json.load(f)
                    except:
                        pass

                state_data.update({
                    "write_caption_previous_behaviors": used_behaviors,
                    "caption_last_used": next_behavior_key
                })

                try:
                    with open(laststate_path, 'w', encoding='utf-8') as f:
                        json.dump(state_data, f, indent=2)
                    print(f"SAVED: {len(used_behaviors)}/{MAX_BEHAVIORS} | Last: {next_behavior_key}")
                except Exception as e:
                    print(f"ERROR writing laststate.json: {e}")

                break
            else:
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                ActionChains(driver).send_keys(Keys.DELETE).perform()

        except Exception as e:
            print(f"  [{i}] Error: {e}")

    # --------------------------------------------------------------------- #
    # 8. Return
    # --------------------------------------------------------------------- #
    if working_element:
        print(f"\nCOMPOSER FOUND | {next_behavior_key.upper()} | NIGERIA FAST MODE")
        success_msg = f"Successfully wrote caption using {next_behavior_key.upper()} behavior"
        update_author_status('pending', success_msg)
        return working_element
    else:
        print("\nFallback to OCR...")
        update_author_status('pending', f"Falling back to OCR method")
        return writecaption_ocr()

def writecaption_ocr():
    """Enter a random caption using GUI automation with OCR text detection.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses FILES_ROOT for caption files
    Uses GUI_PATH for debug screenshots
    """
    reset_used_captions_record()
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, GUI_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"writecaption_ocr: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"writecaption_ocr: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"writecaption_ocr: SKIPPED - Status is 'aborted'. No action taken.")
        return False

    print(f"writecaption_ocr: Starting caption writing via OCR")
    update_author_status('pending', f"Starting caption writing via OCR")

    if not hasattr(writecaption_ocr, 'last_written_caption'):
        writecaption_ocr.last_written_caption = None

    # --------------------------------------------------------------------- #
    # Helper: Extract caption values
    # --------------------------------------------------------------------- #
    def extract_captions_ocr(data):
        """Extract caption values from various JSON structures."""
        captions_list = []
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    captions_list.append(item)
                elif isinstance(item, dict):
                    for key, value in item.items():
                        if key.lower() != 'id' and isinstance(value, str) and value.strip():
                            captions_list.append(value)
            return captions_list
        
        elif isinstance(data, dict):
            if 'id' in data:
                for key, value in data.items():
                    if key.lower() != 'id' and isinstance(value, str) and value.strip():
                        captions_list.append(value)
            else:
                for key, value in data.items():
                    if isinstance(value, str) and value.strip():
                        captions_list.append(value)
                    elif isinstance(value, dict):
                        captions_list.extend(extract_captions_ocr(value))
                    elif isinstance(value, list):
                        captions_list.extend(extract_captions_ocr(value))
            return captions_list
        
        return captions_list

    def get_caption_id_ocr(entry):
        if isinstance(entry, str):
            return entry
        elif isinstance(entry, dict):
            for key, value in entry.items():
                if key.lower() != 'id' and isinstance(value, str) and value.strip():
                    return value
        return None

    def get_caption_description_ocr(entry):
        if isinstance(entry, str):
            return entry
        elif isinstance(entry, dict):
            for key, value in entry.items():
                if key.lower() != 'id' and isinstance(value, str) and value.strip():
                    return value
        return None

    try:
        config = author_data[-1] if author_data and isinstance(author_data[-1], dict) else {}
        
        author = config.get('author', '').strip()
        if not author:
            error_msg = "No author found in config"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return False
            
        post_filter = config.get('post_filter', 'others').lower().strip()
        captions_state = config.get('captions_state', 'mixed').lower().strip()
        print(f"Read from {AUTHOR_PATH}: author='{author}', post_filter='{post_filter}', captions_state='{captions_state}'")
        
        if post_filter not in ['uk', 'others']:
            print(f"Invalid post_filter value: '{post_filter}'. Defaulting to 'others'.")
            post_filter = 'others'
        
        # ==== USE FILES_ROOT FOR CAPTION PATH ====
        captions_dir = os.path.join(FILES_ROOT, "captions")
        json_path = os.path.join(captions_dir, f"{author}({post_filter}).json")
        print(f"Constructed JSON path: {json_path}")
        
        if not os.path.exists(json_path):
            error_msg = f"JSON file not found at {json_path}"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return False
        
        with open(json_path, 'r') as file:
            raw_data = json.load(file)
        
        captions = extract_captions_ocr(raw_data)
        
        if not captions:
            print(f"❌ No captions found in {json_path}")
            update_author_status('pending', f"No captions found in {json_path}")
            return False
        
        print(f"✅ Extracted {len(captions)} captions from {json_path}")
        
        # --------------------------------------------------------------------- #
        # Handle FIXED captions state
        # --------------------------------------------------------------------- #
        used_captions_path = os.path.join(captions_dir, f"{author}({post_filter})_used.json")
        used_captions = []
        available_captions = []
        caption_id = None
        selected_caption = None
        
        if captions_state == "fixed":
            print(f"\n📌 FIXED CAPTIONS MODE ENABLED - Tracking used captions (GUI)")
            
            if os.path.exists(used_captions_path):
                try:
                    with open(used_captions_path, 'r', encoding='utf-8') as f:
                        used_captions = json.load(f)
                    print(f"📊 Loaded {len(used_captions)} used captions from: {used_captions_path}")
                except Exception as e:
                    print(f"⚠️ Error loading used_captions.json: {e}")
                    used_captions = []
            
            available_captions = []
            for caption_entry in captions:
                caption_id_check = get_caption_id_ocr(caption_entry)
                if caption_id_check not in used_captions:
                    available_captions.append(caption_entry)
            
            print(f"📊 Total captions: {len(captions)}, Used: {len(used_captions)}, Available: {len(available_captions)}")
            
            if len(available_captions) == 0:
                print("⚠️ ALL CAPTIONS HAVE BEEN USED! Resetting used captions list...")
                used_captions = []
                available_captions = captions.copy()
                print(f"📊 Reset - Available captions: {len(available_captions)}")
                
                try:
                    with open(used_captions_path, 'w', encoding='utf-8') as f:
                        json.dump([], f, indent=2)
                    print("✅ Reset used_captions.json")
                except Exception as e:
                    print(f"⚠️ Error resetting used_captions.json: {e}")
            
            selected_caption_entry = random.choice(available_captions)
            selected_caption = get_caption_description_ocr(selected_caption_entry)
            caption_id = get_caption_id_ocr(selected_caption_entry)
            
            print(f"📝 Selected caption (ID: {caption_id[:50] if caption_id else 'N/A'}...): '{selected_caption[:100] if selected_caption else ''}...'")
            
        else:
            print(f"\n🔄 MIXED CAPTIONS MODE - No tracking (GUI)")
            selected_caption_entry = random.choice(captions)
            selected_caption = get_caption_description_ocr(selected_caption_entry)
            caption_id = get_caption_id_ocr(selected_caption_entry)
            print(f"Selected random caption for author '{author}' (post_filter '{post_filter}', GUI): '{selected_caption}'")
        
        print("Searching for 'text' to locate input field")
        retry_count = 0
        max_retries = 3
        
        # ==== USE GUI_PATH FOR DEBUG SCREENSHOTS ====
        while retry_count < max_retries:
            screenshot = ImageGrab.grab()
            screenshot_cv = cv2.cvtColor(np.array(screenshot, dtype=np.uint8), cv2.COLOR_RGB2BGR)
            
            os.makedirs(GUI_PATH, exist_ok=True)
            screenshot_file = os.path.join(GUI_PATH, "caption_text_area.png")
            cv2.imwrite(screenshot_file, screenshot_cv)
            print(f"Screenshot captured and saved as '{screenshot_file}'")
            
            gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            resized = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            thresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT, config='--psm 3')
            print("OCR data keys:", data.keys())
            print("All detected text with positions:")
            for i, text in enumerate(data["text"]):
                if text.strip():
                    print(f"Index {i}: '{text}' (Confidence: {data['conf'][i]}, Left: {data['left'][i]}, Top: {data['top'][i]})")
            
            text_lower = [t.lower() for t in data["text"]]
            text_index = None
            for i, text in enumerate(text_lower):
                if text == "text":
                    text_index = i
                    break
            
            if text_index is not None:
                x = data["left"][text_index] // 1.5
                y = data["top"][text_index] // 1.5
                w = data["width"][text_index] // 1.5
                h = data["height"][text_index] // 1.5
                center_x = x + w // 2
                center_y = y + h // 2
                print(f"Detected: 'text'")
                print(f"Coordinates: left={x}, top={y}, width={w}, height={h}")
                print(f"Moving to: ({center_x}, {center_y})")
                
                pyautogui.moveTo(center_x, center_y + 50)
                time.sleep(0.1)
                pyautogui.click()
                print("✅ Clicked on 'text' input field")
                time.sleep(1)
                
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.5)
                current_text = pyperclip.paste().strip()
                print(f"Current text in field (GUI): '{current_text}'")
                
                if not current_text or (current_text != selected_caption and current_text != writecaption_ocr.last_written_caption):
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('delete')
                    time.sleep(0.5)
                    
                    pyautogui.write(selected_caption)
                    print(f"Entered text into post field (GUI): '{selected_caption}'")
                    
                    writecaption_ocr.last_written_caption = selected_caption
                    print(f"Saved caption to last_written_caption (GUI): '{selected_caption}'")
                    time.sleep(1)
                    
                    if captions_state == "fixed" and caption_id:
                        try:
                            if caption_id not in used_captions:
                                used_captions.append(caption_id)
                            
                            with open(used_captions_path, 'w', encoding='utf-8') as f:
                                json.dump(used_captions, f, indent=2)
                            print(f"✅ Saved used caption to: {used_captions_path}")
                            print(f"📊 Total used captions: {len(used_captions)}")
                        except Exception as e:
                            print(f"⚠️ Error saving used caption: {e}")
                    
                    success_msg = f"Successfully wrote caption via OCR for author '{author}'"
                    update_author_status('pending', success_msg)
                    return True
                
                elif current_text == selected_caption or current_text == writecaption_ocr.last_written_caption:
                    print(f"Text '{current_text}' is already correct in the text field (GUI). Skipping write operation.")
                    if current_text == selected_caption:
                        writecaption_ocr.last_written_caption = selected_caption
                        print(f"Updated last_written_caption to match current text (GUI): '{selected_caption}'")
                        
                        if captions_state == "fixed" and caption_id:
                            try:
                                if os.path.exists(used_captions_path):
                                    with open(used_captions_path, 'r', encoding='utf-8') as f:
                                        current_used = json.load(f)
                                else:
                                    current_used = []
                                
                                if caption_id not in current_used:
                                    current_used.append(caption_id)
                                    with open(used_captions_path, 'w', encoding='utf-8') as f:
                                        json.dump(current_used, f, indent=2)
                                    print(f"✅ Saved used caption to: {used_captions_path}")
                                    print(f"📊 Total used captions: {len(current_used)}")
                            except Exception as e:
                                print(f"⚠️ Error saving used caption: {e}")
                    
                    success_msg = f"Caption already present - skipping write"
                    update_author_status('pending', success_msg)
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
                        
                        if captions_state == "fixed" and caption_id:
                            try:
                                if os.path.exists(used_captions_path):
                                    with open(used_captions_path, 'r', encoding='utf-8') as f:
                                        current_used = json.load(f)
                                else:
                                    current_used = []
                                
                                if caption_id not in current_used:
                                    current_used.append(caption_id)
                                    with open(used_captions_path, 'w', encoding='utf-8') as f:
                                        json.dump(current_used, f, indent=2)
                                    print(f"✅ Saved used caption to: {used_captions_path}")
                                    print(f"📊 Total used captions: {len(current_used)}")
                            except Exception as e:
                                print(f"⚠️ Error saving used caption: {e}")
                    else:
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.hotkey('delete')
                        time.sleep(0.5)
                        pyautogui.write(selected_caption)
                        writecaption_ocr.last_written_caption = selected_caption
                        print(f"No previous caption saved. Entered new caption (GUI): '{selected_caption}'")
                        time.sleep(1)
                        
                        if captions_state == "fixed" and caption_id:
                            try:
                                if os.path.exists(used_captions_path):
                                    with open(used_captions_path, 'r', encoding='utf-8') as f:
                                        current_used = json.load(f)
                                else:
                                    current_used = []
                                
                                if caption_id not in current_used:
                                    current_used.append(caption_id)
                                    with open(used_captions_path, 'w', encoding='utf-8') as f:
                                        json.dump(current_used, f, indent=2)
                                    print(f"✅ Saved used caption to: {used_captions_path}")
                                    print(f"📊 Total used captions: {len(current_used)}")
                            except Exception as e:
                                print(f"⚠️ Error saving used caption: {e}")
                    
                    success_msg = f"Replaced caption via OCR for author '{author}'"
                    update_author_status('pending', success_msg)
                    return True
                
                return True
            
            else:
                retry_count += 1
                print(f"Retry {retry_count}/{max_retries}: No 'text' found")
                if retry_count == max_retries:
                    print("Max retries reached. No 'text' input field found.")
                    update_author_status('pending', f"Max retries reached - no text input found")
                    return False
                time.sleep(1)
        
        return False
    
    except Exception as e:
        error_msg = f"ERROR - {str(e)}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return False          

def extract_texts(return_time_value=None, additional_texts=None):
    """Extract all visible text from the current webpage, construct a time value in the format 'Time: HH:MM',
    and check for additional specified text values.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses AUTHOR_PATH global constant
    
    Args:
        return_time_value (callable, optional): A callback function to receive the time value.
        additional_texts (list, optional): A list of text values to check for in the extracted texts.
    Returns:
        tuple: A tuple containing:
            - extractedtexts (list): List of all extracted non-empty text from the webpage.
            - time_value (str or None): The constructed time value in 'Time: HH:MM' format, or None if not found.
            - found_texts (list): List of additional text values that were found in the extracted texts.
    """
    import os
    import json
    import re
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH is already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"extract_texts: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"extract_texts: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"extract_texts: SKIPPED - Status is 'aborted'. No action taken.")
        return [], None, []

    print(f"extract_texts: Starting text extraction")
    update_author_status('pending', f"Starting text extraction")

    global driver
    try:
        elements = driver.find_elements(By.XPATH, "//*[text()]")
        extractedtexts = []
        time_components = []
        found_texts = []

        for element in elements:
            text = element.text.strip()
            if text:
                extractedtexts.append(text)
                if additional_texts and text in additional_texts:
                    found_texts.append(text)
        
        time_value = None
        
        # Method 1: Look for text that starts with "Time:" and contains time format
        for text in extractedtexts:
            if text.startswith("Time:") and ":" in text:
                time_part = text.replace("Time:", "").strip()
                if re.match(r"^\d{1,2}:\d{2}$", time_part):
                    hours, minutes = time_part.split(":")
                    hours = hours.zfill(2)
                    minutes = minutes.zfill(2)
                    time_value = f"Time: {hours}:{minutes}"
                    break
        
        # Method 2: Look for separate time components
        if not time_value:
            for text in extractedtexts:
                if re.match(r"^\d{1,2}:\d{2}$", text):
                    hours, minutes = text.split(":")
                    hours = hours.zfill(2)
                    minutes = minutes.zfill(2)
                    time_value = f"Time: {hours}:{minutes}"
                    break
        
        # Method 3: Look for the pattern with "Time input", hours, ':', minutes
        if not time_value:
            potential_components = []
            for element in elements:
                text = element.text.strip()
                if text and (text == 'Time input' or text == ':' or text.isdigit() or re.match(r"^\d{1,2}:\d{2}$", text)):
                    potential_components.append(text)
            
            for i in range(len(potential_components) - 3):
                if (potential_components[i] == 'Time input' and 
                    potential_components[i+1].isdigit() and 
                    len(potential_components[i+1]) <= 2 and
                    potential_components[i+2] == ':' and 
                    potential_components[i+3].isdigit() and 
                    len(potential_components[i+3]) <= 2):
                    hours = potential_components[i+1].zfill(2)
                    minutes = potential_components[i+3].zfill(2)
                    time_value = f"Time: {hours}:{minutes}"
                    break
            
            if not time_value:
                for i in range(len(potential_components) - 2):
                    if (potential_components[i].isdigit() and 
                        len(potential_components[i]) <= 2 and
                        potential_components[i+1] == ':' and 
                        potential_components[i+2].isdigit() and 
                        len(potential_components[i+2]) <= 2):
                        hours = potential_components[i].zfill(2)
                        minutes = potential_components[i+2].zfill(2)
                        time_value = f"Time: {hours}:{minutes}"
                        break
        
        if time_value:
            print(f"extract_texts: Time value: {time_value}")
            if callable(return_time_value):
                return_time_value(time_value)
            
            success_msg = f"Time value extracted: {time_value}"
            update_author_status('pending', success_msg)
        else:
            print("extract_texts: Time components not found or incomplete.")
            update_author_status('pending', f"Time components not found")

        if additional_texts:
            if found_texts:
                print(f"extract_texts: Found additional texts: {found_texts}")
            else:
                print("extract_texts: No additional texts found")
        else:
            print("extract_texts: No additional texts provided for checking.")

        return extractedtexts, time_value, found_texts
        
    except Exception as e:
        error_msg = f"ERROR - {str(e)}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return [], None, []

def toggleschedule():
    """
    Toggle the 'Set date and time' button or checkbox for scheduling a post.
    - Random delay: 1.0 to 3.0 seconds before click (human-like)
    - State tracker prevents redundant clicks
    - Multiple robust locators with fallback
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses AUTHOR_PATH global constant
    """
    import os
    import json
    import random
    import time
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH is already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"toggleschedule: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"toggleschedule: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"toggleschedule: SKIPPED - Status is 'aborted'. No action taken.")
        return

    print(f"toggleschedule: Starting schedule toggle")
    update_author_status('pending', f"Starting schedule toggle")

    try:
        # Initialize tracker if not already set
        if not hasattr(toggleschedule, 'is_toggled'):
            toggleschedule.is_toggled = False

        # Skip if already toggled
        if toggleschedule.is_toggled:
            print("toggleschedule: Schedule toggle already activated. Skipping click operation.")
            return

        print("toggleschedule: Locating 'Set date and time' toggle...")
        
        # Primary locator
        scheduling_toggle = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'set date and time')]//input[@type='checkbox'] | "
                "//div[contains(@aria-label, 'Set date and time') or contains(text(), 'Set date and time')]//following-sibling::div[@role='switch'] | "
                "//span[contains(text(), 'Set date and time')]/following::input[1]"
            ))
        )

        # === RANDOM HUMAN-LIKE DELAY BEFORE CLICK ===
        delay = random.uniform(1.0, 3.0)
        print(f"toggleschedule: Waiting {delay:.2f} seconds before toggling schedule...")
        time.sleep(delay)

        # Handle checkbox or switch
        if scheduling_toggle.tag_name == 'input' and scheduling_toggle.get_attribute('type') == 'checkbox':
            if not scheduling_toggle.is_selected():
                scheduling_toggle.click()
                print("toggleschedule: Toggled 'Set date and time' checkbox ON.")
            else:
                print("toggleschedule: 'Set date and time' checkbox already enabled.")
        else:
            scheduling_toggle.click()
            print("toggleschedule: Clicked 'Set date and time' toggle switch.")

        # Mark as toggled
        toggleschedule.is_toggled = True
        print("toggleschedule: Tracker updated: is_toggled = True")
        
        success_msg = "Schedule toggled successfully"
        update_author_status('pending', success_msg)

        time.sleep(2)

    except Exception as e:
        error_msg = f"Primary locator failed: {str(e)}"
        print(f"toggleschedule: {error_msg}")
        
        try:
            print("toggleschedule: Trying alternative locator...")
             
            # === ALTERNATIVE LOCATOR ===
            scheduling_toggle = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "[aria-label*='Schedule'] input[type='checkbox'], [data-testid*='schedule-toggle']"
                ))
            )

            # === RANDOM DELAY AGAIN (fallback path) ===
            delay = random.uniform(1.0, 3.0)
            print(f"toggleschedule: Waiting {delay:.2f} seconds before fallback click...")
            time.sleep(delay)

            if scheduling_toggle.tag_name == 'input' and scheduling_toggle.get_attribute('type') == 'checkbox':
                if not scheduling_toggle.is_selected():
                    scheduling_toggle.click()
                    print("toggleschedule: Toggled 'Set date and time' via alternative checkbox.")
                else:
                    print("toggleschedule: 'Set date and time' already enabled (alternative).")
            else:
                scheduling_toggle.click()
                print("toggleschedule: Clicked toggle via alternative locator.")

            # Update tracker
            toggleschedule.is_toggled = True
            print("toggleschedule: Tracker updated: is_toggled = True (fallback)")
            
            success_msg = "Schedule toggled successfully (fallback)"
            update_author_status('pending', success_msg)

            time.sleep(2)

        except Exception as e2:
            error_msg2 = f"Alternative locator also failed: {str(e2)}"
            print(f"toggleschedule: {error_msg2}")
            update_author_status('aborted', error_msg2)
            raise Exception(f"toggleschedule: Could not locate or toggle 'Set date and time' button")
                  
def set_webschedule():
    """
    Set web schedule using 6 input sequences in STRICT ORDER.
    Forces full 6-round cycle before any repeat.
    NEVER repeats last used.
    Records ONLY its own state in AUTHOR_PATH under 'setwebschedule_input'.
    MAXIMUM SPEED - ALL WAITS REMOVED
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Uses AUTHOR_PATH and FILES_ROOT global constants
    """
    import os
    import json
    import re
    import time
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"set_webschedule: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"set_webschedule: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"set_webschedule: SKIPPED - Status is 'aborted'. No action taken.")
        return

    print(f"set_webschedule: Starting web schedule set")
    update_author_status('pending', f"Starting web schedule set")

    # --- 1. Read AUTHOR_PATH ---
    print(f"[{time.strftime('%H:%M:%S')}] Reading AUTHOR_PATH")
    try:
        author_data = load_json_file(AUTHOR_PATH, {})
        
        # Handle both list and dict formats
        if isinstance(author_data, list) and len(author_data) > 0:
            config = author_data[-1]
        elif isinstance(author_data, dict):
            config = author_data
        else:
            error_msg = "Invalid config format in AUTHOR_PATH"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        author = config.get('author', '')
        type_value = config.get('type', '')
        
        if not author or not type_value:
            error_msg = "Missing author or type in config"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
            
        print(f"set_webschedule: Author: {author} | Type: {type_value}")
    except Exception as e:
        error_msg = f"ERROR reading AUTHOR_PATH: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # --- 2. Build schedules.json path using FILES_ROOT ---
    schedules_path = os.path.join(FILES_ROOT, "next jpg", author, "jsons", f"{type_value}_schedules.json")
    print(f"set_webschedule: Reading schedule from: {schedules_path}")

    try:
        with open(schedules_path, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        error_msg = f"{type_value}_schedules.json not found at: {schedules_path}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    except json.JSONDecodeError:
        error_msg = "Invalid JSON in schedules.json"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # --- 3. Extract next_schedule ---
    next_schedule_list = json_data.get('next_schedule')
    if not next_schedule_list or len(next_schedule_list) == 0:
        error_msg = "No next_schedule found in schedules.json"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    next_schedule = next_schedule_list[0]
    target_date = next_schedule.get('date')
    target_time_12h = next_schedule.get('time_12hour')
    target_time_24h = next_schedule.get('time_24hour')

    if not all([target_date, target_time_12h, target_time_24h]):
        error_msg = f"Missing schedule data: {next_schedule}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    target_time_12h = target_time_12h.strip().lower()
    target_time_24h = target_time_24h.strip()

    print(f"set_webschedule: Target → Date: {target_date} | Time: {target_time_12h.upper()} ({target_time_24h})")

    # --- 4. Parse times ---
    match_12h = re.match(r"(\d{1,2}):(\d{2})\s*(am|pm)", target_time_12h, re.IGNORECASE)
    match_24h = re.match(r"(\d{1,2}):(\d{2})", target_time_24h)
    if not match_12h or not match_24h:
        error_msg = f"Invalid time format: {target_time_12h} / {target_time_24h}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    hour_12h, minute_12h, period = match_12h.groups()
    period = period.upper()
    hour_24h, minute_24h = match_24h.groups()

    # --- 5. ROBUST DATE PARSING WITH MULTIPLE FORMATS ---
    def parse_date_to_parts(date_str):
        """Parse date string to (day, month, year) regardless of format"""
        if not date_str:
            return None, None, None
        
        date_str = date_str.strip()
        
        formats = [
            (r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})', 'day month_name year'),
            (r'(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{4})', 'day month_abbr year'),
            (r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2}),?\s+(\d{4})', 'month_name day year'),
            (r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2}),?\s+(\d{4})', 'month_abbr day year'),
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', 'd/m/y'),
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', 'm/d/y'),
            (r'(\d{1,2})-(\d{1,2})-(\d{4})', 'd-m-y'),
            (r'(\d{1,2})-(\d{1,2})-(\d{4})', 'm-d-y'),
            (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', 'd.m.y'),
            (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', 'm.d.y'),
            (r'(\d{4})/(\d{1,2})/(\d{1,2})', 'y/m/d'),
            (r'(\d{4})-(\d{1,2})-(\d{1,2})', 'y-m-d'),
            (r'(\d{4})\.(\d{1,2})\.(\d{1,2})', 'y.m.d'),
        ]
        
        month_map = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12',
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        
        for pattern, format_type in formats:
            match = re.search(pattern, date_str, re.IGNORECASE)
            if match:
                groups = match.groups()
                
                if format_type == 'day month_name year' or format_type == 'day month_abbr year':
                    day = groups[0].zfill(2)
                    month = month_map.get(groups[1].lower())
                    year = groups[2]
                    if month:
                        return day, month, year
                
                elif format_type == 'month_name day year' or format_type == 'month_abbr day year':
                    month = month_map.get(groups[0].lower())
                    day = groups[1].zfill(2)
                    year = groups[2]
                    if month:
                        return day, month, year
                
                elif format_type == 'd/m/y' or format_type == 'd-m-y' or format_type == 'd.m.y':
                    day = groups[0].zfill(2)
                    month = groups[1].zfill(2)
                    year = groups[2]
                    if 1 <= int(day) <= 31 and 1 <= int(month) <= 12:
                        return day, month, year
                
                elif format_type == 'm/d/y' or format_type == 'm-d-y' or format_type == 'm.d.y':
                    month = groups[0].zfill(2)
                    day = groups[1].zfill(2)
                    year = groups[2]
                    if 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
                        return day, month, year
                
                elif format_type == 'y/m/d' or format_type == 'y-m-d' or format_type == 'y.m.d':
                    year = groups[0]
                    month = groups[1].zfill(2)
                    day = groups[2].zfill(2)
                    if 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
                        return day, month, year
        
        numbers = re.findall(r'\d+', date_str)
        if len(numbers) >= 3:
            year = None
            day = None
            month = None
            
            for num in numbers:
                if len(num) == 4 and 1900 <= int(num) <= 2099:
                    year = num
                    break
            
            if not year:
                for num in numbers:
                    if len(num) == 2:
                        year = f"20{num}" if int(num) < 30 else f"19{num}"
                        break
            
            numbers_without_year = [n for n in numbers if n != year and n != year[-2:]] if year else numbers[:]
            
            if len(numbers_without_year) >= 2:
                num1, num2 = int(numbers_without_year[0]), int(numbers_without_year[1])
                
                if num1 > 12 and num2 <= 12:
                    day, month = numbers_without_year[0].zfill(2), numbers_without_year[1].zfill(2)
                elif num2 > 12 and num1 <= 12:
                    day, month = numbers_without_year[1].zfill(2), numbers_without_year[0].zfill(2)
                else:
                    day, month = numbers_without_year[0].zfill(2), numbers_without_year[1].zfill(2)
                
                if not year:
                    year = "2026"
                
                if day and month and year:
                    return day, month, year
        
        return None, None, None

    # --- 6. NORMALIZE DATE FOR COMPARISON ---
    def normalize_date_for_comparison(date_str):
        """Normalize any date format to a standard string for comparison"""
        day, month, year = parse_date_to_parts(date_str)
        if all([day, month, year]):
            return f"{year}-{month}-{day}"
        return date_str

    # --- 7. DETECT DATE FORMAT FROM INPUT ELEMENT ---
    def detect_date_format_from_element(date_input_element):
        """Detect the date format by reading the current value"""
        current_value = driver.execute_script("return arguments[0].value", date_input_element) or ""
        if not current_value:
            return None
        
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
        month_abbr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        
        current_lower = current_value.lower()
        
        for name in month_names + month_abbr:
            if name in current_lower:
                numbers = re.findall(r'\d+', current_value)
                if len(numbers) >= 2:
                    month_pos = current_lower.find(name)
                    day_pos = current_value.find(numbers[0]) if len(numbers) > 0 else -1
                    
                    if month_pos < day_pos:
                        return "MM/DD/YYYY"
                    else:
                        return "DD/MM/YYYY"
                break
        
        if '/' in current_value:
            separator = '/'
        elif '-' in current_value:
            separator = '-'
        elif '.' in current_value:
            separator = '.'
        else:
            separator = None
        
        if separator:
            parts = current_value.split(separator)
            if len(parts) == 3:
                try:
                    first = int(parts[0])
                    second = int(parts[1])
                    
                    if 1 <= first <= 12 and 1 <= second <= 31:
                        return "MM/DD/YYYY"
                    elif 1 <= first <= 31 and 1 <= second <= 12:
                        return "DD/MM/YYYY"
                except:
                    pass
        
        return "DD/MM/YYYY"

    # --- 8. Wait for Schedule Panel (MINIMAL WAIT) ---
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'schedule')]")
            )
        )
        print("set_webschedule: Schedule panel loaded.")
    except TimeoutException:
        error_msg = "Schedule panel not found!"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # --- 9. Locate Inputs ---
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"set_webschedule: Found {len(inputs)} input fields.")

    date_input = hour_input = minute_input = am_pm_input = None
    for inp in inputs:
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
        if all([date_input, hour_input, minute_input]):
            break

    if not all([date_input, hour_input, minute_input]):
        error_msg = "Missing required inputs (date, hour, minute)!"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    is_24h_format = am_pm_input is None
    print(f"set_webschedule: Time format: {'24-hour' if is_24h_format else '12-hour'}")

    # --- 10. DETECT THE ACTUAL DATE FORMAT ---
    detected_format = detect_date_format_from_element(date_input)
    print(f"set_webschedule: Detected format: {detected_format}")
    
    if not detected_format:
        date_placeholder = date_input.get_attribute("placeholder") or ""
        if "mm/dd" in date_placeholder.lower() or "m/d" in date_placeholder.lower():
            detected_format = "MM/DD/YYYY"
        elif "dd/mm" in date_placeholder.lower() or "d/m" in date_placeholder.lower():
            detected_format = "DD/MM/YYYY"
        else:
            detected_format = "DD/MM/YYYY"
        print(f"set_webschedule: Using placeholder format: {detected_format}")

    # --- 11. Parse target date ---
    target_day, target_month, target_year = parse_date_to_parts(target_date)
    if not all([target_day, target_month, target_year]):
        error_msg = f"Could not parse target date: {target_date}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    print(f"set_webschedule: Target date parts → Day: {target_day}, Month: {target_month}, Year: {target_year}")

    # --- 12. FORMAT THE DATE ---
    def format_date_for_input(day, month, year, format_type):
        """Format date parts according to the specified format"""
        if format_type == "MM/DD/YYYY":
            return f"{month}/{day}/{year}"
        elif format_type == "DD/MM/YYYY":
            return f"{day}/{month}/{year}"
        elif format_type == "YYYY/MM/DD":
            return f"{year}/{month}/{day}"
        elif format_type == "MM-DD-YYYY":
            return f"{month}-{day}-{year}"
        elif format_type == "DD-MM-YYYY":
            return f"{day}-{month}-{year}"
        elif format_type == "YYYY-MM-DD":
            return f"{year}-{month}-{day}"
        elif format_type == "MM.DD.YYYY":
            return f"{month}.{day}.{year}"
        elif format_type == "DD.MM.YYYY":
            return f"{day}.{month}.{year}"
        elif format_type == "YYYY.MM.DD":
            return f"{year}.{month}.{day}"
        else:
            return f"{day}/{month}/{year}"
    
    date_to_send = format_date_for_input(target_day, target_month, target_year, detected_format)
    print(f"set_webschedule: Formatted date for input: {date_to_send}")

    # --- 13. Check if already correct ---
    current_date = (driver.execute_script("return arguments[0].value", date_input) or "").strip()
    _, extracted_time, _ = extract_texts() or ("", "", [])

    normalized_current = normalize_date_for_comparison(current_date)
    normalized_target = normalize_date_for_comparison(target_date)
    date_matches = (normalized_current == normalized_target)
    
    time_matches = False
    if is_24h_format:
        expected = f"Time: {hour_24h.zfill(2)}:{minute_24h}"
        time_matches = extracted_time == expected
    else:
        exp1 = f"Time: {int(hour_12h):d}:{minute_12h}"
        exp2 = f"Time: {hour_12h.zfill(2)}:{minute_12h}"
        time_matches = extracted_time in [exp1, exp2]

    if date_matches and time_matches:
        print("set_webschedule: Schedule already correct. Skipping.")
        update_author_status('pending', f"Schedule already correct - skipping")
        return

    # --- 14. SEQUENCE DEFINITIONS ---
    sequences = {
        "hh_date_mm": [
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("date", date_input, date_to_send),
            ("minute", minute_input, minute_24h),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None
        ],
        "hh_mm_date": [
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("minute", minute_input, minute_24h),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None,
            ("date", date_input, date_to_send)
        ],
        "mm_hh_date": [
            ("minute", minute_input, minute_24h),
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None,
            ("date", date_input, date_to_send)
        ],
        "mm_date_hh": [
            ("minute", minute_input, minute_24h),
            ("date", date_input, date_to_send),
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None
        ],
        "date_hh_mm": [
            ("date", date_input, date_to_send),
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("minute", minute_input, minute_24h),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None
        ],
        "date_mm_hh": [
            ("date", date_input, date_to_send),
            ("minute", minute_input, minute_24h),
            ("hour", hour_input, hour_24h.zfill(2) if is_24h_format else (hour_12h.lstrip('0') or '12')),
            ("period", am_pm_input, period) if not is_24h_format and am_pm_input else None
        ]
    }

    # --- 15. FIXED ORDER ---
    order = [
        "hh_date_mm",
        "hh_mm_date",
        "mm_hh_date",
        "mm_date_hh",
        "date_hh_mm",
        "date_mm_hh"
    ]

    # --- 16. LOAD STATE FROM AUTHOR_PATH (setwebschedule_input) ---
    config = author_data[-1] if author_data and isinstance(author_data[-1], dict) else {}
    state_data = config.get('setwebschedule_input', {})
    
    if state_data:
        print(f"set_webschedule: Loaded state from AUTHOR_PATH: {state_data}")
    else:
        print("set_webschedule: No state found in AUTHOR_PATH. Will create new.")

    used_sequences = state_data.get("used_sequences", [])
    used_sequences = [s for s in used_sequences if s in order]
    last_used = state_data.get("last_used")
    if last_used not in order:
        last_used = None

    print(f"set_webschedule: Used so far: {len(used_sequences)}/6 → {used_sequences}")
    print(f"set_webschedule: Last used: {last_used}")

    # --- 17. PICK NEXT IN STRICT 6-CYCLE ---
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
    print(f"set_webschedule: USING #{used_sequences.count(next_seq_key) + 1 if next_seq_key in used_sequences else 1}: {next_seq_key} → {seq_names}")

    # --- 18. EXECUTE SEQUENCE (NO WAITS) ---
    for field_name, element, value in chosen_seq:
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()

            if field_name == "date":
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                ActionChains(driver).send_keys(value).perform()
            elif field_name == "period":
                ActionChains(driver).send_keys(value).send_keys(Keys.ENTER).perform()
            else:
                element.clear()
                element.send_keys(value)

            element.send_keys(Keys.TAB)
        except Exception as e:
            if "intercepted" in str(e).lower():
                print("set_webschedule: Click intercepted. Reloading...")
                reset_trackers()
                driver.refresh()
                raise
            else:
                error_msg = f"Error on {field_name}: {e}"
                print(error_msg)
                update_author_status('aborted', error_msg)
                raise

    # --- 19. UPDATE used_sequences (rotate) ---
    if next_seq_key not in used_sequences:
        used_sequences.append(next_seq_key)
    else:
        used_sequences.remove(next_seq_key)
        used_sequences.append(next_seq_key)
    used_sequences = used_sequences[-6:]

    # --- 20. FINAL VERIFICATION ---
    final_date = (driver.execute_script("return arguments[0].value", date_input) or "").strip()
    _, final_time, _ = extract_texts() or ("", "", [])

    normalized_final = normalize_date_for_comparison(final_date)
    normalized_target_final = normalize_date_for_comparison(target_date)
    date_matches = (normalized_final == normalized_target_final)
    
    if not date_matches:
        actual_format = detect_date_format_from_element(date_input)
        if actual_format and actual_format != detected_format:
            date_to_send = format_date_for_input(target_day, target_month, target_year, actual_format)
            print(f"set_webschedule: Retrying with format: {date_to_send}")
            
            try:
                date_input.click()
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                ActionChains(driver).send_keys(date_to_send).perform()
                date_input.send_keys(Keys.TAB)
                
                final_date = (driver.execute_script("return arguments[0].value", date_input) or "").strip()
                normalized_final = normalize_date_for_comparison(final_date)
                date_matches = (normalized_final == normalized_target_final)
            except Exception as e:
                print(f"set_webschedule: Retry failed: {e}")
        
        if not date_matches:
            error_msg = f"Date not set correctly. Expected: '{target_date}' | Got: '{final_date}'"
            print(error_msg)
            update_author_status('aborted', error_msg)
            raise Exception(error_msg)
    
    # Verify time
    if is_24h_format:
        if final_time != f"Time: {hour_24h.zfill(2)}:{minute_24h}":
            error_msg = f"Time not set correctly. Expected: 'Time: {hour_24h.zfill(2)}:{minute_24h}' | Got: '{final_time}'"
            print(error_msg)
            update_author_status('aborted', error_msg)
            raise Exception(error_msg)
    else:
        exp = [f"Time: {int(hour_12h):d}:{minute_12h}", f"Time: {hour_12h.zfill(2)}:{minute_12h}"]
        if final_time not in exp:
            error_msg = f"Time not set correctly. Expected: '{exp}' | Got: '{final_time}'"
            print(error_msg)
            update_author_status('aborted', error_msg)
            raise Exception(error_msg)

    print(f"set_webschedule: SCHEDULE SET: {target_date} @ {target_time_12h.upper()} via {seq_names}")

    # --- 21. Handle Overlay ---
    overlays = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay')]")
    if overlays:
        print("set_webschedule: Overlay detected. Reloading...")
        reset_trackers()
        driver.refresh()
        update_author_status('pending', f"Overlay detected - reloading")
        raise Exception("Overlay after set")

    # --- 22. SAVE STATE TO AUTHOR_PATH (setwebschedule_input) ---
    state_data = {
        "used_sequences": used_sequences,
        "last_used": next_seq_key,
        "last_updated": time.strftime('%Y-%m-%d %H:%M:%S'),
        "last_schedule_date": target_date,
        "last_schedule_time": target_time_12h
    }

    # Save to AUTHOR_PATH
    author_data = load_json_file(AUTHOR_PATH, [])
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            author_data[-1]['setwebschedule_input'] = state_data
            if save_json_file(AUTHOR_PATH, author_data):
                print(f"set_webschedule: SAVED state to AUTHOR_PATH: {state_data}")
            else:
                print("set_webschedule: ERROR saving state to AUTHOR_PATH")

    success_msg = f"Schedule set successfully for {target_date} @ {target_time_12h}"
    print(f"set_webschedule: {success_msg}")
    update_author_status('pending', success_msg)
    
    # --- 23. Click the publish/update/schedule button (IMMEDIATE) ---
    button_xpaths = [
        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'schedule')]",
        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'publish')]",
        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'update')]",
        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')]",
        "//input[@type='submit']",
    ]
    
    button_clicked = False
    for xpath in button_xpaths:
        try:
            button = driver.find_element(By.XPATH, xpath)
            if button.is_enabled() and button.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                button.click()
                print(f"set_webschedule: Clicked button: {xpath}")
                button_clicked = True
                break
        except:
            continue
    
    if not button_clicked:
        print("set_webschedule: No publish/schedule button found to click.")
    
    print("set_webschedule: set_webschedule() completed successfully.\n")
    return True

def cleanup_processed_image():
    """
    Checks filename.json in next jpg folder and deletes the referenced file
    from both next jpg and downloaded folders.
    
    - Reads filename.json to get original filename
    - Deletes the processed file from next jpg folder
    - Deletes the original source file from downloaded folder
    - Removes or archives filename.json after cleanup
    
    UPDATES operation_status and status in AUTHOR_PATH
    ONLY executes if status is 'pending'
    Sets status to 'aborted' if critical errors occur
    """
    import os
    import json
    import shutil
    from datetime import datetime
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        return default if default is not None else {}
                    return json.loads(content)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"cleanup_processed_image: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"cleanup_processed_image: {operation_message}"
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = f"cleanup_processed_image: {operation_message}"
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = f"cleanup_processed_image: {operation_message}"
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "cleanup_processed_image: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status == 'aborted':
            print(f"cleanup_processed_image: SKIPPED - Status is 'aborted'. No action taken.")
            return
        
        if current_status != 'pending':
            print(f"cleanup_processed_image: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"cleanup_processed_image: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"cleanup_processed_image: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD AUTHOR FROM CONFIG
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "cleanup_processed_image: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"cleanup_processed_image: Author: {author}")
        
    except Exception as e:
        error_msg = f"cleanup_processed_image: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 3: SETUP DIRECTORIES USING FILES_ROOT
    # ============================================================
    next_jpg_dir = os.path.join(FILES_ROOT, "next jpg", author)
    downloaded_dir = os.path.join(FILES_ROOT, "downloaded", author)
    
    print(f"cleanup_processed_image: Next JPG directory: {next_jpg_dir}")
    print(f"cleanup_processed_image: Downloaded directory: {downloaded_dir}")
    
    # ============================================================
    # STEP 4: CHECK IF filename.json EXISTS
    # ============================================================
    filename_json_path = os.path.join(next_jpg_dir, "filename.json")
    
    if not os.path.exists(filename_json_path):
        warning_msg = f"filename.json not found in {next_jpg_dir}. Nothing to clean up."
        print(warning_msg)
        update_author_status('pending', warning_msg)
        return
    
    # ============================================================
    # STEP 5: READ filename.json
    # ============================================================
    try:
        with open(filename_json_path, 'r', encoding='utf-8') as f:
            filename_data = json.load(f)
        
        print(f"cleanup_processed_image: Loaded filename.json: {filename_data}")
        
        original_filename = filename_data.get('original_filename')
        original_source = filename_data.get('original_source')
        action = filename_data.get('action', 'unknown')
        timestamp = filename_data.get('timestamp', 'unknown')
        
        if not original_filename and not original_source:
            error_msg = "filename.json does not contain original_filename or original_source"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"cleanup_processed_image: Original filename: {original_filename}")
        print(f"cleanup_processed_image: Original source: {original_source}")
        print(f"cleanup_processed_image: Action: {action}")
        print(f"cleanup_processed_image: Timestamp: {timestamp}")
        
    except Exception as e:
        error_msg = f"cleanup_processed_image: ERROR - Failed to read filename.json: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return
    
    # ============================================================
    # STEP 6: DELETE FILES
    # ============================================================
    deleted_files = []
    failed_deletions = []
    
    # 6a. Delete card_x.jpg from next jpg folder
    card_x_path = os.path.join(next_jpg_dir, "card_x.jpg")
    if os.path.exists(card_x_path):
        try:
            os.remove(card_x_path)
            print(f"cleanup_processed_image: Deleted card_x.jpg from next jpg")
            deleted_files.append("card_x.jpg")
        except Exception as e:
            error_msg = f"Failed to delete card_x.jpg: {e}"
            print(f"cleanup_processed_image: {error_msg}")
            failed_deletions.append(("card_x.jpg", error_msg))
    else:
        print(f"cleanup_processed_image: card_x.jpg not found (already deleted)")
    
    # 6b. Delete the processed file from next jpg folder (original_filename)
    if original_filename:
        processed_file_path = os.path.join(next_jpg_dir, original_filename)
        if os.path.exists(processed_file_path):
            try:
                os.remove(processed_file_path)
                print(f"cleanup_processed_image: Deleted {original_filename} from next jpg")
                deleted_files.append(original_filename)
            except Exception as e:
                error_msg = f"Failed to delete {original_filename}: {e}"
                print(f"cleanup_processed_image: {error_msg}")
                failed_deletions.append((original_filename, error_msg))
        else:
            print(f"cleanup_processed_image: {original_filename} not found in next jpg (already deleted)")
    
    # 6c. Delete the source file from downloaded folder (original_source)
    if original_source:
        source_file_path = os.path.join(downloaded_dir, original_source)
        if os.path.exists(source_file_path):
            try:
                os.remove(source_file_path)
                print(f"cleanup_processed_image: Deleted {original_source} from downloaded")
                deleted_files.append(original_source)
            except Exception as e:
                error_msg = f"Failed to delete {original_source}: {e}"
                print(f"cleanup_processed_image: {error_msg}")
                failed_deletions.append((original_source, error_msg))
        else:
            print(f"cleanup_processed_image: {original_source} not found in downloaded (already deleted)")
    
    # ============================================================
    # STEP 7: HANDLE filename.json (ARCHIVE OR DELETE)
    # ============================================================
    # Create archive directory if it doesn't exist
    archive_dir = os.path.join(FILES_ROOT, "next jpg", author, "archive")
    try:
        os.makedirs(archive_dir, exist_ok=True)
        
        # Archive filename.json with timestamp
        archive_name = f"filename_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        archive_path = os.path.join(archive_dir, archive_name)
        
        # Move filename.json to archive
        shutil.move(filename_json_path, archive_path)
        print(f"cleanup_processed_image: Archived filename.json → {archive_path}")
        
    except Exception as e:
        # If archive fails, try to delete filename.json
        try:
            os.remove(filename_json_path)
            print(f"cleanup_processed_image: Deleted filename.json (archive failed)")
        except Exception as del_e:
            error_msg = f"Failed to archive or delete filename.json: {del_e}"
            print(f"cleanup_processed_image: ERROR - {error_msg}")
            failed_deletions.append(("filename.json", error_msg))
    
    # ============================================================
    # STEP 8: CHECK RESULTS AND UPDATE STATUS
    # ============================================================
    print(f"\ncleanup_processed_image: CLEANUP SUMMARY")
    print(f"{'='*60}")
    print(f"Author: {author}")
    print(f"Action performed: {action}")
    print(f"Original timestamp: {timestamp}")
    print(f"Files deleted: {len(deleted_files)}")
    for f in deleted_files:
        print(f"  • {f}")
    
    if failed_deletions:
        print(f"Failed deletions: {len(failed_deletions)}")
        for f, err in failed_deletions:
            print(f"  • {f}: {err}")
    
    print(f"{'='*60}")
    
    if failed_deletions:
        # Some files failed to delete - log warning but don't abort
        status_value = 'pending'
        operation_msg = (
            f"Partial cleanup completed. {len(deleted_files)} files deleted, "
            f"{len(failed_deletions)} failed. Check logs for details."
        )
        update_author_status(status_value, operation_msg)
        print(f"\n⚠️ Status updated to 'pending' - Partial cleanup with warnings")
        return False
    else:
        # All files deleted successfully
        status_value = 'pending'
        operation_msg = f"Successfully cleaned up {len(deleted_files)} files for author '{author}'"
        update_author_status(status_value, operation_msg)
        print(f"\n✅ Status updated to 'pending' - Cleanup completed successfully")
        return True
    
def schedule_and_upload():
    """
    Click the schedule/upload post button and confirm success.
    
    UPDATES operation_status and status in AUTHOR_PATH
    Skips execution if status is 'aborted'
    Sets status to 'completed' on success, 'aborted' on failure
    Calls cleanup_processed_image() on successful scheduling
    Uses AUTHOR_PATH global constant
    """
    import os
    import json
    import time
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH is already defined globally
    
    def load_json_file(file_path, default=None):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, [])
            if not isinstance(author_data, list):
                author_data = []
            
            if author_data:
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"click_upload_post_button: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"click_upload_post_button: {operation_message}"
                    
                    if save_json_file(AUTHOR_PATH, author_data):
                        return True
            return False
        except:
            return False

    # ===== CHECK STATUS - Skip if 'aborted' =====
    author_data = load_json_file(AUTHOR_PATH, [])
    current_status = 'pending'
    
    if author_data and isinstance(author_data, list) and len(author_data) > 0:
        if isinstance(author_data[-1], dict):
            current_status = author_data[-1].get('status', 'pending')
            if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                dyn_status = author_data[-1]['dynamic_values'].get('status', 'pending')
                if dyn_status:
                    current_status = dyn_status
    
    if current_status == 'aborted':
        print(f"click_upload_post_button: SKIPPED - Status is 'aborted'. No action taken.")
        return

    print(f"click_upload_post_button: Starting upload/schedule button click")
    update_author_status('pending', f"Starting upload/schedule button click")

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
        print("click_upload_post_button: SCHEDULED SUCCESSFULLY!")
        
        update_author_status('pending', f"Button clicked successfully")

        # Confirm
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(), 'scheduled')]")
            )
        )
        print("click_upload_post_button: Success message confirmed.")
        
        # ===== SUCCESS - Set status to 'completed' =====
        success_msg = "Post scheduled successfully! Operation completed."
        update_author_status('completed', success_msg)
        print(f"click_upload_post_button: ✅ Status updated to 'completed'")
        
        # Call uploadedjpgs
        print("click_upload_post_button: executed uploaded jpgs")
        
        # ===== CALL CLEANUP AFTER SUCCESSFUL SCHEDULING =====
        try:
            print("click_upload_post_button: Running cleanup_processed_image()...")
            cleanup_result = cleanup_processed_image()
            if cleanup_result:
                print("click_upload_post_button: ✅ Cleanup completed successfully")
            else:
                print("click_upload_post_button: ⚠️ Cleanup completed with warnings")
        except Exception as cleanup_e:
            print(f"click_upload_post_button: ⚠️ Cleanup failed: {cleanup_e}")
            # Don't raise - cleanup failure shouldn't stop the process

        # Reload page to start a new process
        print("click_upload_post_button: Reloading page to start a new scheduling process...")
        reset_trackers()
        driver.refresh()
        time.sleep(2)

    except Exception as e:
        error_str = str(e).lower()
        
        if "element click intercepted" in error_str:
            error_msg = "Element click intercepted - reloading page and resetting trackers"
            print(f"click_upload_post_button: {error_msg}")
            reset_trackers()
            driver.refresh()
            update_author_status('aborted', error_msg)
            raise Exception(f"click_upload_post_button: Page reloaded due to click interception")
        
        # Check for overlay
        overlay = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'overlay') or @role='dialog']")
        if overlay:
            error_msg = "Detected overlay blocking interaction - reloading page"
            print(f"click_upload_post_button: {error_msg}")
            reset_trackers()
            driver.refresh()
            update_author_status('aborted', error_msg)
            raise Exception(f"click_upload_post_button: Page reloaded due to overlay")
        
        error_msg = f"Failed to schedule: {str(e)}"
        print(f"click_upload_post_button: {error_msg}")
        update_author_status('aborted', error_msg)
        raise

def move_downloaded_urls_to_uploadedjpgsurl():
    """
    Moves downloaded image URLs from downloaded_images_url to uploaded_jpgs_url.
    
    - Reads downloaded_images_url from AUTHOR_PATH
    - Appends all downloaded URLs to uploaded_jpgs_url
    - Clears downloaded_images_url after successful transfer
    - Updates operation_status and status in AUTHOR_PATH
    
    ONLY executes if status is 'pending'
    Sets status to 'aborted' only on fatal/critical errors
    """
    import os
    import json
    from datetime import datetime
    import pytz
    
    # ===== USE GLOBAL CONFIGURATION =====
    # AUTHOR_PATH, FILES_ROOT are already defined globally
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        return default if default is not None else {}
                    return json.loads(content)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    def save_json_file(file_path, data):
        """Save JSON file with proper formatting"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def update_author_status(status_value, operation_message):
        """Update status and operation_status in AUTHOR_PATH"""
        try:
            author_data = load_json_file(AUTHOR_PATH, {})
            
            is_list = isinstance(author_data, list)
            
            if is_list:
                if not author_data:
                    author_data = [{}]
                
                if isinstance(author_data[-1], dict):
                    author_data[-1]['status'] = status_value
                    author_data[-1]['operation_status'] = f"record_downloaded_to_uploadedjpgs: {operation_message}"
                    
                    if 'dynamic_values' in author_data[-1] and isinstance(author_data[-1]['dynamic_values'], dict):
                        author_data[-1]['dynamic_values']['status'] = status_value
                        author_data[-1]['dynamic_values']['operation_status'] = f"record_downloaded_to_uploadedjpgs: {operation_message}"
            else:
                if not isinstance(author_data, dict):
                    author_data = {}
                
                author_data['status'] = status_value
                author_data['operation_status'] = f"record_downloaded_to_uploadedjpgs: {operation_message}"
                
                if 'dynamic_values' in author_data and isinstance(author_data['dynamic_values'], dict):
                    author_data['dynamic_values']['status'] = status_value
                    author_data['dynamic_values']['operation_status'] = f"record_downloaded_to_uploadedjpgs: {operation_message}"
            
            if save_json_file(AUTHOR_PATH, author_data):
                return True
            return False
        except Exception as e:
            print(f"Failed to update author status: {e}")
            return False
    
    def get_uploaded_jpgs_url_from_config(config):
        """Extract uploaded_jpgs_url from config"""
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            return config['dynamic_values'].get('uploaded_jpgs_url', [])
        return config.get('uploaded_jpgs_url', [])
    
    def set_uploaded_jpgs_url_in_config(config, value):
        """Set uploaded_jpgs_url in config"""
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            config['dynamic_values']['uploaded_jpgs_url'] = value
        else:
            config['uploaded_jpgs_url'] = value
        return config

    # ============================================================
    # STEP 1: CHECK STATUS - ONLY execute if 'pending'
    # ============================================================
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
            config_is_list = True
        elif isinstance(config_data, dict):
            config = config_data
            config_is_list = False
        else:
            error_msg = "record_downloaded_to_uploadedjpgs: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        current_status = config.get('status', 'pending')
        
        if 'dynamic_values' in config and isinstance(config['dynamic_values'], dict):
            dyn_status = config['dynamic_values'].get('status', 'pending')
            if dyn_status:
                current_status = dyn_status
        
        if current_status == 'aborted':
            print(f"record_downloaded_to_uploadedjpgs: SKIPPED - Status is 'aborted'. No action taken.")
            return
        
        if current_status != 'pending':
            print(f"record_downloaded_to_uploadedjpgs: SKIPPED - Status is '{current_status}'. Function only executes when status is 'pending'.")
            return
        
        print(f"record_downloaded_to_uploadedjpgs: Status is 'pending' - proceeding...")
        
    except Exception as e:
        error_msg = f"record_downloaded_to_uploadedjpgs: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 2: LOAD AUTHOR FROM CONFIG
    # ============================================================
    try:
        author = config.get('author', '').strip()
        if not author:
            error_msg = "record_downloaded_to_uploadedjpgs: ERROR - 'author' is missing or empty in config."
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
        print(f"record_downloaded_to_uploadedjpgs: Author: {author}")
        
    except Exception as e:
        error_msg = f"record_downloaded_to_uploadedjpgs: ERROR - Failed to process config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 3: GET DOWNLOADED URLs
    # ============================================================
    downloaded_urls = config.get('downloaded_images_url', [])
    
    if not isinstance(downloaded_urls, list):
        downloaded_urls = []
    
    if not downloaded_urls:
        warning_msg = f"No downloaded URLs found for author '{author}'. Nothing to transfer."
        print(warning_msg)
        update_author_status('pending', warning_msg)
        return
    
    print(f"record_downloaded_to_uploadedjpgs: Found {len(downloaded_urls)} downloaded URLs to transfer")

    # ============================================================
    # STEP 4: GET EXISTING UPLOADED URLs
    # ============================================================
    try:
        existing_uploaded = get_uploaded_jpgs_url_from_config(config)
        
        # Extract existing URL strings
        if isinstance(existing_uploaded, list):
            # Handle the complex structure from generate_final_csv
            existing_urls = []
            for item in existing_uploaded:
                if isinstance(item, str):
                    existing_urls.append(item)
                elif isinstance(item, dict):
                    # Skip metadata objects (like {'folder': author} or {'_timestamp': ...})
                    if not any(key.startswith('_') for key in item.keys()) and 'folder' not in item:
                        # Try to extract URL from dict
                        for key, value in item.items():
                            if isinstance(value, str) and value.startswith(('http://', 'https://')):
                                existing_urls.append(value)
            # Also check if the array contains a timestamp marker
        elif isinstance(existing_uploaded, str):
            try:
                parsed = json.loads(existing_uploaded)
                if isinstance(parsed, list):
                    existing_urls = [item for item in parsed if isinstance(item, str)]
                else:
                    existing_urls = []
            except:
                existing_urls = [u.strip() for u in existing_uploaded.split(',') if u.strip()]
        else:
            existing_urls = []
        
        print(f"record_downloaded_to_uploadedjpgs: Existing uploaded URLs: {len(existing_urls)}")
        
    except Exception as e:
        error_msg = f"record_downloaded_to_uploadedjpgs: ERROR - Failed to read existing uploaded URLs: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 5: COMBINE AND DEDUPLICATE
    # ============================================================
    all_uploaded = existing_urls + downloaded_urls
    unique_uploaded = list(dict.fromkeys(all_uploaded))
    
    newly_added = len(unique_uploaded) - len(existing_urls)
    
    print(f"record_downloaded_to_uploadedjpgs: Transfer results:")
    print(f"   Existing: {len(existing_urls)}")
    print(f"   Downloaded: {len(downloaded_urls)}")
    print(f"   Combined unique: {len(unique_uploaded)}")
    print(f"   Newly added: {newly_added}")

    # ============================================================
    # STEP 6: BUILD UPLOADED_JPGS_URL STRUCTURE
    # ============================================================
    timestamp = datetime.now(pytz.timezone('Africa/Lagos')).isoformat()
    
    uploaded_jpgs_array = [{"folder": author}] + unique_uploaded
    uploaded_jpgs_array.append({
        "_timestamp": timestamp,
        "_total_urls": len(unique_uploaded),
        "_added_this_time": len(downloaded_urls),
        "_new_unique": newly_added,
        "_source": "record_downloaded_to_uploadedjpgs",
        "_downloaded_urls_transferred": True
    })

    # ============================================================
    # STEP 7: UPDATE CONFIG
    # ============================================================
    try:
        # Update uploaded_jpgs_url
        if config_is_list:
            config_data[-1] = set_uploaded_jpgs_url_in_config(config_data[-1], uploaded_jpgs_array)
        else:
            config_data = set_uploaded_jpgs_url_in_config(config_data, uploaded_jpgs_array)
        
        # Clear downloaded_images_url
        if config_is_list:
            config_data[-1]['downloaded_images_url'] = []
        else:
            config_data['downloaded_images_url'] = []
        
        # Save to AUTHOR_PATH
        if save_json_file(AUTHOR_PATH, config_data):
            print(f"record_downloaded_to_uploadedjpgs: ✅ Config updated successfully")
            print(f"   uploaded_jpgs_url: {len(unique_uploaded)} total unique URLs")
            print(f"   downloaded_images_url: cleared (was {len(downloaded_urls)})")
        else:
            error_msg = "record_downloaded_to_uploadedjpgs: ERROR - Failed to save config to AUTHOR_PATH"
            print(error_msg)
            update_author_status('aborted', error_msg)
            return
        
    except Exception as e:
        error_msg = f"record_downloaded_to_uploadedjpgs: ERROR - Failed to update config: {e}"
        print(error_msg)
        update_author_status('aborted', error_msg)
        return

    # ============================================================
    # STEP 8: UPDATE STATUS
    # ============================================================
    success_msg = (
        f"Successfully transferred {len(downloaded_urls)} downloaded URLs to uploaded_jpgs_url for author '{author}'. "
        f"Total unique uploaded URLs: {len(unique_uploaded)}. Downloaded_images_url cleared."
    )
    update_author_status('pending', success_msg)
    print(f"\n✅ Status updated to 'pending' - Transfer completed successfully")

    # ============================================================
    # STEP 9: DISPLAY SUMMARY
    # ============================================================
    print(f"\n{'='*80}")
    print(f"RECORD DOWNLOADED TO UPLOADEDJPGS - SUMMARY")
    print(f"{'='*80}")
    print(f"Author:                    {author}")
    print(f"Downloaded URLs:           {len(downloaded_urls)}")
    print(f"Existing Uploaded URLs:    {len(existing_urls)}")
    print(f"New Unique URLs Added:     {newly_added}")
    print(f"Total Uploaded URLs:       {len(unique_uploaded)}")
    print(f"downloaded_images_url:     cleared ✅")
    print(f"uploaded_jpgs_url:         updated ✅")
    print(f"Status:                    pending ✅")
    print(f"{'='*80}\n")
    
    # Show first few URLs transferred
    if downloaded_urls:
        print("Transferred URLs (first 5):")
        for url in downloaded_urls[:5]:
            print(f"  • {url[:80]}...")
        if len(downloaded_urls) > 5:
            print(f"  ... and {len(downloaded_urls) - 5} more")
        print()
    
    return True

def sequence():  
    #*
    copy_downloaded_to_nextjpg()
    toggleaddphoto()
    #toggleaddphoto() #*
    selectgroups()
    writecaption_element()
    toggleschedule() #*
    update_calendar()
    set_webschedule() #*  
#===================#

def execute_engine():
    """Execute the appropriate engine based on the engine value.
    Executes regardless of status - NO STATUS CHECKS OR UPDATES."""
    
    def load_json_file(file_path, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default if default is not None else {}
        except json.JSONDecodeError:
            return default if default is not None else {}
        except Exception:
            return default if default is not None else {}
    
    # ============================================================
    # STEP 1: LOAD CONFIG - No status anything
    # ============================================================
    fetch_settings()
    try:
        config_data = load_json_file(AUTHOR_PATH, {})
        
        if isinstance(config_data, list) and len(config_data) > 0:
            config = config_data[-1]
        elif isinstance(config_data, dict):
            config = config_data
        else:
            error_msg = "execute_engine: ERROR - Invalid config format in AUTHOR_PATH."
            print(error_msg)
            return
        
        print(f"execute_engine: Config loaded successfully")
        
    except Exception as e:
        error_msg = f"execute_engine: ERROR - Failed to load config from {AUTHOR_PATH}: {e}"
        print(error_msg)
        return

    # ============================================================
    # STEP 2: GET ENGINE VALUE
    # ============================================================
    engine_value = config.get("engine", "").strip().lower()
    
    if not engine_value:
        error_msg = "execute_engine: ERROR - 'engine' field is missing or empty in config."
        print(error_msg)
        return
    
    print(f"execute_engine: Engine value: '{engine_value}'")
    
    # Get author info for logging
    author = config.get('author', 'Unknown')
    time_order = config.get('time_order', 'Unknown')

    # ============================================================
    # STEP 3: EXECUTE BASED ON ENGINE TYPE
    # ============================================================
    
    if engine_value == "driver":
        # ===== DRIVER ENGINE =====
        print(f"\n{'='*80}")
        print(f"EXECUTING DRIVER ENGINE")
        print(f"{'='*80}")
        print(f"Author: {author}")
        print(f"Time Order: {time_order}")
        print(f"{'='*80}\n")
        
        try:
            download_scheduled_images()
            # Initialize WebDriver
            print("execute_engine: Initializing WebDriver...")
            driver, wait = initialize_driver(mode="headed")
            
            if driver is None or wait is None:
                error_msg = f"execute_engine: DRIVER engine failed - WebDriver initialization returned None"
                print(f"❌ {error_msg}")
                return
            
            print("execute_engine: WebDriver initialized successfully")
            
            # Call update_calendar before launch_profile
            print("execute_engine: Calling update_calendar before launch_profile...")
            try:
                update_calendar()
                print("execute_engine: update_calendar completed")
            except Exception as e:
                error_msg = f"execute_engine: update_calendar failed: {str(e)}"
                print(f"⚠️ {error_msg}")
                # Continue anyway - don't abort
            
            # Execute launch_profile
            print("execute_engine: Calling launch_profile...")
            try:
                
                launch_profile()
                move_downloaded_urls_to_uploadedjpgsurl()
                print("execute_engine: launch_profile completed")
            except Exception as e:
                error_msg = f"execute_engine: launch_profile failed: {str(e)}"
                print(f"❌ {error_msg}")
                return
            
            # Update settings
            print("execute_engine: Calling update_settings...")
            try:
                update_settings()
                print("execute_engine: update_settings completed")
            except Exception as e:
                error_msg = f"execute_engine: update_settings failed: {str(e)}"
                print(f"⚠️ {error_msg}")
                # Don't abort - settings update is not critical
            
            print(f"\n✅ execute_engine: DRIVER engine completed successfully for author '{author}'")
            return
         
        except Exception as e:
            error_msg = f"execute_engine: DRIVER engine failed: {str(e)}"
            print(f"\n❌ {error_msg}")
            return
            
    elif engine_value == "csv":
        # ===== CSV ENGINE =====
        print(f"\n{'='*80}")
        print(f"EXECUTING CSV ENGINE")
        print(f"{'='*80}")
        print(f"Author: {author}")
        print(f"Time Order: {time_order}")
        print(f"{'='*80}\n")
        
        try:
            # Call csv_engine which handles the CSV pipeline
            print("execute_engine: Calling csv_engine...")
            csv_engine()
            print("execute_engine: csv_engine completed")
            
            # Update settings
            print("execute_engine: Calling update_settings...")
            try:
                update_settings()
                print("execute_engine: update_settings completed")
            except Exception as e:
                error_msg = f"execute_engine: update_settings failed: {str(e)}"
                print(f"⚠️ {error_msg}")
                # Don't abort - settings update is not critical
            
            print(f"\n✅ execute_engine: CSV engine completed successfully for author '{author}'")
            return
         
        except Exception as e:
            error_msg = f"execute_engine: CSV engine failed: {str(e)}"
            print(f"\n❌ {error_msg}")
            return
            
    else:
        # ===== UNKNOWN ENGINE =====
        error_msg = f"execute_engine: ERROR - Unknown engine: '{engine_value}'. Must be 'driver' or 'csv'."
        print(f"\n❌ {error_msg}")
        return
      
if __name__ == "__main__":
   execute_engine()


   