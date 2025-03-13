import os
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_prompt_to_openai(messages: list[dict], system_prompt_file: str = "system_prompt.txt") -> str:
    # Get API key and model name from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")  # Default if not set
    
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    # Initialize the ChatOpenAI client with environment variables
    chat = ChatOpenAI(
        model_name=model_name,
        openai_api_key=api_key,
        temperature=0.7
    )

    # Read system prompt from file
    system_prompt_path = os.path.join(os.path.dirname(__file__), "..", system_prompt_file)
    with open(system_prompt_path, 'r') as file:
        system_prompt = file.read().strip()

    # Convert messages to the format expected by langchain_openai
    formatted_messages = [SystemMessage(content=system_prompt)]
    for msg in messages:
        if msg.role == 'user':
            formatted_messages.append(HumanMessage(content=msg.content))
        elif msg.role == 'assistant':
            formatted_messages.append(AIMessage(content=msg.content))
    response = chat.invoke(formatted_messages)
    return response.text()
