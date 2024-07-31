import logging
import os
import time
from datetime import datetime, timedelta
import requests
from openpyxl import Workbook
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from browser_functions import contains_currency

logging.basicConfig(level=logging.INFO)

class APNewsFresh:
    def __init__(self, browser):
        self.driver = browser
        self.fs = FileSystem()
        self.download_folder = "output"
        self.excel_file = "output.xlsx"

        if not self.fs.folder_exists(self.download_folder):
            self.fs.create_directory(self.download_folder)

        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "Data"
        self.sheet.append(["TITLE", "DESCRIPTION", "PATH", "DATE", "COUNT_PHRASE", "CONTAIN_AMOUNT"])
    
    def click_search_button(self):
        element = self.driver.wait_until_element_is_visible(
            '//button[contains(@class, "search-button-class")]'
        )
        element.click()

    def enter_search_phrase(self, search_phrase):
        element = self.driver.wait_until_element_is_visible(
            '//input[contains(@class, "search-input-class")]'
        )
        element.send_keys(search_phrase)
        element.send_keys(Keys.RETURN)

    def choose_newest(self):
        element = self.driver.wait_until_element_is_visible(
            '.Select-input'
        )
        element.click()
        time.sleep(1)
        element = self.driver.wait_until_element_is_visible(
            '.Select-input > option:nth-child(2)'
        )
        element.click()
        self.driver.refresh()

    def source_apnews(self, search_phrase):
        self.click_search_button()
        self.enter_search_phrase(search_phrase)
        self.choose_newest()

    def click_random_element(self):
        while True:
            try:
                element = self.driver.find_element_by_css_selector(".fancybox-item")
                element.click()
                logging.info("Element clicked")
                break
            except Exception as e:
                logging.warning(f"Element not found. Trying again... Error: {e}")
                time.sleep(1)
    
    def get_texts_and_images_of_children(self, search_phrase):
        parent_element_selector = ".SearchResultsModule-results > bsp-list-loadmore:nth-child(1) > div:nth-child(2)"
        parent_element = self.driver.find_element_by_css_selector(parent_element_selector)
        child_elements = parent_element.find_elements_by_xpath("./*")

        for index, child in enumerate(child_elements, start=1):
            full_text = child.text.split('\n')
            title = full_text[0] if full_text else ""
            description = full_text[1] if len(full_text) > 1 else ""

            count = title.lower().count(search_phrase.lower()) + description.lower().count(search_phrase.lower())
            contain_value = contains_currency(search_phrase)
            
            images = child.find_elements_by_tag_name("img")
            image_paths = []
            for img_index, img in enumerate(images, start=1):
                img_url = img.get_attribute("src")
                if img_url:
                    date_time = self.get_date_time(child)
                    filename = f"image_{index}_{img_index}_{date_time}.jpg"
                    image_path = self.download_image(img_url, filename)
                    if image_path:
                        image_paths.append(image_path)

            date_time = self.get_date_time(child)
            
            for image_path in image_paths:
                self.sheet.append([title, description, image_path, date_time, count, contain_value])

    def get_date_time(self, element, max_attempts=3):
        attempts = 0
        while attempts < max_attempts:
            try:
                date_time_element = self.driver.wait_until_element_is_visible(
                    ".Timestamp-template"
                )
                date_time = date_time_element.text

                if date_time.lower() == 'yesterday':
                    yesterday = datetime.now() - timedelta(days=1)
                    date_time = yesterday.strftime("%Y-%m-%d")

                return date_time.replace(":", "-").replace(" ", "_")
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
        output_path = os.path.join(self.download_folder, self.excel_file)
        self.workbook.save(output_path)
        logging.info(f"Excel file saved as {output_path}")

