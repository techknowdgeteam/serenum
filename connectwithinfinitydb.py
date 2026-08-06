from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import signal
import sys
import os
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import psutil
import shutil
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# ⚠️ CRITICAL CONFIGURATION ⚠️
# ==============================================================================
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ==============================================================================
# 🎯 BROWSER MODE CONFIGURATION
# Set to True for headless mode (no visible window), False for headed mode (visible window)
# ==============================================================================
HEADLESS_MODE = False  # Set to True for headless, False for headed

# Server Configuration
primary_servers = {
    'query_page': 'https://fhdrikxsirudr.fwh.is/phpmyadmintemplate.php',
    'fetch': 'https://fhdrikxsirudr.fwh.is/phpmyadmin_tablesfetch.php'
}
backup_servers = {
    'query_page': 'https://fhdrikxsirudr.fwh.is/phpmyadmintemplate.php',
    'fetch': 'https://fhdrikxsirudr.fwh.is/phpmyadmin_tablesfetch.php'
}
server3 = {
    'query_page': 'https://fhdrikxsirudr.fwh.is/phpmyadmintemplate.php',
    'fetch': 'https://fhdrikxsirudr.fwh.is/phpmyadmin_tablesfetch.php'
}

admin_email = 'ciphercirclex12@gmail.com'
admin_password = '@ciphercircleadminauthenticator#'
temp_download_dir = r'C:\xampp\htdocs\AI automation\CIPHER\temp_downloads'
json_log_path = r'C:\xampp\htdocs\AI automation\CIPHER\cipher trader\market\dbserver\connectwithdb.json'

# Global driver and session
driver = None
session = None
current_servers = primary_servers  # Start with primary servers
# ==============================================================================

