# Capstone Custom Internal Chatbot Referencing an Azure Search Index

## Project Overview (data warehouse and data lake table in appendix here as well)
* PROBLEM: Information is often scattered across data sources, making it time-consuming and difficult for users manually searching for information.
* SOLUTION: Users can quickly retrieve needed information; users prompt this chatbot that responds with information and a link where the information was found.
* DESCRIPTION: This web application serves as an interface hosting a LLM (Large Language Model) that utilizes RAG [Retrieval Augmented Generation](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview?tabs=docs). [The Azure OpenAI service](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search) used the gpt-4o model and references an Azure Search Index storing normalized data from a variety of sources.


## Project Phases
![image](https://github.com/user-attachments/assets/95d544c2-ed0d-4cee-8eab-41635c6c6597)

## Directories
### get_data_create_azure_index (original code)
* Process mapping as seen in the image below
  ![image](https://github.com/user-attachments/assets/b71214e0-ef34-488f-a6fc-354f17881198)
#### Data Retrieval and Extraction From Data Lake and Data Warehouse
Clean, extract, and normalize the data from a data lake ((Azure Storage Explorer)[https://learn.microsoft.com/en-us/azure/storage/storage-explorer/vs-azure-tools-storage-explorer-blobs] storing semi-structured or un-structured web-scraped JSON files) and data warehouse ((SQL Server Management Studio or SSMS)[https://learn.microsoft.com/en-us/ssms/sql-server-management-studio-ssms] storing structured tables, etc.)
#### Upload Batches of Data to the Azure Search Index
Normalize and index the data to enable efficient RAG (better data quality = better chatbot results)

## Capstone Contributors

## Technical Details

### Setup Instructions and Pre-Requisite Installations

### Environment Variables

### Helpful Links

### Possible Future Work 






