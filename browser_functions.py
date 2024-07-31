import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from config import PATH_GECKODRIVER

logging.basicConfig(level=logging.INFO)

def open_link(link):
    logging.info("Opening browser")
    service = Service(executable_path=PATH_GECKODRIVER)
    firefox_options = Options()
    
    driver = webdriver.Firefox(service=service, options=firefox_options)
    time.sleep(5)
    driver.get(link)
    time.sleep(5)
    driver.maximize_window()
    
    logging.info(f"Opened link: {link}")
    return driver

def contains_currency(search_phrase):
    patterns = [
        r'\$\d+(?:\.\d{1,2})?',             # $11.1 or $111.11
        r'\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?', # $111,111.11
        r'\d+\s+dollars?',                   # 11 dollars
        r'\d+\s+USD',                        # 11 USD
        r'\$\d+\s+million',                  # $111 million
        r'\$\d+\s+billion',                  # $111 billion
        r'\$\d+\s+thousand'                  # $111 thousand
    ]
    
    for pattern in patterns:
        if re.search(pattern, search_phrase, re.IGNORECASE):
            logging.info(f"Currency pattern found in phrase: {search_phrase}")
            return True
            
    logging.info(f"No currency pattern found in phrase: {search_phrase}")
    return False
