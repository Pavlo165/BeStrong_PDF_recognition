import azure.functions as func
import datetime
import json
import logging
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.storage.fileshare import ShareFileClient

STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
SHARE_NAME = os.getenv("AZURE_FILE_SHARE_NAME")
FILE_PATH = os.getenv("AZURE_FILE_PATH")
BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME")
FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

app = func.FunctionApp()

@app.function_name(name="mytimer")
@app.timer_trigger(schedule="*/30 * * * * *", 
              arg_name="mytimer",
              run_on_startup=True)
def test_function(mytimer: func.TimerRequest) -> None:
    print("VSE OK")

    try:
        # Download PDF from Azure File Share
        file_client = ShareFileClient.from_connection_string(STORAGE_CONNECTION_STRING, share_name=SHARE_NAME, file_path=FILE_PATH)
        pdf_data = file_client.download_file().readall()
        print("file download successfully")
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")