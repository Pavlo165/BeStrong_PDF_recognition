import logging
import os
import json
from azure.functions import InputStream
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Параметри підключення
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name_import = os.getenv("AZURE_BLOB_CONTAINER_NAME_IMPORT")
container_name_archive = os.getenv("AZURE_BLOB_CONTAINER_NAME_ARCHIVE")

FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

def main(myblob: InputStream):
    try:
        # Логування інформації про оброблений файл
        logging.info(f"Python blob trigger function processed blob \n"
                     f"Name: {myblob.name}\n"
                     f"Blob Size: {myblob.length} bytes")
        # print("VSE OK")

         # Підключення до Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Отримання клієнта контейнера
        container_client = blob_service_client.get_container_client(container_name_import)
        file_name = os.path.basename(myblob.name)
        print(file_name)
        # Завантаження файлу в контейнер
        pdf_data = container_client.download_blob(file_name)
        print(f"file '{myblob.name}' successfully uploaded")

         # Send PDF to Azure AI Document Intelligence
        document_analysis_client = DocumentAnalysisClient(endpoint=FORM_RECOGNIZER_ENDPOINT, credential=AzureKeyCredential(FORM_RECOGNIZER_KEY))
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", pdf_data)
        result = poller.result()

        # Convert result to JSON
        result_json = result.to_dict()

        # Upload JSON to Azure Blob Storage
        container_client = blob_service_client.get_container_client(container_name_archive)
        container_client.upload_blob(file_name + ".json", json.dumps(result_json))
        logging.info("PDF processed and JSON uploaded successfully.")
        
    except Exception as e:
        logging.error(f"Error processing blob: {e}")
        print(f"Error: {e}")