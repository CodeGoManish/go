from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv to load environment variables.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot about its role and behavior.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""
SystemChatBot = [{"role": "system", "content": System}]

# Attempt to load the chat log.
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open("Data/ChatLog.json", "w") as f:
        dump([], f)

# Function to get real-time date and time information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return (
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H:%M:%S')}\n"
    )

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

# Main chatbot function to handle user queries.
def ChatBot(Query):
    try:
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)
        
        messages.append({"role": "user", "content": Query})
        
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        Answer = Answer.replace("</s>", "").strip()
        
        messages.append({"role": "assistant", "content": Answer})
        
        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        
        return AnswerModifier(Answer)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main loop for chatbot interaction.
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = ChatBot(user_input)
        print(f"{Assistantname}: {response}")
# End of Backend/Chatbot.py