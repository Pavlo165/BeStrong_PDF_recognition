import azure.functions as func
import datetime
import json
import logging
import os
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Environment variables
STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_BLOB_CONTAINER_NAME_ARCHIVE = os.getenv("AZURE_BLOB_CONTAINER_NAME_ARCHIVE")
AZURE_BLOB_CONTAINER_NAME_IMPORT = os.getenv("AZURE_BLOB_CONTAINER_NAME_IMPORT")
FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

app = func.FunctionApp()

@app.function_name(name="blob_trigger_function")
@app.blob_trigger(
    arg_name="blob",
    path=f"{AZURE_BLOB_CONTAINER_NAME_IMPORT}/{{name}}",
    connection=STORAGE_CONNECTION_STRING
)
def process_blob(blob: func.InputStream, name: str) -> None:
    logging.info(f"Blob trigger fired for file: {name}")

    # Перевірка змінних середовища
    if not all([STORAGE_CONNECTION_STRING, AZURE_BLOB_CONTAINER_NAME_ARCHIVE, FORM_RECOGNIZER_ENDPOINT, FORM_RECOGNIZER_KEY]):
        logging.error("Missing required environment variables.")
        return

    try:
        # Читання даних файлу
        pdf_data = blob.read()
        logging.info(f"Read file {name} successfully.")

        # Аналіз документа за допомогою Form Recognizer
        document_analysis_client = DocumentAnalysisClient(
            endpoint=FORM_RECOGNIZER_ENDPOINT, 
            credential=AzureKeyCredential(FORM_RECOGNIZER_KEY)
        )
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", pdf_data)
        result = poller.result()

        # Конвертація результатів у JSON
        result_json = result.to_dict()
        logging.info("Document analysis completed successfully.")

        # Формування імені файлу для архіву
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        archive_blob_name = f"{os.path.splitext(name)[0]}_{timestamp}.json"

        # Завантаження JSON до архівного контейнера
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        archive_blob_client = blob_service_client.get_blob_client(
            container=AZURE_BLOB_CONTAINER_NAME_ARCHIVE, blob=archive_blob_name
        )
        archive_blob_client.upload_blob(json.dumps(result_json), overwrite=True)
        logging.info(f"Processed file {name} and uploaded to archive as {archive_blob_name}.")

    except Exception as e:
        logging.error(f"Error processing blob {name}: {e}")
