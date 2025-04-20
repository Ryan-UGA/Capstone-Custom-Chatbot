# Capstone Custom Internal Chatbot Referencing an Azure Search Index

## Project Overview (data warehouse and data lake table in appendix here as well)
### PROBLEM
Information is often scattered across data sources, making it time-consuming and difficult for users manually searching for information.
### SOLUTION
Users can quickly retrieve needed information; users prompt this chatbot which responds with information and a citation - where the information originated from. It provides a URL and article title for the HTML-scraped JSON files; if there is no link (i.e. structured data in SQL query), then all data tied to the observation in the search index is provided as the citation.
### Software Involved
This web application serves as an interface hosting a LLM (Large Language Model) that utilizes RAG or [Retrieval Augmented Generation](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview?tabs=docs). [The Azure OpenAI service](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search) used the gpt-4o model and references an Azure Search Index storing normalized data from a variety of sources.

The picture below diagrams the software involved. The Python diagrammed is the data processing pipelines in the get_data_create_azure_index directory explained later. The sample-app-aoai-chatGPT directory currently has the webapp, Azure OpenAI gpt-4o model, Azure AI Search Index, and Azure CosmosDB (for chat history), but feel free to look at the Microsoft repository named [sample-app-aoai-chatGPT](https://github.com/microsoft/sample-app-aoai-chatGPT) for more information and potential software to include.

![image](https://github.com/user-attachments/assets/54764883-d5ef-4bad-8ea8-c3c255b088da)

* Azure AI Search Index: stored cleaned, extracted, and normalized batches of data which enables efficient RAG
* Azure Open AI: deployed the gpt-4o model
* Azure CosmosDB: stored users' chat history with the web app
* Application Insights (not included now, but could be added later): Application Performance Management (APM) for live web apps
* Key Vault (not included now, but could be added later): stores important information such as keys and endpoints in this project

## Project Phases
![image](https://github.com/user-attachments/assets/95d544c2-ed0d-4cee-8eab-41635c6c6597)

We did not have time to tune the LLM, but everything else was completed within a few months.

## Directories
### get_data_create_azure_index (original code)
* The process involved data retrieval, extraction, and normalization then batch processing when uploading to the Azure Search index. The process was mapped as seen in the image below:
  ![image](https://github.com/user-attachments/assets/b71214e0-ef34-488f-a6fc-354f17881198)
#### Data Retrieval and Extraction From Data Lake and Data Warehouse
Clean, extract, and normalize the data from a data lake ((Azure Storage Explorer)[https://learn.microsoft.com/en-us/azure/storage/storage-explorer/vs-azure-tools-storage-explorer-blobs] storing semi-structured or un-structured web-scraped JSON files) and data warehouse ((SQL Server Management Studio or [SSMS](https://learn.microsoft.com/en-us/ssms/sql-server-management-studio-ssms) storing structured tables, etc.)
#### Upload Batches of Data to the Azure Search Index
Normalize and index the data to enable efficient RAG (better data quality = better chatbot results).

### sample-app-aoai-chatGPT
The web app was originally cloned from this Microsoft github repo called [sample-app-aoai-chatGPT](https://github.com/microsoft/sample-app-aoai-chatGPT). I then integrated keys, endpoints, and other necessary information found in the repo. My .env file has what variables I used (and read technical details for information on those variables), but feel free to add more from the .env.sample file in the Microsoft repo.

## Capstone Contributors
* Ryan Cullen [@Ryan-UGA](https://github.com/Ryan-UGA)
* Fan Yuan [@Fan36466](https://github.com/Fan36466)
* Nate Moore [@NateM2025](https://github.com/NateM2025)
* Katie Gerrick
* Graham Luckey
* Destinee Pruden

## Technical Details

### Setup Instructions and Pre-Requisite Installations

### Environment Variables

### Helpful Links

### Possible Future Work 