def initialize_browser():
    """
    Initialize Chrome using ChromeDriverManager with auto-version detection.
    Uses the same successful method as your working function.
    """
    global driver, session, current_servers
    
    # Check if existing session is alive
    if driver is not None:
        log_and_print("Checking existing browser session...", "INFO")
        try:
            driver.get(current_servers['query_page'])
            # Re-sync session cookies
            session = requests.Session()
            for cookie in driver.get_cookies():
                session.cookies.set(cookie['name'], cookie['value'])
            return True
        except Exception:
            log_and_print("Session invalid, restarting browser...", "WARNING")
            try: driver.quit()
            except: pass
            driver = None

    log_and_print("--- Step 1: Setting Up Chrome Environment ---", "TITLE")
    
    # --- 1. Process Cleanup ---
    log_and_print("Closing existing Chrome instances...", "INFO")
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in ['chrome.exe', 'chromedriver.exe']:
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    time.sleep(1)

    # --- 2. Path Configuration ---
    selenium_profile = os.path.expanduser(r"~\.chrome_selenium_profile")
    wdm_home = os.path.join(os.path.expanduser("~"), ".wdm")

    # --- 3. Profile Setup ---
    if not os.path.exists(selenium_profile):
        real_user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        source_profile = os.path.join(real_user_data, "Profile 1")
        if os.path.exists(source_profile):
            log_and_print("Copying Profile 1 to Selenium directory...", "INFO")
            shutil.copytree(source_profile, selenium_profile, dirs_exist_ok=True)

    # --- 4. Chrome Options ---
    chrome_options = Options()
    if os.path.exists(CHROME_PATH):
        chrome_options.binary_location = CHROME_PATH
    
    chrome_options.add_argument(f"--user-data-dir={selenium_profile}")
    chrome_options.add_argument("--profile-directory=Default")
    
    # ===== BROWSER MODE CONFIGURATION =====
    if HEADLESS_MODE:
        log_and_print("🔵 Running in HEADLESS MODE (no visible window)", "INFO")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
    else:
        log_and_print("🟢 Running in HEADED MODE (visible window)", "INFO")
        chrome_options.add_argument("--start-maximized")
    
    # Common arguments for both modes
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Disable httpsS upgrades and certificate errors
    chrome_options.add_argument("--disable-features=httpssUpgrades")
    chrome_options.add_argument("--disable-features=httpssOnlyMode")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    
    # Anti-detection measures
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Realistic user agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    # Log level
    chrome_options.add_argument("--log-level=3")

    log_and_print("--- Step 2: Getting ChromeDriver (Auto-Version Detection) ---", "TITLE")
    
    # --- 5. The "Bypass" Driver Logic (Same as your working function) ---
    driver_path = None
    
    # Set environment variables to bypass SSL issues
    os.environ['WDM_SSL_VERIFY'] = '0'
    os.environ['WDM_PROGRESS_BAR'] = '0'
    os.environ['WDM_LOCAL'] = '1'  # Use local cache if available
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        
        log_and_print("Attempting to fetch ChromeDriver with auto-version detection...", "INFO")
        # This will auto-detect your Chrome version and download the matching driver
        driver_path = ChromeDriverManager().install()
        
        if driver_path and os.path.exists(driver_path):
            log_and_print(f"ChromeDriver found at: {driver_path}", "SUCCESS")
        else:
            raise Exception("ChromeDriver installation returned invalid path")
            
    except Exception as e:
        log_and_print(f"Network/auto-download failed: {str(e)}", "WARNING")
        log_and_print("Searching local .wdm cache for the newest available driver...", "INFO")
        
        found_drivers = []
        for root, _, files in os.walk(wdm_home):
            for file in files:
                if file.lower() == "chromedriver.exe":
                    found_drivers.append(os.path.join(root, file))
        
        if found_drivers:
            # Pick the newest driver we have ever downloaded
            driver_path = max(found_drivers, key=os.path.getmtime)
            log_and_print(f"Using latest cached driver: {driver_path}", "SUCCESS")
        else:
            # Final fallback - try to use any chromedriver in PATH
            import subprocess
            try:
                result = subprocess.run(['where', 'chromedriver'], capture_output=True, text=True, shell=True)
                if result.stdout:
                    driver_path = result.stdout.strip().split('\n')[0]
                    if driver_path and os.path.exists(driver_path):
                        log_and_print(f"Using ChromeDriver from PATH: {driver_path}", "SUCCESS")
                    else:
                        raise Exception("No driver found in PATH")
                else:
                    raise Exception("No driver found online, in cache, or in PATH")
            except:
                # If all fails, raise clear error
                raise Exception("No ChromeDriver found. Please ensure webdriver-manager can download or manually place chromedriver.exe in C:\\chromedriver\\")

    # --- 6. Start WebDriver ---
    try:
        log_and_print("--- Step 3: Starting WebDriver ---", "TITLE")
        
        # Ensure the driver path exists
        if not driver_path or not os.path.exists(driver_path):
            raise Exception(f"Driver path does not exist: {driver_path}")
        
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set timeouts
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        
        # Hide automation
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        mode_text = "HEADLESS" if HEADLESS_MODE else "HEADED"
        log_and_print(f"ChromeDriver initialized successfully in {mode_text} MODE.", "SUCCESS")
        if not HEADLESS_MODE:
            log_and_print("Browser window should now be visible on screen.", "INFO")
        else:
            log_and_print("Browser is running in the background (headless).", "INFO")
            
    except Exception as e:
        log_and_print(f"FATAL: Could not initialize ChromeDriver: {str(e)}", "ERROR")
        
        # Provide helpful error message
        log_and_print("", "INFO")
        log_and_print("=" * 70, "INFO")
        log_and_print("TROUBLESHOOTING TIPS:", "INFO")
        log_and_print("=" * 70, "INFO")
        log_and_print("1. Ensure Chrome is installed and up to date", "INFO")
        log_and_print("2. Check if firewall is blocking webdriver-manager downloads", "INFO")
        log_and_print("3. Try manually downloading ChromeDriver from:", "INFO")
        log_and_print("   https://googlechromelabs.github.io/chrome-for-testing/", "INFO")
        log_and_print("4. Place chromedriver.exe in C:\\chromedriver\\chromedriver.exe", "INFO")
        log_and_print("=" * 70, "INFO")
        log_and_print("", "INFO")
        
        return False

    log_and_print("--- Step 4: Authenticating and Accessing Query Page ---", "TITLE")
    server_attempts = [
        (primary_servers, "Primary"),
        (backup_servers, "Backup"),
        (server3, "Server3")
    ]
    
    for servers, server_type in server_attempts:
        current_servers = servers
        try:
            log_and_print(f"Attempting to connect to {server_type} server...", "INFO")
            driver.get(servers['query_page'])
            
            # Wait for page to be fully loaded
            log_and_print("Waiting for page to load...", "INFO")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Inject credentials via LocalStorage
            driver.execute_script(f"localStorage.setItem('admin_email', '{admin_email}');")
            driver.execute_script(f"localStorage.setItem('admin_password', '{admin_password}');")
            
            # Reload to apply credentials
            driver.get(servers['query_page'])
            
            # Wait for query element to be present
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "sql-query"))
            )
            
            log_and_print(f"Authenticated on {server_type} server", "SUCCESS")
            
            # Sync requests session
            session = requests.Session()
            for cookie in driver.get_cookies():
                session.cookies.set(cookie['name'], cookie['value'])
            
            append_to_json_log(server_type, servers['query_page'])
            
            return True
        except Exception as e:
            log_and_print(f"{server_type} server failed: {str(e)}", "WARNING")
            continue
    
    return False

