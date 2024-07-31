# import sys
# import json
# import logging
# from config import LINK_APNEWS
# from apnews_functions import APNewsFresh
# from RPA.Browser.Selenium import Selenium
# from RPA.FileSystem import FileSystem

# logging.basicConfig(level=logging.INFO)

# def main():
#     logging.info("Starting main function")

#     work_item = None
#     if not sys.stdin.isatty():
#         try:
#             logging.info(f"Reading work item from stdin")
#             work_item = json.loads(sys.stdin.read())
#             logging.info(f"Work item read successfully: {work_item}")
#         except json.JSONDecodeError as e:
#             logging.error(f"Error decoding JSON from work item: {e}")
#             return
#         except Exception as e:
#             logging.error(f"Unexpected error reading work item: {e}")
#             return

#     logging.info(f"Processing search phrase: {work_item['payload']['search_phrase']}")

#     search_phrase = work_item.get("payload", {}).get("search_phrase", "Default Search Phrase")
#     files = work_item.get("files", {})

#     file_system = FileSystem()
#     orders_file_path = files.get("orders.xlsx")
#     if orders_file_path and file_system.file_exists(orders_file_path):
#         logging.info(f"Processing file: {orders_file_path}")
#         # Process file orders.xlsx
#     else:
#         logging.warning("File 'orders.xlsx' not found or not provided.")

#     browser = Selenium()
#     browser.open_available_browser(LINK_APNEWS, headless=True)
#     ap_news = APNewsFresh(browser)
#     ap_news.source_apnews(search_phrase)
#     ap_news.get_texts_and_images_of_children(search_phrase)
#     ap_news.save_excel()
#     browser.close_browser()

# if __name__ == "__main__":
#     main()

from RPA.Robocorp.WorkItems import WorkItems
from RPA.Robocorp.Process import Process
import logging
import os
from apnews_functions import APNewsFresh
from browser_functions import open_link

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    # Cria uma instância do WorkItems
    workitems = WorkItems()

    # Obtém o item de trabalho atual
    item = workitems.inputs.current
    search_phrase = item.payload.get("search_phrase", "Default Search Phrase")
    files = item.files

    # Verifica se o arquivo 'orders.xlsx' está presente
    orders_file_path = files.get("orders.xlsx")
    if orders_file_path:
        logging.info(f"Processing file: {orders_file_path}")
        # Processar arquivo orders.xlsx se necessário

    # Configura o driver e instancia a classe APNewsFresh
    driver = open_link("https://apnews.com")  # Use o link apropriado aqui
    ap_news = APNewsFresh(driver)
    ap_news.source_apnews(search_phrase)
    ap_news.get_texts_and_images_of_children(search_phrase)
    ap_news.save_excel()

    driver.quit()

    # Cria um item de trabalho de saída com o resultado
    workitems.outputs.create(payload={"status": "completed"}, files={"output.xlsx": "output/output.xlsx"})

if __name__ == "__main__":
    main()
