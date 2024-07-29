import sys
import json
import os
import logging
from config import LINK_APNEWS
from apnews_functions import APNews_fresh
from browser_functions import open_link

logging.basicConfig(level=logging.INFO)

def main():
    # Lê o work item do Robocorp
    work_item = json.loads(sys.stdin.read())
    search_phrase = work_item.get("payload", {}).get("search_phrase", "Default Search Phrase")
    files = work_item.get("files", {})

    # Verifica se o arquivo orders.xlsx foi fornecido e existe
    orders_file_path = files.get("orders.xlsx", None)
    if orders_file_path and os.path.exists(orders_file_path):
        logging.info(f"Processing file: {orders_file_path}")
        # Processar o arquivo orders.xlsx conforme necessário
    else:
        logging.warning("File 'orders.xlsx' not found or not provided.")

    # Inicia o driver e executa a lógica de scraping
    driver = open_link(LINK_APNEWS)
    ApNews = APNews_fresh(driver)
    ApNews.source_apnews(search_phrase)
    ApNews.get_texts_and_images_of_children(search_phrase)
    # Salva o arquivo Excel
    ApNews.save_excel()
    driver.quit()

if __name__ == "__main__":
    main()