from RPA.Robocorp.WorkItems import WorkItems
from RPA.Robocorp.Process import Process
from robocorp.tasks import task
import logging
import os
from apnews_functions import APNewsFresh
from browser_functions import open_link

# Configure logging
logging.basicConfig(level=logging.INFO)

@task
def process_work_item():
    # Cria uma instância do WorkItems
    workitems = WorkItems()

    # Verifica se há itens de trabalho na lista de inputs
    if not workitems.inputs:
        logging.error("No input work items found.")
        return

    # Loop através de todos os itens de trabalho de entrada
    for item in workitems.inputs:
        with item:  # Reserva o item de trabalho
            try:
                logging.info(f"Processing item: {item}")
                
                # Obtém o search_phrase do payload, com um valor padrão
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
                output_item = workitems.outputs.create(
                    payload={"status": "completed"},
                    files={"output.xlsx": "output/output.xlsx"}
                )
                output_item.save()

                # Marca o item como concluído
                item.done()
            except Exception as e:
                # Marca o item como falhado em caso de erro
                logging.error(f"Error processing item: {e}")
                item.fail(message=str(e))

if __name__ == "__main__":
    process_work_item()


# from RPA.Robocorp.WorkItems import WorkItems
# from RPA.Robocorp.Process import Process
# import logging
# import os
# from apnews_functions import APNewsFresh
# from browser_functions import open_link

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# def main():
#     # Cria uma instância do WorkItems
#     workitems = WorkItems()

#     # Obtém o primeiro item de trabalho da lista
#     if not workitems.inputs:
#         logging.error("No input work items found.")
#         return

#     # Usa o primeiro item da lista de inputs
#     item = workitems.inputs[0]
#     logging.info(f"Processing file: {item}")
    
#     search_phrase = item.payload.get("search_phrase", "Default Search Phrase")
#     files = item.files

#     # Verifica se o arquivo 'orders.xlsx' está presente
#     orders_file_path = files.get("orders.xlsx")
#     if orders_file_path:
#         logging.info(f"Processing file: {orders_file_path}")
#         # Processar arquivo orders.xlsx se necessário

#     # Configura o driver e instancia a classe APNewsFresh
#     driver = open_link("https://apnews.com")  # Use o link apropriado aqui
#     ap_news = APNewsFresh(driver)
#     ap_news.source_apnews(search_phrase)
#     ap_news.get_texts_and_images_of_children(search_phrase)
#     ap_news.save_excel()

#     driver.quit()

#     # Cria um item de trabalho de saída com o resultado
#     workitems.outputs.create(payload={"status": "completed"}, files={"output.xlsx": "output/output.xlsx"})

# if __name__ == "__main__":
#     main()
