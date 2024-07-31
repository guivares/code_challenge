import sys
import json
import os
import logging
from config import LINK_APNEWS
from apnews_functions import APNewsFresh
from browser_functions import open_link

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting main function")

    work_item = None
    if not sys.stdin.isatty():
        try:
            logging.info("Reading work item from stdin")
            work_item = json.loads(sys.stdin.read())
            logging.info(f"Work item read successfully: {work_item}")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from work item: {e}")
            return
        except Exception as e:
            logging.error(f"Unexpected error reading work item: {e}")
            return

    # Your logic to process work_item
    logging.info(f"Processing search phrase: {work_item['payload']['search_phrase']}")

    logging.info("Work item read successfully")

    search_phrase = work_item.get("payload", {}).get("search_phrase", "Default Search Phrase")
    files = work_item.get("files", {})

    orders_file_path = files.get("orders.xlsx")
    if orders_file_path and os.path.exists(orders_file_path):
        logging.info(f"Processing file: {orders_file_path}")
        # Process file orders.xlsx
    else:
        logging.warning("File 'orders.xlsx' not found or not provided.")

    driver = open_link(LINK_APNEWS)
    ap_news = APNewsFresh(driver)
    ap_news.source_apnews(search_phrase)
    ap_news.get_texts_and_images_of_children(search_phrase)
    ap_news.save_excel()
    driver.quit()

if __name__ == "__main__":
    main()
