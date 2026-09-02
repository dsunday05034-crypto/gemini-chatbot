import sys
import time
import threading
import re
from google import genai
from dotenv import load_dotenv

# Load Api key from .env
load_dotenv()
client = genai.Client()
chat = client.chats.create(model="gemini-3.7-flash")

RESET = "\033[0m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"

def thinking_animation(stop_animation):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not stop_animation.is_set():
        sys.stdout.write(f"\r{YELLOW}Thinking... {chars[i]}{RESET}")
        sys.stdout.flush()
        i = (i + 1) % len(chars)

        # Sleep for a short period of time to control the speed of the animation
        time.sleep(0.1)

    # Overwrite the thinking animation with spaces to clear it and return to the beginning of the line    
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()

while True:
    try:
        question = input(f"{GREEN}You: {RESET}")
    except (KeyboardInterrupt, EOFError):
        print(f"\n{YELLOW}Exiting chat.{RESET}")
        break

    if question.lower() == "exit":
        break

    stop_animation = threading.Event()
    spinner_thread = threading.Thread(target=thinking_animation, args=(stop_animation,))
    spinner_thread.start()

    max_retries = 3
    response = None

    for attempt in range(max_retries):
        try:
            response = chat.send_message(question)
            break
        except Exception as e:
            error_str = str(e)
            
            # Handle Rate Limit (429)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                match = re.search(r"Please retry in ([0-9.]+)s", error_str)
                wait_time = float(match.group(1)) if match else 21.0
                
                stop_animation.set()
                spinner_thread.join()
                
                print(f"\n{YELLOW}Rate limit hit. Sleeping for {wait_time:.1f}s (Attempt {attempt+1}/{max_retries})...{RESET}")
                time.sleep(wait_time)
                
                stop_animation = threading.Event()
                spinner_thread = threading.Thread(target=thinking_animation, args=(stop_animation,))
                spinner_thread.start()
                
            # Handle Server Overload / High Demand (503)
            elif "503" in error_str or "UNAVAILABLE" in error_str:
                wait_time = 5.0 * (attempt + 1) # Exponential backoff: 5s, 10s, 15s
                
                stop_animation.set()
                spinner_thread.join()
                
                print(f"\n{YELLOW}Model busy (503 High Demand). Retrying in {wait_time}s (Attempt {attempt+1}/{max_retries})...{RESET}")
                time.sleep(wait_time)
                
                stop_animation = threading.Event()
                spinner_thread = threading.Thread(target=thinking_animation, args=(stop_animation,))
                spinner_thread.start()
            else:
                stop_animation.set()
                spinner_thread.join()
                print(f"\n{RED}Gemini: Error: {e}{RESET}")
                break
    else:
        stop_animation.set()
        spinner_thread.join()
        print(f"\n{RED}Gemini: Error: Maximum connection retries exceeded.{RESET}")
        continue

    if response:
        stop_animation.set()
        spinner_thread.join()
        print(f"{CYAN}Gemini:{RESET} {response.text}")