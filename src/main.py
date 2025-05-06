"""
Main program for automatically correcting grammar errors in academic papers.
"""
import os
import glob
import sys
import time
import re
from pathlib import Path
from tqdm import tqdm

from ask import ask


def clean_response(text):
    """
    Clean up API response by removing surrounding backticks if present.
    
    Args:
        text (str): The raw response from the API
        
    Returns:
        str: Cleaned response with backticks removed if present
    """
    # Strip whitespace first
    text = text.strip()
    
    # Check if text starts and ends with triple backticks
    if text.startswith('```') and text.endswith('```'):
        # Remove the backticks at the beginning and end
        text = text[3:len(text)-3].strip()
        
        # If there's a language identifier after the opening backticks (like ```python),
        # we need to remove the first line
        lines = text.split('\n', 1)
        if len(lines) > 1 and not lines[0].strip():
            text = lines[1].strip()
    
    return text

def main():
    # Find input files
    input_files = glob.glob(os.path.join("files", "input.*"))
    
    # Check if there's exactly one input file
    if len(input_files) != 1:
        print(f"Error: There should be exactly one input.* file in the files directory. Found {len(input_files)}.")
        sys.exit(1)
    
    input_file = input_files[0]
    input_file_name = os.path.basename(input_file)
    file_extension = os.path.splitext(input_file_name)[1]
    output_file = os.path.join("files", f"output{file_extension}")
    
    # Get environment variables
    base_url = os.environ.get("BASE_URL", "")
    model = os.environ.get("MODEL", "")
    api_key = os.environ.get("API_KEY", "")
    max_char = int(os.environ.get("MAX_CHAR", "2048"))
    
    # Print configuration
    print(f"Input file: {input_file_name}")
    print(f"BASE_URL: {base_url}")
    print(f"MODEL: {model}")
    print(f"MAX_CHAR: {max_char}")
    
    # Check if API_KEY is set
    if api_key == "DeepSeek-API-Key":
        print("Error: API_KEY is not set. Please set your DeepSeek API Key in start.bat.")
        sys.exit(1)
    else:
        print("API_KEY: Set")
        input("Press Enter to continue...")
    
    # Read the prompt template
    with open(os.path.join("prompt", "prompt.txt"), "r", encoding="utf-8") as f:
        prompt_template = f.read()
    
    # Process the input file in chunks
    with open(input_file, "r", encoding="utf-8") as f:
        input_content = f.readlines()
    
    # Pre-determine chunks
    chunks = []
    current_chunk = []
    current_chunk_size = 0
    
    # Divide input content into chunks
    for line in input_content:
        line_size = len(line)
        
        # If adding this line would exceed MAX_CHAR, finalize the current chunk
        if current_chunk and current_chunk_size + line_size > max_char:
            chunks.append((current_chunk, current_chunk_size))
            
            # Start a new chunk with the current line
            current_chunk = [line]
            current_chunk_size = line_size
        else:
            # Add line to current chunk
            current_chunk.append(line)
            current_chunk_size += line_size
            
            # Special case for the first line if it's already bigger than MAX_CHAR
            if len(current_chunk) == 1 and current_chunk_size > max_char:
                chunks.append((current_chunk, current_chunk_size))
                
                # Reset for the next chunk
                current_chunk = []
                current_chunk_size = 0
    
    # Add any remaining content as the final chunk
    if current_chunk:
        chunks.append((current_chunk, current_chunk_size))
    
    # Display information about the chunks
    print(f"Paper divided into {len(chunks)} chunks for processing.")
    
    # Process all chunks with progress bar
    all_responses = []
    for chunk_data, chunk_size in tqdm(chunks, desc="Processing paper chunks", unit="chunk"):
        chunk_text = "".join(chunk_data)
        prompt = prompt_template.replace("[content]", chunk_text)
        
        # Add retry logic for API calls
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                response = ask(prompt)
                # Clean the response by removing backticks if present
                cleaned_response = clean_response(response)
                all_responses.append(cleaned_response)
                break  # Success, exit the retry loop
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"\nError: Failed to process chunk after {max_retries} attempts. Last error: {str(e)}")
                    sys.exit(1)  # Exit with error
                else:
                    print(f"\nAPI call failed (attempt {retry_count}/{max_retries}). Waiting 3 seconds before retrying... Error: {str(e)}")
                    time.sleep(3)  # Wait 3 seconds before retry
    
    # Combine all responses and write to output file
    combined_response = "\n".join(all_responses)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_response)
    
    print(f"Success! Corrected paper saved to {os.path.basename(output_file)}")

if __name__ == "__main__":
    main()
