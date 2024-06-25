# src/setup_qdrant.py
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models

def setup_qdrant():
    qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
    qdrant_port = int(os.getenv('QDRANT_PORT', 6333))
    
    client = QdrantClient(qdrant_host, port=qdrant_port)
    
    # Create a collection for our documents
    client.create_collection(
        collection_name="documents",
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
    )
    
    print("Qdrant collection 'documents' created successfully.")

if __name__ == "__main__":
    setup_qdrant()