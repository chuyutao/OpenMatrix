from openai import OpenAI

import datetime

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def append_to_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)

api_key = open_file('api-keys/openaiapikey2.txt')
chatbot1 = open_file('personalities/Activated.txt')

def chatgpt(api_key, chatbot, history_content):

    client = OpenAI(api_key=api_key, base_url="https://chat-router.recursal-dev.com/dFe6VG2eAjfEjGt7yb39q")
    context = "You are going to analyze a smart speaker conversation. This is a two-way conversation between a user and an AI. You will be updating the user's bio. Look for new facts, information about their name, hobbies, family, personality, goals, desires. Summarize key insights as bullets."
    prompt = {"role": "system", "content": f"{chatbot}\n\n{context}"}
    messages = [{"role": "user", "content": history_content}]
    messages.insert(0, prompt)

    completion = client.chat.completions.create(model="gpt-4",
    messages=messages,
    temperature=0.7,
    max_tokens=1024)
    return completion.choices[0].message.content

def process_history_and_update_user():
    history_content = open_file('history-files/history.txt')
    user_content = open_file('history-files/user.txt')

    # Print the current contents of history.txt and user.txt
    print("Current 'history-files/history.txt' content:")
    print(history_content)
    print("\nCurrent 'history-files/user.txt' content:")
    print(user_content)

    # Generate insights
    insights = chatgpt(api_key, chatbot1, history_content)

    # Print insights
    print("\nAdding the following insights to the 'user.txt' file:")
    print(insights)

    # Append timestamp and insights to user.txt
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    append_to_file('history-files/user.txt', f"\n\nTimestamp: {timestamp}\nInsights:\n{insights}")

# Process history.txt and update user.txt
process_history_and_update_user()
