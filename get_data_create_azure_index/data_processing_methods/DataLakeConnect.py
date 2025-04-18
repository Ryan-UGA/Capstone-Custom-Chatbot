from azure.storage.blob import BlobServiceClient
import os
import json

data_lake = []

def get_data_lake():
    return data_lake

def get_files_from_container(azure_storage_connection_string:str, container_name:str):
    try:
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
        # Get container client
        container_client = blob_service_client.get_container_client(container_name)
        # Apply methods to the files/blobs in the container_client -> could start with -> for blob in container_client.list_blobs(): blob_name = blob.name ...
        return container_client

    except Exception as e:
        print(f"Error: {e}")

def process_and_append_json(container_client:str, process_json): #download_folder:str parameter is needed if downloading files
    try:
        # # Ensure the local download folder exists
        # if not os.path.exists(download_folder):
        #     os.makedirs(download_folder)
        #     print(f"Created download folder: {download_folder}")
        # List and process/download files
        for blob in container_client.list_blobs():
            blob_name = blob.name
            # download_path = os.path.join(download_folder, blob_name)

            print(f"Processing {blob_name}...")

            # Read the file content
            blob_data = container_client.download_blob(blob_name).readall().decode("utf-8")

            # Ensure JSON is properly parsed
            try:
                json_data = json.loads(blob_data)  # Convert string to dictionary
            except json.JSONDecodeError:
                print(f"Skipping {blob_name}: Not a valid JSON file.")
                continue  # Skip non-JSON files

            # Apply processing to JSON content
            json_data = process_json(json_data) 

            # Append this JSON to the array_of_jsons for final upload
            data_lake.append(json_data)
            
            # if downloading -> modified_data = process_json(json_data)

            # # Save the processed file as JSON
            # with open(download_path, "w", encoding="utf-8") as download_file:
            #     json.dump(modified_data, download_file, indent=4)
            # print(f"json dump to {download_path}) complete.")

        print("All files processed and downloaded successfully!")

    except Exception as e:
        print(f"Error: {e}")
