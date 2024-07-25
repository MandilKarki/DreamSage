from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
from src.config.settings import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME

# ... rest of the file remains the same
from src.config.settings import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME

def init_pinecone():
    return PineconeClient(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

def get_or_create_index(embeddings):
    pc = init_pinecone()
    
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=len(embeddings.embed_query("test")),
            metric="cosine"
        )
    
    return Pinecone.from_existing_index(PINECONE_INDEX_NAME, embeddings)