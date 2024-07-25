import os
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from a .env file

# AWS Bedrock settings
AWS_REGION = "us-west-2"  # Replace with your AWS region

# Pinecone settings
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = "us-east-1"  # Replace with your Pinecone environment
PINECONE_INDEX_NAME = "dream-interpreter-index"
PINECONE_DIMENSION = 768

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model settings
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
INSTRUCTION_MODEL = "anthropic.claude-v2"

# Data settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "dream_psychology_texts")