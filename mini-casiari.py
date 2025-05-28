import os
import google.generativeai as genai
from dotenv import load_dotenv

STORIES="stories.txt"
PROMPT="""estos son algunos cuentos de hernan caciari , un famoso escritor argentino.
Escribe solamente un cuento corto , no olides pornerle titulo , relatado en primera persona , donde el habla de la vez que fue a una heladría y el de adelante se tomaba demasiado su tiempo para elegir el gusto de helado"""


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

def interact_with_gemini_text_file(filepath):
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

    initial_message = f"{file_content}\n\n{PROMPT}"
    try:
        response = chat.send_message(initial_message)
        print("\nGemini (initial response):")
        print(response.text)
    except Exception as e:
        print(f"An error occurred during initial Gemini interaction: {e}")
        return


def main():
    interact_with_gemini_text_file(STORIES)

if __name__ == "__main__":
    main()