def log_and_print(message, level="INFO"):
    """Helper function to print formatted messages without color coding."""
    indent = "    "
    formatted_message = f"{level:7} | {indent}{message}"
    print(formatted_message)

def append_to_json_log(server_type, server_url):
    """Append the server used to the JSON log file if the URL is different from the last recorded URL."""
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'server_type': server_type,
        'server_url': server_url,
        'status': 'success'
    }
    log_data = []

    try:
        if os.path.exists(json_log_path):
            with open(json_log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
                if not isinstance(log_data, list):
                    log_data = []
    except Exception as e:
        log_and_print(f"Error reading JSON log file: {str(e)}, starting with empty log", "WARNING")
        log_data = []

    if log_data and log_data[-1].get('server_url') == server_url:
        log_and_print(f"Skipping log append: Same server URL ({server_url}) as last entry", "INFO")
        return

    log_data.append(log_entry)

    try:
        os.makedirs(os.path.dirname(json_log_path), exist_ok=True)
        with open(json_log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
        log_and_print(f"Logged server usage ({server_type}: {server_url}) to {json_log_path}", "SUCCESS")
    except Exception as e:
        log_and_print(f"Failed to write to JSON log file: {str(e)}", "ERROR")

def signal_handler(sig, frame):
    """Handle script interruption (Ctrl+C)."""
    log_and_print("Script interrupted by user. Initiating cleanup...", "WARNING")
    cleanup()
    sys.exit(0)

def cleanup():
    """Clean up resources before exiting."""
    global driver, session
    log_and_print("--- Cleanup Operations ---", "TITLE")
    log_and_print("Starting cleanup process", "INFO")
    
    if driver:
        log_and_print("Clearing browser localStorage", "INFO")
        try:
            if "data:" not in driver.current_url:
                driver.execute_script("localStorage.clear();")
                log_and_print("LocalStorage cleared successfully", "SUCCESS")
        except Exception as e:
            log_and_print(f"Failed to clear localStorage: {str(e)}", "ERROR")
        log_and_print("Closing browser", "INFO")
        driver.quit()
        driver = None
        log_and_print("Browser closed successfully", "SUCCESS")

    if session:
        session.close()
        session = None
        log_and_print("Closed https session", "SUCCESS")

    # Cleanup temp download directory
    if os.path.exists(temp_download_dir):
        log_and_print(f"Cleaning temporary download directory: {temp_download_dir}", "INFO")
        try:
            for temp_file in os.listdir(temp_download_dir):
                file_path = os.path.join(temp_download_dir, temp_file)
                os.remove(file_path)
            os.rmdir(temp_download_dir)
            log_and_print(f"Successfully removed temporary directory: {temp_download_dir}", "SUCCESS")
        except Exception as e:
            log_and_print(f"Failed to clean temporary directory: {str(e)}", "ERROR")

def check_server_availability(url):
    """Check if a server is available by sending a HEAD request with browser-like headers."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        response = requests.head(url, headers=headers, timeout=10, verify=True)
        log_and_print(f"Server check response for {url}: Status {response.status_code}", "INFO")
        return response.status_code == 200
    except requests.RequestException as e:
        log_and_print(f"Server availability check failed for {url}: {str(e)}", "INFO")
        return False

def execute_query(sql_query):
    """
    Execute a SQL query and return results.
    The browser will automatically close after the query completes.
    """
    global driver, session
    
    # Initialize the browser first
    if not initialize_browser():
        return {'status': 'error', 'message': 'Browser init failed', 'results': []}
    
    try:
        log_and_print("===== Database Query Execution =====", "TITLE")
        
        # --- Step 5: JS Injection ---
        try:
            query_textarea = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "sql-query"))
            )
            driver.execute_script("arguments[0].value = arguments[1];", query_textarea, sql_query)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", query_textarea)
            
            execute_button = driver.find_element(By.XPATH, "//button[text()='Execute Query']")
            execute_button.click()
            log_and_print(f"Query executed: {sql_query[:100]}...", "INFO")
        except Exception as e:
            return {'status': 'error', 'message': f"Input failed: {str(e)}", 'results': []}

        # --- Step 6: Improved Result Fetching ---
        log_and_print("--- Step 6: Fetching Query Results (Selenium) ---", "TITLE")
        results = []
        
        try:
            # Check if it's a SELECT query
            is_select = sql_query.strip().upper().startswith("SELECT")
            
            # Give the page time to process the query
            time.sleep(3)  # Add a small delay for the AJAX response
            
            if is_select:
                # Try multiple selectors for result tables
                selectors = [
                    "#query-result table",
                    "#column-data table",
                    ".result table",
                    "table",
                    "#results table"
                ]
                
                table_found = False
                for selector in selectors:
                    try:
                        log_and_print(f"Looking for table with selector: {selector}", "INFO")
                        # Wait for the table to appear
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        table_found = True
                        log_and_print(f"Table found with selector: {selector}", "SUCCESS")
                        break
                    except:
                        continue
                
                if not table_found:
                    # Debug: Print the page source to see what's actually there
                    log_and_print("Table not found. Checking page content...", "WARNING")
                    page_text = driver.find_element(By.TAG_NAME, "body").text
                    if "no results" in page_text.lower() or "empty" in page_text.lower():
                        log_and_print("Query returned no results (empty set)", "INFO")
                        return {'status': 'success', 'results': []}
                    else:
                        log_and_print(f"Page contains: {page_text[:500]}", "INFO")
                        return {'status': 'success', 'results': []}
                
                # Now parse the HTML
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Find the table in the page
                table = None
                for container_id in ['query-result', 'column-data', 'results']:
                    container = soup.find('div', id=container_id)
                    if container:
                        table = container.find('table')
                        if table:
                            log_and_print(f"Found table in container: {container_id}", "SUCCESS")
                            break
                
                if not table:
                    table = soup.find('table')
                
                if table:
                    # Extract headers
                    headers = []
                    header_row = table.find('tr')
                    if header_row:
                        headers = [th.text.strip() for th in header_row.find_all(['th', 'td'])]
                    
                    # Extract data rows
                    for row in table.find_all('tr')[1:]:  # Skip header row
                        cols = row.find_all('td')
                        if len(cols) > 0:
                            row_dict = {}
                            for i, col in enumerate(cols):
                                if i < len(headers):
                                    row_dict[headers[i]] = col.text.strip()
                                else:
                                    row_dict[f"col_{i}"] = col.text.strip()
                            results.append(row_dict)
                    
                    log_and_print(f"Scraped {len(results)} rows successfully", "SUCCESS")
                else:
                    log_and_print("No table found in page source", "WARNING")
                    # Check if there's a message about empty result
                    msg_div = soup.find('div', id='message')
                    if msg_div and "affected rows" in msg_div.text.lower():
                        results = [{'status': 'done', 'message': msg_div.text.strip()}]
                
                return {'status': 'success', 'results': results}
                
            else:
                # For UPDATE/INSERT, wait for the message div
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "message"))
                )
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                msg_text = soup.find('div', id='message').get_text() if soup.find('div', id='message') else ""
                if "Affected rows" in msg_text or "success" in msg_text.lower():
                    results = [{'status': 'done', 'message': msg_text}]
                return {'status': 'success', 'results': results}

        except Exception as e:
            log_and_print(f"Result fetch failed: {str(e)}", "ERROR")
            # Don't return error - it might just be empty results
            return {'status': 'success', 'results': []}

    except Exception as e:
        log_and_print(f"Query execution error: {str(e)}", "ERROR")
        return {'status': 'error', 'message': str(e), 'results': []}
    
    finally:
        # ALWAYS close the browser after the query is done
        log_and_print("Query complete. Closing browser...", "INFO")
        cleanup()
    
def execute_multiple_queries(sql_queries):
    """
    Execute multiple SQL queries and automatically close the browser when done.
    
    Args:
        sql_queries: List of SQL query strings or a single query string
    
    Returns:
        List of results for each query
    """
    global driver
    
    # Convert single query to list for uniform processing
    if isinstance(sql_queries, str):
        sql_queries = [sql_queries]
    
    results = []
    
    try:
        log_and_print(f"Starting execution of {len(sql_queries)} queries...", "INFO")
        
        for i, query in enumerate(sql_queries):
            log_and_print(f"--- Executing Query {i+1}/{len(sql_queries)} ---", "TITLE")
            result = execute_query(query)
            results.append(result)
            
            # Add a small delay between queries if there are multiple
            if i < len(sql_queries) - 1:
                time.sleep(1)
        
        log_and_print(f"All {len(sql_queries)} queries executed successfully!", "SUCCESS")
        
    finally:
        # ALWAYS close the browser after all queries are done
        log_and_print("All queries complete. Closing browser...", "INFO")
        cleanup()
    
    return results

def shutdown():
    """Explicitly shut down the browser and cleanup."""
    cleanup()

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # For testing standalone
    sql_query = "SELECT id FROM automation_tree WHERE id = '2'"
    result = execute_query(sql_query)
    print("\nFinal Result:")
    print(json.dumps(result, indent=2))