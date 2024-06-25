import os
import sys
import argparse
import logging
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import docx2txt
from pypdf import PdfReader
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_file(file_path):
    logger.debug(f"Reading file: {file_path}")
    _, ext = os.path.splitext(file_path)
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.docx':
        return docx2txt.process(file_path)
    elif ext == '.pdf':
        reader = PdfReader(file_path)
        return ' '.join([page.extract_text() for page in reader.pages])
    elif ext == '.html':
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.get_text()
    else:
        logger.warning(f"Unsupported file type: {ext}")
        return ''

def load_documents(directory):
    logger.info(f"Starting to load documents from directory: {directory}")
    
    qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
    qdrant_port = int(os.getenv('QDRANT_PORT', 6333))
    logger.debug(f"Connecting to Qdrant at {qdrant_host}:{qdrant_port}")
    client = QdrantClient(qdrant_host, port=qdrant_port)
    
    logger.debug("Initializing SentenceTransformer model")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    files_processed = 0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            logger.debug(f"Processing file: {file_path}")
            content = read_file(file_path)
            if content:
                logger.debug(f"Encoding content for file: {file_path}")
                embedding = model.encode(content)
                logger.debug(f"Upserting document to Qdrant: {file_path}")

                client.upsert(
                    collection_name="documents",
                    points=[{
                        "id": files_processed+1,
                        "vector": embedding.tolist(),
                        "payload": {"content": content, "file_path": file_path}
                    }]
                )
                logger.info(f"Loaded: {file_path}")
                files_processed += 1
            else:
                logger.warning(f"Skipped empty or unsupported file: {file_path}")
    
    logger.info(f"Finished loading documents. Total files processed: {files_processed}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load documents into Qdrant from a specified directory.")
    parser.add_argument("directory", help="Path to the directory containing documents to load")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        logger.error(f"The specified path is not a directory: {args.directory}")
        sys.exit(1)

    load_documents(args.directory)