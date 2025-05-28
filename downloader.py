import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

BASE_URL = "https://orsai.org/125cuentos/"
TRADEMARK = "2003-2024.Hernán Casciari.Un blog puede convertirse en cualquier cosa"
DIGITAL_ONCEAN_ID=""
OUTPUT_DIR = "stories"
MAX_WORKERS = 5  # Be gentle with the server
DELAY = 0.5  # Seconds between requests

def setup_directory():
    """Create output directory if it doesn't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
def extract_mp3_url(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the playlist item
    playlist_item = soup.find('li', class_='sr-playlist-item')
    
    if playlist_item:
        # Extract the audio URL from data-audiopath attribute
        mp3_url = playlist_item.get('data-audiopath', '')
        return mp3_url
    
    return None

def download_mp3(url:str,story_id:int):
    response = requests.get(url, stream=True)
    filename = os.path.join(OUTPUT_DIR, f"story_{story_id:03d}.mp3")
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"File saved to {filename}")

def get_story(session, story_id):
    """Fetch and process a single story"""
    try:
        formatted_id = f"{story_id:03d}"
        url = f"{BASE_URL}{formatted_id}"
        
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title= soup.find_all('title')[0].get_text(strip=True)
        paragraphs = soup.find_all('p')
        story = "\n".join(p.get_text(strip=True) for p in paragraphs)
        story = title + "\n\n" + story
        story = story.replace(TRADEMARK, "").strip()
        download_mp3(url=extract_mp3_url(response.text),story_id=story_id)
        
        return story_id, story
    except Exception as e:
        print(f"Error downloading story {story_id}: {str(e)}")
        return story_id, None

def save_story(story_id, content):
    """Save story to a file"""
    if content:
        filename = os.path.join(OUTPUT_DIR, f"story_{story_id:03d}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def download_all_stories():
    setup_directory()
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    print(f"Downloading stories 1-125 to '{OUTPUT_DIR}' directory...")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for story_id in range(1, 126):
            futures.append(executor.submit(get_story, session, story_id))
        
        for future in as_completed(futures):
            story_id, content = future.result()
            if save_story(story_id, content):
                print(f"✓ Saved story {story_id:03d}")
            else:
                print(f"✗ Failed to save story {story_id:03d}")

if __name__ == "__main__":
    start_time = time.time()
    download_all_stories()
    print(f"Completed in {time.time() - start_time:.2f} seconds")