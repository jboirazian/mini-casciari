import os
import google.generativeai as genai
from dotenv import load_dotenv
import sys

STORIES="stories.txt"
PROMPT="""estos son algunos cuentos de hernan caciari , un famoso escritor argentino.
Escribe solamente un cuento corto , no olides pornerle titulo , relatado en primera persona , el tema del cuento es: """


# Load environment variables from .env
load_dotenv()

# Configure the Gemini API key
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
    print("Please create a .env file with GOOGLE_API_KEY='YOUR_API_KEY_HERE'")
    exit()

def get_text_from_file(filepath):
    """Reads content from a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def story_generator(filepath,story_topic):
    """
    Interacts with Gemini using the content of a text file.
    The file content is used as part of the initial prompt.
    """
    file_content = get_text_from_file(filepath)
    if not file_content:
        return

    # For text-based models (like gemini-pro)
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

    # Start a chat session
    chat = model.start_chat(history=[])

    initial_message = f"{file_content}\n\n{PROMPT} {story_topic}"
    try:
        response = chat.send_message(initial_message)
        print(response.text)
    except Exception as e:
        print(f"An error occurred during initial Gemini interaction: {e}")
        return

    

if __name__ == "__main__":
    if(len(sys.argv)==2):
        story_generator(STORIES,sys.argv[1])
    else:
        print(f"Invalid argument. Run the program like this")
        print(f"{sys.argv[0]} 'tema de la historia'")