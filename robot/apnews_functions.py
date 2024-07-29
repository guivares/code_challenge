from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os
import requests
from openpyxl import Workbook
from browser_functions import contains_currency
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

class APNews_fresh:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.download_folder = "images"
        self.excel_file = "output.xlsx"

        # Create download folder if it does not exist
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

       # Create an Excel workbook and add headers
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "Data"
        self.sheet.append(["TITLE", "DESCRIPTION", "PATH", "DATE", "COUNT_PHRASE", "COUNTAIN_AMOUNT"])
    
    def click_search_button(self):
        element = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/bsp-header/div[2]/div[3]/bsp-search-overlay/button')))
        element.click()

    def enter_search_phrase(self, search_phrase):
        element = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '/html/body/div[2]/bsp-header/div[2]/div[3]/bsp-search-overlay/div/form/label/input')))
        element.send_keys(search_phrase)
        element.send_keys(Keys.RETURN)

    def choose_newest(self):
        element = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.Select-input')))
        element.click()
        time.sleep(1)
        element = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.Select-input > option:nth-child(2)')))
        element.click()
        self.driver.refresh()

    def source_apnews(self, search_phrase):
        self.click_search_button()
        self.enter_search_phrase(search_phrase)
        self.choose_newest()

    def click_random_element(self):
        while True:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, ".fancybox-item")
                element.click()
                logging.info("Element clicked")
                break  # Saia do loop após clicar no elemento
            except Exception as e:
                logging.warning("Element not found. Trying again...")
                time.sleep(1)  # Espera antes de tentar novamente
    
    def get_texts_and_images_of_children(self, search_phrase):
        parent_element_selector = ".SearchResultsModule-results > bsp-list-loadmore:nth-child(1) > div:nth-child(2)"
        parent_element = self.driver.find_element(By.CSS_SELECTOR, parent_element_selector)
        child_elements = parent_element.find_elements(By.XPATH, "./*")

        for index, child in enumerate(child_elements, start=1):
            full_text = child.text.split('\n')
            title = full_text[0] if full_text else ""
            description = full_text[1] if len(full_text) > 1 else ""

             # Count occurrences of search_phrase in title and description
            count = title.lower().count(search_phrase.lower()) + description.lower().count(search_phrase.lower())
            countain_value = contains_currency(search_phrase)
            
            # Find and download images
            images = child.find_elements(By.TAG_NAME, "img")
            image_paths = []
            for img_index, img in enumerate(images, start=1):
                img_url = img.get_attribute("src")
                if img_url:
                    # Get date and time if available
                    date_time = self.get_date_time(child)
                    filename = f"image_{index}_{img_index}_{date_time}.jpg"
                    image_path = self.download_image(img_url, filename)
                    if image_path:  # Ensure image_path is not empty
                        image_paths.append(image_path)

            # Get date and time
            date_time = self.get_date_time(child)
            
            # Add data to Excel
            for image_path in image_paths:
                self.sheet.append([title, description, filename, date_time, count, countain_value])

    def get_date_time(self, element, max_attempts=3):
        attempts = 0
        while attempts < max_attempts:
            try:
                # Wait for the Timestamp-template element to be visible
                date_time_element = WebDriverWait(element, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".Timestamp-template"))
                )
                date_time = date_time_element.text  # Assuming the date and time are in the text

                # Check if the date_time is 'yesterday' and replace it with actual date
                if date_time.lower() == 'yesterday':
                    yesterday = datetime.now() - timedelta(days=1)
                    date_time = yesterday.strftime("%Y-%m-%d")

                return date_time.replace(":", "-").replace(" ", "_")  # Format for filename
            except Exception as e:
                logging.error(f"Error extracting date and time: {e}")
                attempts += 1
                if attempts < max_attempts:
                    logging.info(f"Retrying... (attempt {attempts + 1}/{max_attempts})")
                    self.driver.refresh()
                else:
                    logging.error("Max attempts reached. Returning 'unknown_time'.")
                    return "unknown_time"

    def download_image(self, url, filename):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_path = os.path.join(self.download_folder, filename)
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                logging.info(f"Downloaded {filename} to {image_path}")
                return image_path
            else:
                logging.warning(f"Failed to download image: {url}")
                return ""
        except Exception as e:
            logging.error(f"Error downloading image: {url}, error: {e}")
            return ""

    def save_excel(self):
        output_path = os.path.join("output", self.excel_file)
        self.workbook.save(output_path)
        logging.info(f"Excel file saved as {output_path}")