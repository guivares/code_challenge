import re
import logging
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem

logging.basicConfig(level=logging.INFO)

def open_link(link):
    logging.info("Opening browser")
    browser = Selenium()
    browser.open_available_browser(link, headless=True)
    browser.set_browser_window_size(1920, 1080)
    logging.info(f"Opened link: {link}")
    return browser

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
