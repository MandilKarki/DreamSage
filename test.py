https://msty.app/
https://github.com/pdichone/ollama-fundamentals/blob/main/pdf-rag.py

https://www.promptingguide.ai/techniques/tot

microsoft/Phi-3.5-mini-instruct

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-llm-7b-base")
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-llm-7b-base")


improve exisiting tprompt anthropic console https://console.anthropic.com/dashboard


import dspy
import json

# Connect to the Ollama server
lm = dspy.LM("ollama_chat/llama3.2", api_base="http://localhost:11434", api_key="")
dspy.configure(lm=lm)

# Define the summarization task with DSPy
class Summarization(dspy.Signature):
    """
    Summarize the provided incident details into a concise yet comprehensive summary.
    Focus on:
    - What caused the incident.
    - What processes occurred (steps taken).
    - What was included (data, assets, communication).
    - Conclude with the overall summary of the incident.
    """
    text = dspy.InputField(desc="Incident details to be summarized.")
    summary = dspy.OutputField(desc="Detailed summary of the input incident details.")

# Initialize the ChainOfThought module with the Summarization signature
summarizer = dspy.ChainOfThought(Summarization)

def generate_summary(prompt, max_new_tokens=122):
    """
    Generate text using the DSPy ChainOfThought module with the detailed prompt.
    """
    return summarizer(prompt, max_new_tokens=max_new_tokens)

def main():
    # Example incident data
    incidents = [
        {
            "Incident Priority": "P3",
            "Cease & Desist": "Yes",
            "Declared Incident Indicator": "Yes",
            "Highest Classification": "Restricted",
            "Number of Records": "10–99",
            "Financial Loss – Data Protection": "Yes",
            "Data Misuse – Data Protection": "Yes",
            "Reputational Loss – Data Protection": "Yes",
            "Operations Disruption": "No",
            "Incident Types and Themes": "Personal use/information"
        },
        {
            "Incident Priority": "P4",
            "Cease & Desist": "No",
            "Declared Incident Indicator": "No",
            "Highest Classification": "Internal",
            "Number of Records": "<10",
            "Financial Loss – Data Protection": "No",
            "Data Misuse – Data Protection": "No",
            "Reputational Loss – Data Protection": "No",
            "Operations Disruption": "Yes",
            "Incident Types and Themes": "Insider Threat"
        }
    ]

    # Define the prompt format with additional context
    summary_format = """
    Executive Summary:
    Incident Priority: {Incident Priority}
    Cease & Desist: {Cease & Desist}
    Declared Incident Indicator: {Declared Incident Indicator}
    Highest Classification: {Highest Classification}
    Number of Records: {Number of Records}
    Financial Loss – Data Protection: {Financial Loss – Data Protection}
    Data Misuse – Data Protection: {Data Misuse – Data Protection}
    Reputational Loss – Data Protection: {Reputational Loss – Data Protection}
    Operations Disruption: {Operations Disruption}
    Incident Types and Themes: {Incident Types and Themes}

    Additional Context:
    - **Cause**: Identify what caused this incident (e.g., hardware failure, human error, management instructions).
    - **Process**: Describe the processes involved during the incident. What steps were taken to handle or escalate the issue?
    - **Details**: Highlight what was included in the incident (e.g., types of data, actions taken).
    - **Overall Summary**: Conclude with a detailed summary of the incident.

    Summary: {summary}
    """

    try:
        # Iterate over the incidents and generate summaries
        for incident in incidents:
            incident_details = json.dumps(incident, indent=2)
            prompt = f"{incident_details}\n{summary_format}"
            summary = generate_summary(prompt)
            formatted_summary = summary_format.format(**incident, summary=summary)
            print(formatted_summary)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()


