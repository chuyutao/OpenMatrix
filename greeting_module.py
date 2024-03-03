# Import necessary modules
from chatgpt_module import chatgpt
from file_management import open_file
from text_speech_module import text_to_speech

# Add other necessary imports

def first_time_greeting(api_key, elapikey, chatbot1, conversation1, voice_id1):
    # Read user information
    user_info = open_file('history-files/user.txt')

    # Initial greeting message
    greeting_message = "Hi Shannon. I'm excited to meet you. I'm the OpenHome onboarding assistant. Let me summarize what I know about you."

    # Pass user info to the chatbot
    chat_response = chatgpt(api_key, conversation1, chatbot1, user_info, temperature=0.5)

    # Convert chatbot's response to speech
    text_to_speech(chat_response, voice_id1, elapikey)
