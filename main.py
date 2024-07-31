import logging
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Browser.Selenium import Selenium
from apnews_functions import APNewsFresh
from browser_functions import open_link  


def main():
    logging.basicConfig(level=logging.INFO)
    work_items = WorkItems()
    work_items.get_input_work_item()

    search_phrase = work_items.get_work_item_variable("payload").get("search_phrase", "Default Search Phrase")
    logging.info(f"Search phrase: {search_phrase}")

    browser = Selenium()
    
    open_link("https://apnews.com")

    try:
        apnews = APNewsFresh(browser)
        logging.info("Opening browser")
        apnews.source_apnews(search_phrase)
        apnews.get_texts_and_images_of_children(search_phrase)
        apnews.save_excel()
    except Exception as e:
        logging.error(f"Error processing item: {e}")
    finally:
        browser.close_browser()

    work_items.save_work_item()
    work_items.release_input_work_item(state="processed") 

if __name__ == "__main__":
    main()
