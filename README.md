# Capstone Internal Chatbot Referencing an Azure Search Index

## Project Overview
### PROBLEM
Information is often scattered across data sources, making it time-consuming and difficult for users manually searching for information.
### SOLUTION
Users can quickly retrieve needed information; users prompt this chatbot which responds with information and a citation - where the information originated from. It provides a URL and article title for the data lake records; if there is no link (i.e. structured data in SQL query), then, instead of a link, all data tied to the observation in the search index is provided as the citation.

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

We did not have time to tune the LLM, but everything else was completed within a few months. The .env.sample file from the Microsoft repo provides some environment variables that would tune the LLM such as lower temperature and top p. Lower temperature makes output more data-specific and focused while higher temperature makes it more diverse and creative; top p limits the number of choices and helps avoid overly diverse outputs.

## Directories
### get_data_create_azure_index (original code)
* The process involved data retrieval, extraction, and normalization then batch processing when uploading to the Azure Search index. The process was mapped as seen in the image below:
  ![image](https://github.com/user-attachments/assets/b71214e0-ef34-488f-a6fc-354f17881198)
#### Data Retrieval and Extraction From Data Lake and Data Warehouse
Clean, extract, and normalize the data from a data lake and data warehouse
| Data Lake | Data Warehouse |
|:---------|:---------|
| semi-structured HTML-scraped JSON files | structured information from a table in a database |
| [Azure Storage Explorer](https://learn.microsoft.com/en-us/azure/storage/storage-explorer/vs-azure-tools-storage-explorer-blobs) | SQL Server Management Studio or [SSMS](https://learn.microsoft.com/en-us/ssms/sql-server-management-studio-ssms) |
#### Upload Batches of Data to the Azure Search Index
Normalize and index the data to enable efficient RAG (better data quality = better chatbot results).

### sample-app-aoai-chatGPT
The web app was originally cloned from this Microsoft github repo called [sample-app-aoai-chatGPT](https://github.com/microsoft/sample-app-aoai-chatGPT) and then integrated keys, endpoints, and other necessary information found in the repo in the .env file (read technical details -> environment variables section later).

## Capstone Contributors
* Ryan Cullen [@Ryan-UGA](https://github.com/Ryan-UGA)
* Fan Yuan [@Fan36466](https://github.com/Fan36466)
* Nate Moore [@NateM2025](https://github.com/NateM2025)
* Katie Gerrick
* Graham Luckey
* Destinee Pruden [@DPRUDEN25](https://github.com/DPRUDEN25)

## Technical Details

### Setup Instructions and Pre-Requisite Installations 
#### Restart Visual Studio Code or the editor you use after the below installations if the same error persists

![image](https://github.com/user-attachments/assets/96226978-09bd-46c3-9fae-afcc7309e9f9)

* Have [Python](https://www.python.org/) and [git](https://git-scm.com/downloads/win) installed (I installed the latest 64-bit version of Git for Windows).
* Command prompt (change directory): cd absolute/path/to/directory/storing/code
* Command prompt (getting code from git): git clone https://... (look at picture below)
  ![image](https://github.com/user-attachments/assets/3501713c-2986-4905-adfc-9de1c79a79bb)

* Edit the .env file in same directory as .env.sample (look at next section): AUTH_ENABLED = “False” right now, but definitely add authentication to the app when put into production (look at Microsoft repo for Authentication information).
* Download [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/), run the .exe file, and add the individual components in the picture below (Windows 10 or 11 is fine depending on your computer).
![image](https://github.com/user-attachments/assets/4c189735-b4d9-45e0-8fa2-f391c102bd50)

* Download [Node.js with NPM](https://nodejs.org/en/download/) (Windows Installer (.msi) for the prebuilt Node.js for Windows running a x64 architecture with NPM)
* Terminal (used VS Code): pip install -r requirements.txt
* Terminal: python -m pip install –upgrade python-certifi-win32
* Terminal: set PYTHONHTTPSVERIFY=0

### Terminal: .\start.cmd will load the web interface in the browser (Normal to Refresh Browser if 127… isn’t found)

### Terminal: Ctrl-c then Y in the terminal will stop the application

### Environment Variables 
#### AUTH_ENABLED="False" on local machine, but add Authentication (look at Microsoft repo's README file for tutorials/information)
#### Azure OpenAI model
* AZURE_OPENAI_ENDPOINT: Overview tab
* AZURE_OPENAI_MODEL: top of Overview tab -> Go to Azure AI Foundry Portal -> Deployments tab -> Deploy model
* AZURE_OPENAI_KEY: Overview tab
#### Mandatory variable from Microsoft repo's README.md
* DATASOURCE_TYPE = “AzureCognitiveSearch”
#### Azure AI Search Index
* AZURE_SEARCH_SERVICE: name of the search service
* AZURE_SEARCH_INDEX: Navigate to the name of the search service -> Search management tab -> Indexes tab -> Name
* AZURE_SEARCH_KEY: Navigate to the AZURE_SEARCH_SERVICE -> Settings tab -> Keys tab -> we chose Primary admin key
#### CosmosDB for chat history
* AZURE_COSMOSDB_ACCOUNT: name of Azure CosmosDB account
* AZURE_COSMOSDB_DATABASE: navigate to the name of CosmosDB account -> Containers tab -> Settings -> container
* AZURE_COSMOSDB_CONVERSATIONS_CONTAINER: container inside AZURE_COSMOSDB_DATABASE
* AZURE_COSMOSDB_ACCOUNT_KEY: navigate to the name of CosmosDB account -> Settings tab -> Keys tab -> we chose the Primary key
* AZURE_COSMOSDB_ENABLE_FEEDBACK: we set to "False"
#### User Interface Customization
* UI_TITLE: title of the web app (top left)
* UI_LOGO: copy link address of image
* UI_CHAT_LOGO: copy link address of image
* UI_CHAT_TITLE: title of gpt (middle of interface above the description)
* UI_CHAT_DESCRIPTION: some description of what this web app does
#### Recommended for nice-looking responses to the user
* SANITIZE_ANSWER = “True”

### Helpful Links
* [Azure Storage Explorer](https://learn.microsoft.com/en-us/azure/storage/blobs/)
* [Structured vs. Unstructured Data](https://k21academy.com/microsoft-azure/dp-900/structured-data-vs-unstructured-data-vs-semi-structured-data/)
* [Azure AI Search (previously known as Cognitive Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
* [Azure AI Services](https://learn.microsoft.com/en-us/azure/ai-services/what-are-ai-services)
* [Retrieval Augmentation Generation (RAG)](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
* [Microsoft Chatbot Repo](https://github.com/microsoft/sample-app-aoai-chatGPT)
* [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/overview)
* [Azure CosmosDB](https://learn.microsoft.com/en-us/azure/cosmos-db/introduction)
* [Azure Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
