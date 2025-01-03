import logging
import os
import json
import azure.functions as func
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
# from azure.storage.fileshare import ShareFileClient
# from azure.ai.formrecognizer import DocumentAnalysisClient
# from azure.core.credentials import AzureKeyCredential

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


    # try:
    #     # Download PDF from Azure File Share
    #     file_client = ShareFileClient.from_connection_string(STORAGE_CONNECTION_STRING, share_name=SHARE_NAME, file_path=FILE_PATH)
    #     pdf_data = file_client.download_file().readall()

    #     # Send PDF to Azure AI Document Intelligence
    #     document_analysis_client = DocumentAnalysisClient(endpoint=FORM_RECOGNIZER_ENDPOINT, credential=AzureKeyCredential(FORM_RECOGNIZER_KEY))
    #     poller = document_analysis_client.begin_analyze_document("prebuilt-document", pdf_data)
    #     result = poller.result()

    #     # Convert result to JSON
    #     result_json = result.to_dict()

    #     # Upload JSON to Azure Blob Storage
    #     blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
    #     blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=os.path.basename(FILE_PATH) + ".json")
    #     blob_client.upload_blob(json.dumps(result_json), overwrite=True)
    #     logging.info("PDF processed and JSON uploaded successfully.")
    # except Exception as e:
    #     logging.error(f"Error processing PDF: {e}")