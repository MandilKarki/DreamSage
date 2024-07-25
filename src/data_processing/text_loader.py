# import os
# import PyPDF2
# from src.config.settings import DATA_DIR

# def load_text_files():
#     texts = []
#     print(f"Looking for files in: {DATA_DIR}")
    
#     if not os.path.exists(DATA_DIR):
#         print(f"Error: Directory {DATA_DIR} does not exist.")
#         return texts

#     for filename in os.listdir(DATA_DIR):
#         file_path = os.path.join(DATA_DIR, filename)
#         print(f"Processing file: {filename}")
        
#         if filename.endswith(".txt"):
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 texts.append(file.read())
#         elif filename.endswith(".pdf"):
#             try:
#                 with open(file_path, 'rb') as file:
#                     pdf_reader = PyPDF2.PdfReader(file)
#                     text = ""
#                     for page in pdf_reader.pages:
#                         text += page.extract_text() or ""
#                     if text:
#                         texts.append(text)
#                         print(f"Extracted {len(text)} characters from {filename}")
#                         print(f"Sample text: {text[:200]}...")  # Print first 200 characters
#                     else:
#                         print(f"Warning: No text extracted from {filename}")
#             except Exception as e:
#                 print(f"Error processing {filename}: {str(e)}")
#         else:
#             print(f"Skipping unsupported file: {filename}")
    
#     print(f"Total files processed: {len(texts)}")
#     return texts

# def get_text_chunks(texts, chunk_size=1000):
#     chunks = []
#     for text in texts:
#         chunks.extend([text[i:i+chunk_size] for i in range(0, len(text), chunk_size)])
#     return chunks


from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config.settings import DATA_DIR

def load_and_split_documents():
    loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf")
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks