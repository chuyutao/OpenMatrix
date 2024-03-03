import requests  # Add this line at the top of the file
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
import subprocess

def text_to_speech(text, voice_id, api_key):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream'
    headers = {
        'accept': '*/*',
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'voice_settings': {
            'stability': 0.50,
            'similarity_boost': 0.30
        }
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    response.raise_for_status()  # Ensure we raise an exception for bad responses

    # Use subprocess to pipe the audio data to ffplay and play it
    ffplay_cmd = ['ffplay', '-autoexit', '-nodisp', '-']
    ffplay_proc = subprocess.Popen(ffplay_cmd, stdin=subprocess.PIPE)

    try:
        for chunk in response.iter_content(chunk_size=4096):
            ffplay_proc.stdin.write(chunk)
#            print("Playing audio...")
    except Exception as e:
        print(f"Error while playing audio: {e}")
    finally:
        # Close the ffplay process when finished
        ffplay_proc.stdin.close()
        ffplay_proc.wait()
        

def print_colored(agent, text):
    agent_colors = {
        "Openhome:": Fore.YELLOW,
    }
    color = agent_colors.get(agent, "")
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")

