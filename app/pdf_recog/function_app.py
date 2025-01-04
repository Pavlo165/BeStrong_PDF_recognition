import azure.functions as func
import datetime
import json
import logging
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
SHARE_NAME = os.getenv("AZURE_FILE_SHARE_NAME")
#FILE_PATH = os.getenv("AZURE_FILE_PATH")  # Тепер це шлях до директорії
BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME")
FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

app = func.FunctionApp()

@app.function_name(name="mytimer")
@app.timer_trigger(schedule="0 */2 * * * *", 
              arg_name="mytimer",
              run_on_startup=True)
def test_function(mytimer: func.TimerRequest) -> None:

    try:
        # Підключення до директорії у File Share
        directory_client = ShareDirectoryClient.from_connection_string(
            STORAGE_CONNECTION_STRING, share_name=SHARE_NAME, directory_path=None
        )

        # Отримуємо список файлів у директорії
        file_list = directory_client.list_directories_and_files()

        for file_item in file_list:
            # Перевіряємо, чи це файл (а не піддиректорія)
            if file_item["is_directory"]:
                continue

            file_name = file_item["name"]
            logging.info(f"Processing file: {file_name}")

            # Завантаження файлу
            file_client = ShareFileClient.from_connection_string(
                STORAGE_CONNECTION_STRING, share_name=SHARE_NAME, file_path=file_name
            )
            pdf_data = file_client.download_file().readall()
            logging.info(f"File {file_name} downloaded successfully.")

            # Надсилаємо файл на аналіз до Azure AI Document Intelligence
            document_analysis_client = DocumentAnalysisClient(
                endpoint=FORM_RECOGNIZER_ENDPOINT, credential=AzureKeyCredential(FORM_RECOGNIZER_KEY)
            )
            poller = document_analysis_client.begin_analyze_document("prebuilt-document", pdf_data)
            result = poller.result()

            # Перетворюємо результат на JSON
            result_json = result.to_dict()

            # Формуємо унікальне ім'я для файлу на основі дати та часу
            timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
            unique_blob_name = f"{os.path.splitext(file_name)[0]}_{timestamp}.json"

            # Завантажуємо JSON до Azure Blob Storage
            blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=unique_blob_name)
            blob_client.upload_blob(json.dumps(result_json), overwrite=True)
            logging.info(f"Processed file {file_name} and uploaded as {unique_blob_name}.")

    except Exception as e:
        logging.error(f"Error processing files: {e}")
