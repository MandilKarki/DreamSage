import uuid
from openai import OpenAI
from langsmith import traceable
from langchain_community.vectorstores import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.config.settings import PINECONE_INDEX_NAME, EMBEDDING_MODEL, OPENAI_API_KEY, PINECONE_DIMENSION
from src.storage.pinecone_utils import init_pinecone

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

@traceable(run_type="retriever")
def retriever(query: str):
    # This is where you'd implement your actual retrieval logic
    # For now, we'll just return a mock result
    results = ["Dreams often symbolize our subconscious thoughts and emotions"]
    return results

class DreamInterpreter:
    def __init__(self):
        pc = init_pinecone()
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        
        self.vectorstore = Pinecone.from_existing_index(PINECONE_INDEX_NAME, embeddings)
        
        llm = ChatOpenAI(
            temperature=0.7, 
            model_name="gpt-3.5-turbo",
            openai_api_key=OPENAI_API_KEY
        )
        
        template = """You are a knowledgeable dream interpreter. Use the following pieces of context to interpret the dream. If you're unsure, say that you're not certain but offer a possible interpretation.

Context: {context}

Dream: {question}

Interpretation:"""

        prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

    @traceable(metadata={"llm": "gpt-3.5-turbo"})
    def interpret_dream(self, dream_description, user_id=None):
        run_id = str(uuid.uuid4())
        
        docs = retriever(dream_description)
        result = self.qa_chain.invoke(
            {"query": dream_description},
            config={"metadata": {"user_id": user_id} if user_id else {}}
        )
        
        interpretation = result['result']
        sources = [doc.page_content for doc in result['source_documents']]
        
        return interpretation, sources, run_id

    def run_interactive_session(self):
        print("Dream Interpreter is ready!")
        
        while True:
            dream = input("\nDescribe your dream (or type 'quit' to exit): ")
            if dream.lower() == 'quit':
                break
            
            user_id = input("Enter your user ID (or press enter to skip): ")
            
            print("Interpreting your dream...")
            try:
                interpretation, sources, run_id = self.interpret_dream(dream, user_id if user_id else None)
                
                print("\nDream Interpretation:")
                print(interpretation)
                
                print("\nSources:")
                for i, source in enumerate(sources, 1):
                    print(f"Source {i}: {source[:200]}...")  # Print first 200 characters of each source
                
                print(f"\nRun ID: {run_id}")
                
                feedback = input("Was this interpretation helpful? (y/n): ")
                if feedback.lower() == 'y':
                    self.log_feedback(run_id, 1.0)
                elif feedback.lower() == 'n':
                    self.log_feedback(run_id, 0.0)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            
            print("\n")

    def log_feedback(self, run_id, score):
        from langsmith import Client
        ls_client = Client()
        ls_client.create_feedback(
            run_id,
            key="user-score",
            score=score,
        )

    def get_qa_chain(self):
        return self.qa_chain