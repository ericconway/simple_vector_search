# Vector Search Project

## Introduction

The Vector Search Project is an advanced document retrieval system that utilizes vector embeddings to find relevant documents based on natural language queries. It combines Qdrant as the vector database, FastAPI for the backend API, and a simple HTML interface for user interaction. The system can ingest various document types (PDF, Word, Text, HTML) and allows users to search through them using semantic similarity.

## Getting Started - Setting up, Initializing, and Launching the App

### Prerequisites

- Docker and Docker Compose
- Git

### Setup and Launch

1. Clone the repository:
```
   git clone https://github.com/yourusername/vector-search-project.git
   cd vector-search-project
```
2. Build and start the services:
```
   docker-compose up --build -d
```
3. Initialize the Qdrant collection:
```
   docker-compose exec app python -m src.setup_qdrant
```
This will set up the necessary collection in Qdrant for storing document vectors.

## Loading Documents into the Vector DB

To load documents into the vector database:

1. Ensure your documents are in a directory accessible to the Docker container. You may need to adjust the volume mappings in docker-compose.yml if the documents are on your host machine.

2. Run the document loading script:
```
   docker-compose exec app python -m src.load_documents /path/to/your/documents
```
   Replace /path/to/your/documents with the actual path to the directory containing your documents within the Docker container.

   For example there is a folder called document_corpus in the project. This file is copied into the docker container  in the Dockerfile with the following command:
```
COPY document_corpus/ ./document_corpus/
```

So If your files to upload are in this folder...

```
   docker-compose exec app python -m src.load_documents /document_corpus
```

The script will process each file in the specified directory, create vector embeddings, and store them in the Qdrant database. You'll see logging output indicating the progress of the document loading process.

## Connecting via Web Browser

Once the application is running:

1. Open your web browser.

2. Navigate to:
```
   http://localhost:8000
   ```

3. You should see a simple search interface where you can enter queries and view results.

If you encounter a "Not Found" error, ensure that your api.py file is correctly set up to serve the static HTML file and that the file is in the correct location within your project structure.

To connect to the Fast API docs page open browser to
```
http://localhost:8000/docs
```

To connect to the Qdrant console open browser to 
```
http://localhost:6333/dashboard
```



## Monitoring the Application Logs

To monitor the logs of your application:

1. View real-time logs:
```
   docker-compose logs -f app
```
   This command will show you the most recent logs and continue to stream new log entries as they occur.

2. View the last N lines of the log:
```
   docker-compose logs --tail=100 app
```
   This shows the last 100 lines of the app service log.

3. View logs with timestamps:
```
   docker-compose logs -f --timestamps app
```
These logs will include any debug statements you've added to your Python scripts, helping you monitor the application's behavior and troubleshoot any issues.

Remember, you can adjust the logging level by modifying the LOG_LEVEL environment variable in your docker-compose.yml file or Dockerfile.