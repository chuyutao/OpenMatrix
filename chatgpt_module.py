from openai import OpenAI
import datetime
import requests


# You might need to adjust the imports based on what the chatgpt function uses

def fetch_recipe(query, app_id, app_key):
    base_url = "https://api.edamam.com/search"
    params = {
        "q": query,
        "app_id": "19b42bba",
        "app_key": "0dbb59a43ea716cfa5128be3c23172e3",
        "from": 0,
        "to": 1  # Adjust if more recipes are needed
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        recipes = data.get("hits")
        if recipes:
            # Just fetching the first recipe for simplicity
            recipe = recipes[0]['recipe']
            title = recipe['label']
            ingredients = recipe['ingredientLines']
            url = recipe['url']
            return f"Recipe Title: {title}\nIngredients: {', '.join(ingredients)}\nURL: {url}"
        else:
            return "No recipes found."
    else:
        return "Failed to fetch recipes."
        
        
def interpret_dish_name(user_input, client):
    # Use the LLM to interpret the dish name or key ingredients from the user input
    conversation = [
        {"role": "system", "content": "Extract the main dish or ingredient from the user's query about a recipe."},
        {"role": "user", "content": user_input}
    ]
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=conversation)
    interpreted_input = completion.choices[0].message.content.strip()
    return interpreted_input

def chatgpt(api_key, conversation, chatbot, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0, edamam_app_id=None, edamam_app_key=None):
    

    client = OpenAI(api_key=api_key)
    
    # If the conversation is about recipes, interpret the dish name or ingredients
    if "recipe" in user_input.lower() and edamam_app_id and edamam_app_key:
        # Interpret the dish name or key ingredients from user_input using the LLM
        query = interpret_dish_name(user_input, client)
        recipe_info = fetch_recipe(query, edamam_app_id, edamam_app_key)
        conversation.append({"role": "system", "content": recipe_info})
        
    conversation.append({"role": "user", "content": user_input})
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    messages_input.insert(0, prompt[0])
    completion = client.chat.completions.create(
        model="gpt-4",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input)
    chat_response = completion.choices[0].message.content
    conversation.append({"role": "assistant", "content": chat_response})

    # Write to history file
    with open('history-files/history.txt', 'a', encoding='utf-8') as history_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_file.write(f"Timestamp: {timestamp}\n")
        history_file.write(f"User: {user_input}\n")
        history_file.write(f"Openhome: {chat_response}\n\n")

    return chat_response
