# Install necessary libraries
# Uncomment and run if libraries are not already installed
# !pip install langchain transformers

from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load the Flan-T5 model directly from Hugging Face
model_name = "google/flan-t5-large"  # Using Flan-T5 as an example model; adjust as needed.
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Define a function to generate text using the model directly
def generate_text(prompt, max_new_tokens=100):
    """
    Generates a response based on the input prompt using the Hugging Face model directly.

    Parameters:
        prompt (str): The input prompt to the model.
        max_new_tokens (int): Maximum number of new tokens to generate in the output.

    Returns:
        str: The generated text response.
    """
    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate output using the model with specific parameters
    output = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        num_beams=5,  # Use beam search to improve generation quality
        early_stopping=True
    )
    
    # Decode the generated tokens into a readable string
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Define the LangChain class to use this direct generation function
class DirectLLM:
    """
    Wrapper class to integrate the Hugging Face model directly with LangChain.
    """
    def __init__(self, generate_fn):
        self.generate_fn = generate_fn

    def __call__(self, prompt):
        return self.generate_fn(prompt)

# Instantiate the custom LLM for LangChain with the direct model function
hugging_face_llm = DirectLLM(generate_text)

# Define prompt templates for cybersecurity-related tasks
qa_prompt = PromptTemplate(
    input_variables=["question"],
    template="In the context of cybersecurity, provide a detailed answer to the following question. "
             "Include examples, tools, and potential challenges: {question}"
)

summarize_prompt = PromptTemplate(
    input_variables=["content"],
    template="Summarize the following cybersecurity-related content, focusing on the key risks, "
             "benefits, and implications: {content}"
)

idea_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Generate a list of innovative AI applications in cybersecurity based on the following topic. "
             "Include real-world examples and potential challenges: {topic}"
)

# Set up memory for conversation context
memory = ConversationBufferMemory()

# Create LangChain chains for each task with detailed comments
# Q&A Chain
qa_chain = LLMChain(
    llm=hugging_face_llm,
    prompt=qa_prompt,
    memory=memory
)

# Summarization Chain
summarize_chain = LLMChain(
    llm=hugging_face_llm,
    prompt=summarize_prompt
)

# Idea Generation Chain
idea_chain = LLMChain(
    llm=hugging_face_llm,
    prompt=idea_prompt
)

# Combine all chains into a sequential chain for a full workflow
sequential_chain = SequentialChain(
    chains=[qa_chain, summarize_chain, idea_chain],
    input_variables=["question", "content", "topic"],
    output_variables=["answer", "summary", "ideas"]
)

# Sample inputs for the sequential chain
inputs = {
    "question": "What are the main challenges in using AI for real-time cybersecurity threat detection?",
    "content": "AI has revolutionized cybersecurity through its applications in real-time threat detection. It uses machine learning models, anomaly detection, and natural language processing to monitor traffic, detect malicious activities, and respond to threats faster than human operators. However, challenges such as data quality, false positives, model adaptability, and real-time processing limitations remain.",
    "topic": "Potential of AI-driven anomaly detection in cybersecurity"
}

# Run the sequential chain and display outputs
outputs = sequential_chain(inputs)
print("Question-Answering Output:", outputs['answer'])
print("Summarization Output:", outputs['summary'])
print("Idea Generation Output:", outputs['ideas'])
