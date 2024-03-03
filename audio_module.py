import sounddevice as sd
import soundfile as sf
from openai import OpenAI



def record_and_transcribe(api_key, duration=8, fs=44100):
    client = OpenAI(api_key=api_key)
    print('Recording...')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print('Recording complete.')
    filename = 'temp-sound/myrecording.wav'
    sf.write(filename, myrecording, fs)
    with open(filename, "rb") as file:
        result = client.audio.transcriptions.create(model="whisper-1", file=file)
    transcription = result.text
    print("Transcription:", transcription)
    return transcription
