import logging
import os
from azure.functions import InputStream
from azure.storage.blob import BlobServiceClient

# Параметри підключення
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME_IMPORT")
container_name_archive = os.getenv("AZURE_BLOB_CONTAINER_NAME_ARCHIVE")



def main(myblob: InputStream):
    try:
        # Логування інформації про оброблений файл
        logging.info(f"Python blob trigger function processed blob \n"
                     f"Name: {myblob.name}\n"
                     f"Blob Size: {myblob.length} bytes")
        print("VSE OK")

         # Підключення до Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Отримання клієнта контейнера
        container_client = blob_service_client.get_container_client(container_name)
        file_name = os.path.basename(myblob.name)
        print(file_name)
        # Завантаження файлу в контейнер
        file = container_client.download_blob(file_name)
        print(f"Файл '{myblob.name}' успішно завантажено")

        
    except Exception as e:
        logging.error(f"Error processing blob: {e}")
        print(f"Error: {e}")