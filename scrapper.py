import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller  # Auto-install ChromeDriver

# Configure Chrome options for deployment
options = Options()
options.binary_location = "/usr/bin/google-chrome"  # Set Chrome binary for Linux (Koyeb)
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")  # Required for running in cloud environments
options.add_argument("--disable-dev-shm-usage")  # Prevents /dev/shm error in Docker

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

driver = None
wait = None
leaderboard_data = []

def start_driver():
    """Initialize WebDriver"""
    try:
        global driver, wait
        chromedriver_autoinstaller.install()  # Ensures correct ChromeDriver version
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
    except Exception as e:
        print("Error initializing WebDriver:", e)

def open_chrome(hacker_rank_url):
    """Open the HackerRank URL"""
    try:
        if driver is None:
            start_driver()
        driver.get(hacker_rank_url)
    except Exception as e:
        print("Error:", e)

def change_view_per_page():
    """Change leaderboard pagination to 100 entries per page"""
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".leaderboard-list-view .row")))

    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="s2id_pagination-length"]/a')))
    dropdown.click()

    option_100 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-drop"]/ul/li[4]/div')))
    option_100.click()

def extract_data():
    """Extract leaderboard usernames and scores"""
    global leaderboard_data
    time.sleep(5)

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "leaderboard-list-view")))

    leaderboards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "leaderboard-list-view")))

    for leaderboard in leaderboards:
        try:
            userna
