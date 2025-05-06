"""
Module for making API requests to LLM services for paper grammar correction.
"""
import os
from openai import OpenAI

def ask(content):
    """
    Send a prompt to the LLM API and return the response.
    
    Args:
        content (str): The content to send to the LLM API
        
    Returns:
        str: The response from the LLM API
    """
    # Get environment variables
    api_key = os.environ.get("API_KEY")
    base_url = os.environ.get("BASE_URL")
    model = os.environ.get("MODEL")
    
    # Create OpenAI client
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Make API request
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": content},
        ],
        stream=False
    )
    
    # Return the content from the response
    return response.choices[0].message.content
