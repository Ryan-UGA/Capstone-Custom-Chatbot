from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

import requests
from azure.core.exceptions import ServiceRequestError

def update_index(data, index_name, azure_search_endpt, azure_search_key): 
    try:
        search_client = SearchClient(endpoint=azure_search_endpt,index_name=index_name,credential=AzureKeyCredential(azure_search_key))
        search_client.upload_documents(data)
        print("Documents uploaded")
    except (requests.exceptions.SSLError, ServiceRequestError) as e:
        print(f"SSL error occurred: {e}. Retrying...")
        # raise  # Reraise to trigger retry logic found at the bottom of the script
    except Exception as e:
        print(f"Unexpected error: {e}")

def does_index_exist(index_name, azure_search_endpt, azure_search_key):
    client = SearchIndexClient(endpoint=azure_search_endpt,credential=AzureKeyCredential(azure_search_key))
    try:
        result = client.get_index(index_name)
        return True
    except ResourceNotFoundError:
        return False

def upload_single_doc(data,index_name,azure_search_endpt,azure_search_key):
    search_client = SearchClient(endpoint=azure_search_endpt, index_name=index_name, credential= AzureKeyCredential(azure_search_key))
    result = search_client.upload_documents(data)  
    print(f"Uploaded document")

def get_document_count(index_name,azure_search_endpt,azure_search_key):
    search_client = SearchClient(endpoint=azure_search_endpt, index_name=index_name, credential= AzureKeyCredential(azure_search_key))
    result = search_client.get_document_count()
    print(result)

def get_document(index_name,index_key, azure_search_endpt,azure_search_key):
    search_client = SearchClient(endpoint=azure_search_endpt, index_name=index_name, credential= AzureKeyCredential(azure_search_key))
    result = search_client.get_document(key=index_key)
    print(result)

def delete_documents_by_datasource(datasource, index_name, azure_search_endpt, azure_search_key):
    search_client = SearchClient(endpoint=azure_search_endpt, index_name=index_name, credential=AzureKeyCredential(azure_search_key))
    
    # Search for documents with the specified datasource
    results = search_client.search(search_text="", filter=f"datasource eq '{datasource}'")
    
    # Collect document keys to delete
    document_keys = [doc['key'] for doc in results]
    
    if document_keys:
        # Delete documents by keys
        delete_results = search_client.delete_documents(documents=[{"key": key} for key in document_keys])
        print(f"Deleted {len(delete_results)} documents from datasource '{datasource}'")
    else:
        print(f"No documents found for datasource '{datasource}'")    


def get_document_count_by_datasource(datasource, index_name, azure_search_endpt, azure_search_key):
    search_client = SearchClient(endpoint=azure_search_endpt, index_name=index_name, credential=AzureKeyCredential(azure_search_key))
    
    # Search for documents with the specified datasource
    results = search_client.search(search_text="", filter=f"datasource eq '{datasource}'")
    
    # Count the number of documents
    document_count = len([doc for doc in results])
    
    print(f"Found {document_count} documents for datasource '{datasource}'")

# @retry(
#     retry=retry_if_exception_type((requests.exceptions.SSLError, ServiceRequestError)),  # Retry on SSL and request errors
#     stop=stop_after_attempt(5),  # Stop after 5 attempts
#     wait=wait_exponential(multiplier=1, min=2, max=10),  # Exponential backoff
# )