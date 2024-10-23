from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
load_dotenv()


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "pdf-index2"

# ---------------------SETUPS-----------------------
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # OpenAI embeddings are 1536 dimensions
        metric='cosine',
        spec=ServerlessSpec(
            cloud=os.getenv("PINECONE_CLOUD", "aws"),
            region=os.getenv("PINECONE_REGION", "us-east-1")
        )
    )


"""
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "pdf-index1"

# ---------------------SETUPS-----------------------
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # OpenAI embeddings are 1536 dimensions
        metric='cosine',
        spec=ServerlessSpec(
            cloud=os.getenv("PINECONE_CLOUD", "aws"),
            region=os.getenv("PINECONE_REGION", "us-east-1")
        )
    )
    print("index", index_name)
index = pc.Index(index_name)
"""
