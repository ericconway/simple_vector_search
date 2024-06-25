# api.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
qdrant_port = int(os.getenv('QDRANT_PORT', 6333))
client = QdrantClient(qdrant_host, port=qdrant_port)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
          
class Query(BaseModel):
    prompt: str


@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.post("/search")
async def search(query: Query):
    try:
        logger.debug(f"Received search query: {query.prompt}")
        vector = model.encode(query.prompt).tolist()
        logger.debug("Encoded query to vector")

        results = client.search(
            collection_name="documents",
            query_vector=vector,
            limit=5
        )
        logger.debug(f"Received {len(results)} results from Qdrant")

        return [
            {
                "file_path": hit.payload["file_path"],
                "content": hit.payload["content"][:200] + "...",  # Return first 200 characters
                "score": hit.score
            }
            for hit in results
        ]
    except Exception as e:
        logger.error(f"Error during search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting the FastAPI application")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)