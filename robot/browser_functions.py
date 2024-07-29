from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from config import PATH_GECKODRIVER
import re

def open_link(link):
    print("Open browser")
    service = Service(executable_path=PATH_GECKODRIVER)
    # Set Firefox options if needed
    firefox_options = Options()
    # Initialize the Firefox WebDriver with the service and options
    driver = webdriver.Firefox(service=service, options=firefox_options)
    time.sleep(5)
    driver.get(link)
    time.sleep(5)
    driver.maximize_window()
    return driver
def contains_currency(search_phrase):
        patterns = [
            r'\$\d+(?:\.\d{1,2})?',  # $11.1 or $111.11
            r'\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?',  # $111,111.11
            r'\d+\s+dollars?',  # 11 dollars
            r'\d+\s+USD',  # 11 USD
            r'\$\d+\s+million',  # $111 million
            r'\$\d+\s+billion',  # $111 billion
            r'\$\d+\s+thousand'  # $111 thousand
        ]
        for pattern in patterns:
            if re.search(pattern, search_phrase, re.IGNORECASE):
                return True
        return False