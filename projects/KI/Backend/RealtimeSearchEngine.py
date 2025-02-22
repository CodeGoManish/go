from googlesearch import search
from groq import Groq  # Importing the Groq library to use its API
from json import load, dump  # Importing functions to read and write JSON files
import datetime  # Importing the datetime module for real-time information
from dotenv import dotenv_values  # Importing dotenv to read environment variables

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Retrieve environment variables
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
GroqAPIKey = env_vars.get("GroqAPIKey", "")

# Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

# Define system instructions
System =System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Load or create chat log
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []

# Function to perform a Google search and return formatted results
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    
    Answer += "[end]"
    return Answer

# Function to clean up chatbot responses
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

# Function to get real-time date and time information
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = (
        "Use this real-time information if needed:\n"
        f"Day: {day}\n"
        f"Date: {date}\n"
        f"Month: {month}\n"
        f"Year: {year}\n"
        f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    )
    return data

# System message setup
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to handle chatbot queries with real-time search
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load the chat log from JSON
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
    except FileNotFoundError:
        messages = []

    messages.append({"role": "user", "content": prompt})

    # Perform Google search and add results to system messages
    search_results = GoogleSearch(prompt)
    SystemChatBot.append({"role": "system", "content": search_results})

    # Generate a response using Groq API
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        # Process streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        # Clean response
        Answer = Answer.strip().replace("</s>", "")

        # Append chatbot response to the conversation log
        messages.append({"role": "assistant", "content": Answer})

        # Save updated chat log
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        # Remove the last system message (search results) after response generation
        SystemChatBot.pop()

        return AnswerModifier(Answer)

    except Exception as e:
        return f"Error: {str(e)}"

# Entry point for chatbot interaction
if __name__ == "__main__":
    print("Chatbot is running. Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = RealtimeSearchEngine(user_input)
        print(f"{Assistantname}: {response}")
         