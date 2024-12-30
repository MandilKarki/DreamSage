import dspy

# Connect to the Ollama server
lm = dspy.LM('ollama_chat/llama3.2:1b', api_base='http://localhost:11434', api_key='')

# Configure DSPy with the language model
dspy.configure(lm=lm)

class Summarization(dspy.Signature):
    """Summarize the provided text into a concise summary."""
    text = dspy.InputField()
    summary = dspy.OutputField(desc="A concise summary of the input text.")


# Initialize the ChainOfThought module with the Summarization signature
summarizer = dspy.ChainOfThought(Summarization)

# Example text to summarize
text_to_summarize = """
Artificial Intelligence (AI) has been transforming various industries, from healthcare to finance.
It enables machines to learn from data and make decisions. Applications of AI include image recognition,
natural language processing, robotics, and autonomous vehicles. The technology continues to evolve,
bringing new opportunities and challenges. As organizations embrace AI, ethical considerations and 
regulations are becoming increasingly important to ensure responsible use.
"""

# Generate the summary
result = summarizer(text=text_to_summarize)

# Access and print the summary
print("Summary:", result.summary)
