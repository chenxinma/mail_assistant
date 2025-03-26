import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

import chromadb
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from log_config import setup_logging

logger = setup_logging(__name__)

# Initialize FastMCP server
server = FastMCP("fsg_project_assistant")
# Global variables
_chroma_client = None


def get_chroma_client():
    """Get or create the global Chroma client instance."""
    global _chroma_client
    if _chroma_client is None:
        load_dotenv()
        chroma_host = os.getenv('CHROMA_HOST', '')
        chroma_port = int(os.getenv('CHROMA_PORT', '0'))

        _chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        print("chroma_client", chroma_host, ":", chroma_port)

    return _chroma_client

@server.tool()
async def query_documents(
    query_texts: List[str],
    n_results: int = 5,
    where: Optional[Dict] = None,
    where_document: Optional[Dict] = None,
    include: Optional[List[str]] = None) -> List:
    """Query documents from a Chroma collection with advanced filtering.
    
    Args:
        query_texts: List of query texts to search for
        n_results: Number of results to return per query
        where: Optional metadata filters using Chroma's query operators
               Examples:
               - Simple equality: {"metadata_field": "value"}
               - Comparison: {"metadata_field": {"$gt": 5}}
               - Logical AND: {"$and": [{"field1": {"$eq": "value1"}}, {"field2": {"$gt": 5}}]}
               - Logical OR: {"$or": [{"field1": {"$eq": "value1"}}, {"field1": {"$eq": "value2"}}]}
        where_document: Optional document content filters
        include: Optional list of what to include in response. Can contain any of:
                ["documents", "embeddings", "metadatas", "distances"]
    """
    logger.info("Querying documents with parameters: %s", locals())
    load_dotenv()
    collection_name = os.getenv('CHROMA_COLLECTION_NAME', '')

    client = get_chroma_client()
    logger.info("Using collection: %s", collection_name)
    collection = client.get_collection(collection_name)
    
    result = collection.query(
        query_texts=query_texts,
        n_results=n_results,
        # where=where,
        where_document=where_document,
        include=["documents"] # pyright: ignore
    ) # pyright: ignore
    return result["documents"] # pyright: ignore


if __name__ == "__main__":
    logger.info("Starting FastMCP server...")
    # Initialize and run the server
    server.run()
