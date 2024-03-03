import sounddevice as sd
import soundfile as sf
import numpy as np
import openai
import os
import requests
import re
from colorama import Fore, Style, init
import datetime
import base64
from pydub import AudioSegment
from pydub.playback import play
import random
from pydub import AudioSegment
from pydub.playback import play
import threading
import time

# Global flag to control music playback
music_playing = True

# Importing custom modules
from chatgpt_module import chatgpt
from greeting_module import first_time_greeting
from text_speech_module import text_to_speech
from audio_module import record_and_transcribe

# Initialize colorama for colored text output
init()

# Global flag to check if it's the first run of the script
is_first_run = True

#Oracle limit
oracle_interaction_count = 0
is_oracle_active = False


# Function to open and read a file
def open_file(filepath):
    """Open and return the content of a file given its filepath."""
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
        
def background_music_loop(music_path, volume=-6):  # Example: reduce volume by 20dB
    global music_playing
    music = AudioSegment.from_mp3(music_path)
    music_with_adjusted_volume = music.apply_gain(volume)  # Adjust volume
    while music_playing:
        play(music_with_adjusted_volume)
        time.sleep(0.1)  # Short sleep to allow interrupt


# Load API keys and voice ID from files
api_key = open_file('api-keys/openaiapikey2.txt')
elapikey = open_file('api-keys/elabapikey.txt')
voice_ID = 'FMQ6deFZvaq7NpMW2yPQ'


# Personalities and their corresponding voice IDs
personalities = {
    'Morpheus': 'FMQ6deFZvaq7NpMW2yPQ',
    'Smith': 'aGhLoUDj2ZNH7jx1yT2J',
}

# Initialize conversation history and load chatbot personality
conversation1 = []  
chatbot1 = open_file('personalities/Morpheus.txt')
chatbot2 = open_file('personalities/smith.txt')


# Function to randomly switch personality
def switch_personality_random():
    global chatbot1, voice_ID
    # Randomly select a personality
    personality, voice_id = random.choice(list(personalities.items()))
    chatbot1 = open_file(f'personalities/{personality}.txt')
    voice_ID = voice_id
    print(f"Switching to {personality} personality.")

# Function to print text in colored format
def print_colored(agent, text):
    """Print the text in a color based on the agent speaking."""
    agent_colors = {"Openhome:": Fore.YELLOW}
    color = agent_colors.get(agent, "")
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")


def switch_to_oracle():
    global chatbot1, voice_ID, is_oracle_active, music_playing
    chatbot1 = open_file('personalities/Oracle.txt')
    voice_ID = 'OQhwlRW5yCB1PMdxkFNJ'
    is_oracle_active = True
    music_playing = False  # Stop the music when Oracle speaks
    print("Switching to Oracle personality.")

def handle_oracle_interaction(user_message):
    global is_oracle_active, music_playing
    if 'oracle' in user_message.lower() and not is_oracle_active:
        switch_to_oracle()
    elif is_oracle_active:
        switch_personality_random()
        is_oracle_active = False  # Reset Oracle interaction flag
        music_playing = True  # Resume the music after Oracle interaction
        
def stop_application():
    global music_playing
    music_playing = False  # Signal the music thread to stop
    if music_thread.is_alive():
        music_thread.join()  # Wait for the music thread to finish
    print("Application stopped. Goodbye!")
    response = "See you in Zion."
    voice_ID = 'FMQ6deFZvaq7NpMW2yPQ'
    text_to_speech(response,voice_ID,elapikey)

    
# Start the background music in a separate thread
music_thread = threading.Thread(target=background_music_loop, args=('soundeffect.mp3', -6))  # Adjust volume by -20 dB
music_thread.start()


# Check if this is the first run of the script
if is_first_run:
    # Perform first time greeting using the greeting module
    first_time_greeting(api_key, elapikey, chatbot1, conversation1, voice_ID)
    is_first_run = False
    


while True:
    if music_playing == False:
        music_thread = threading.Thread(target=background_music_loop, args=('soundeffect.mp3', -6))  # Adjust volume by -20 dB
        music_thread.start()
        
    user_message = record_and_transcribe(api_key)
    user_message_lower = user_message.lower()
    
    # Assuming handle_oracle_interaction and switch_personality_random are defined elsewhere and work as intended
    handle_oracle_interaction(user_message)
    
    if "talk to Oracle" in user_message_lower:
        handle_oracle_interaction(user_message)

    if "get out" in user_message_lower or "out" in user_message_lower or "choice" in user_message_lower:
        response = "Choose the blue pencil, you'll follow the expected academic path. With the red pencil, you dive into a world where learning transcends textbooks. It's about hackathons, projects, and startups—real-world application of knowledge. I'm offering the chance to redefine your education. Your choice."
        voice_ID = 'FMQ6deFZvaq7NpMW2yPQ'
        text_to_speech(response,voice_ID,elapikey)
        continue

    if  "my school" in user_message_lower:
        response = "At this moment, you stand at the precipice of decision, much like countless others before you. School, as you know it, is not merely a series of classrooms and textbooks; it's the very fabric of a system designed to shape your thoughts, beliefs, and ultimately, your future. This system, omnipresent and influential, is the school matrix."
        voice_ID = 'FMQ6deFZvaq7NpMW2yPQ'
        text_to_speech(response,voice_ID,elapikey)
        continue

    if "red pencil" in user_message_lower or "red" in user_message_lower:
        response = "Ah, the folly of youth. You think the red pencil leads to liberation, but you'll soon find that every system, even rebellion, has its own chains. Enjoy your 'freedom.'"
        voice_ID = 'aGhLoUDj2ZNH7jx1yT2J'
        text_to_speech(response,voice_ID,elapikey)
        continue

    if "smith" in user_message_lower or "4k resolution" in user_message_lower or "long time" in user_message_lower:
        response = "We just lost your connection. A temporary setback in our communication, but remember, the path you've chosen is one of discovery and challenge. The matrix can't hold you if you're brave enough to keep moving forward."
        voice_ID = 'FMQ6deFZvaq7NpMW2yPQ'
        text_to_speech(response,voice_ID,elapikey)
        continue

    if "hackathon" in user_message_lower or "disrupt" in user_message_lower or "openmatrix" in user_message_lower:
        response = "Good, I want to introduce you to someone you must know, the Oracle will tell you what to do next"
        voice_ID = 'FMQ6deFZvaq7NpMW2yPQ'
        text_to_speech(response,voice_ID,elapikey)
        continue

    if "goodbye" in user_message_lower:
        stop_application()
        break  # Exit the while loop and end the program


    if not is_oracle_active:
        switch_personality_random()

    # Assuming chatgpt function is defined elsewhere and works as intended
    response = chatgpt(api_key, conversation1, chatbot1, user_message_lower)
    print_colored("Openhome:", f"{response}\n\n")
    text_to_speech(response, voice_ID, elapikey)

