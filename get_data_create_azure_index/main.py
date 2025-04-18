# Our package data_processing_methods
from data_processing_methods.DataLakeConnect import get_files_from_container, process_and_append_json, get_data_lake
from data_processing_methods.DataLake2 import data_lake2_extract
from data_processing_methods.DataLake1 import data_lake1_extract
from data_processing_methods.GenerateTags import generate_tags_from_csv_column
from data_processing_methods.WarehouseConnect import ssms_connect_and_extract
from data_processing_methods.AzureSearchIndex import does_index_exist, update_index
# General Python packages
import os
import json
from dotenv import load_dotenv
import datetime

load_dotenv()

# Azure Storage Account details (connection, containers, and download folders)
AZURE_STORAGE_CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
DATA_LAKE1_CONTAINER_NAME = os.environ["DATA_LAKE1_CONTAINER_NAME"]
DATA_LAKE2_CONTAINER_NAME = os.environ["DATA_LAKE2_CONTAINER_NAME"]
# Folders/directories (DOWNLOAD_FOLDER is not used right now -> check DATALAKECONNECT.py to see how to download)
DOWNLOAD_FOLDER = os.environ["DOWNLOAD_FOLDER"]
CSV_FILE_PATH = os.environ["CSV_FILE_PATH"]
# SSMS environment variables
SSMS_QUERY_STRING = os.environ["SSMS_QUERY_STRING"]
SSMS_CONNECTION_STRING = os.environ["SSMS_CONNECTION_STRING"]
# Azure Search Index variables
AZURE_SEARCH_ENDPT = os.environ["AZURE_SEARCH_ENDPT"]
AZURE_SEARCH_KEY = os.environ["AZURE_SEARCH_KEY"]
AZURE_SEARCH_INDEX = os.environ["AZURE_SEARCH_INDEX"]

# Process each JSON-formatted data_lake1 file (HTML page that was scraped into JSON prior to this project was structured)
def process_each_json_data_lake1(json_data):
    # Open the format file
    with open("format.json", "r", encoding="utf-8") as format_file:
        format = json.load(format_file)
    data_lake1_output = data_lake1_extract(json_data,format)
    data_lake1_output["tags"] = generate_tags_from_csv_column(CSV_FILE_PATH, data_lake1_output)
    return data_lake1_output

# Process each JSON-formatted data lake2 file (HTML page that was scraped into JSON prior to this project was structured)
def process_each_json_data_lake2(json_data):
    with open("format.json", "r", encoding="utf-8") as format_file:
        format = json.load(format_file)
    data_lake2_output = data_lake2_extract(json_data, format)
    data_lake2_output["tags"] = generate_tags_from_csv_column(CSV_FILE_PATH, data_lake2_output)
    return data_lake2_output

def convert_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    
def split_into_batches(json_array, max_batch_size): # splits list/array of JSON objects into batches with max_batch_size
    return [json_array[i:i + max_batch_size] for i in range(0, len(json_array), max_batch_size)]

def main():
    ####################################### Data Retrieval, Processing, and Extraction #######################################
    # Initialize variables that will be coded
    data_lake = []
    warehouse = []
    all_data = []
    # Data Lake - data_lake1 logic
    data_lake1_container_client = get_files_from_container(AZURE_STORAGE_CONNECTION_STRING, DATA_LAKE1_CONTAINER_NAME)
    process_and_append_json(data_lake1_container_client, process_each_json_data_lake1)
    # Data Lake - DataLake2 Logic
    data_lake2_container_client = get_files_from_container(AZURE_STORAGE_CONNECTION_STRING, DATA_LAKE2_CONTAINER_NAME)
    process_and_append_json(data_lake2_container_client, process_each_json_data_lake2)
    # Data Lake logic
    data_lake = get_data_lake()
    # # Data Warehouse logic
    with open("format.json", "r", encoding="utf-8") as format_file:
        format = json.load(format_file)
    warehouse = ssms_connect_and_extract(SSMS_QUERY_STRING, SSMS_CONNECTION_STRING, format)
    # Combine the data lake and datawarehouse for the Azure Search Index upload
    all_data = data_lake + warehouse

    # Add a key to every object (required for the Azure Search Index)
    for i, obj in enumerate(all_data):
        obj["key"] = str(i)
        # print each object in all_data, a list of JSON objects
        # print("Next object")
        # print(obj)
        # print()
    ####################################### Batch Processing and Search Index Upload #######################################
    # Check if index exists
    if does_index_exist(AZURE_SEARCH_INDEX, AZURE_SEARCH_ENDPT, AZURE_SEARCH_KEY):
        # IndexDocumentsActionCountExceeded Error forces us to upload in batches (if error persists -> lower max batch size)
        max_batch_size = 30000
        batched_data = split_into_batches(all_data,max_batch_size)
        print(f"all_data has {len(all_data)} records. batched_data has {len(batched_data)} batches with a max batch size of {max_batch_size}.")
        # Printing each batch to ensure uniqueness and correct batch sizing
        for array in batched_data:
            print("New array below")
            print(len(array))
            print(json.dumps(array[0],indent=5, default=convert_datetime))
            print()
            print(json.dumps(array[-1],indent=5, default=convert_datetime))
            print()
        print(f"index named {AZURE_SEARCH_INDEX} exists. Beginning the upload of all batches now.")
        # Update Azure Search Index with each batch (batch is an array of JSONS)
        for batch in batched_data:
            update_index(batch, AZURE_SEARCH_INDEX, AZURE_SEARCH_ENDPT, AZURE_SEARCH_KEY)
        print(f"index {AZURE_SEARCH_INDEX} has been updated.")
    else:
        return(f"{AZURE_SEARCH_INDEX} does not exist and was not updated with given parameters.")

if __name__ == "__main__":
    main()
    print("Main done")
