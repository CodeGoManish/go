# Import required libraries
import asyncio  # For asynchronous programming
import os  # OS functionalities
import subprocess  # System interactions
import requests  # HTTP requests
import webbrowser  # Opening URLs
import keyboard  # Keyboard control
from webbrowser import open as webopen  # Web browser opening
from AppOpener import close, open as appopen  # App control
from dotenv import dotenv_values  # Environment variable management
from bs4 import BeautifulSoup  # HTML parsing
from rich import print  # Styled console output
from pywhatkit import search, playonyt  # Google search & YouTube playback
from groq import Groq  # AI chatbot functionality

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve Groq API key

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Define user-agent for making web requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# Define professional responses
PROFESSIONAL_RESPONSES = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help with.",
    "I'm at your service for any additional questions or support you may need. Don't hesitate to ask!"
]

# List to store chatbot messages
messages = []

# Function to perform a Google search
def GoogleSearch(topic):
    try:
        search(topic)  # Perform Google search using pywhatkit
        return True
    except Exception as e:
        print(f"[red]Error performing Google Search:[/red] {e}")
        return False

# Function to generate content using AI
async def Content(query):
    try:
        response = client.chat(query)
        return response
    except Exception as e:
        print(f"[red]Error generating content:[/red] {e}")
        return "Error generating content."

# Function to search on YouTube
def YouTubeSearch(topic):
    try:
        url = f"https://www.youtube.com/results?search_query={topic}"
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"[red]Error performing YouTube Search:[/red] {e}")
        return False

# Function to play a YouTube video
def PlayYouTube(query):
    try:
        playonyt(query)
        return True
    except Exception as e:
        print(f"[red]Error playing YouTube video:[/red] {e}")
        return False

# Function to open an application
def OpenApp(app):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"[red]Error opening application:[/red] {e}")
        return False

# Function to close an application
def CloseApp(app):
    try:
        if "chrome" not in app:
            close(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"[red]Error closing application:[/red] {e}")
        return False

# Function to execute system commands
def System(command):
    try:
        if command == "mute":
            keyboard.press_and_release("volume mute")
        elif command == "unmute":
            keyboard.press_and_release("volume mute")  # Toggle mute
        elif command == "volume up":
            keyboard.press_and_release("volume up")
        elif command == "volume down":
            keyboard.press_and_release("volume down")
        else:
            subprocess.run(command, shell=True, check=True)
        return True
    except Exception as e:
        print(f"[red]Error executing system command:[/red] {e}")
        return False

# Function to extract links from HTML content
def extract_links(html):
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", {"jsname": "UWckNb"})  # Extract relevant links
    return [link.get("href") for link in links if link.get("href")]

# Function to perform a Google search and retrieve HTML content
def search_google(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("[red]Failed to retrieve search results.[/red]")
            return None
    except Exception as e:
        print(f"[red]Error performing Google search:[/red] {e}")
        return None

# Asynchronous function to translate and execute commands
async def TranslateAndExecute(commands):
    funcs = []

    for command in commands:
        if command.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command.removeprefix("open ")))

        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))

        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYouTube, command.removeprefix("play ")))

        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")))

        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")))

        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(System, command.removeprefix("system ")))

        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content ")))

        else:
            print(f"[red]No function found for command:[/red] {command}")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

# Asynchronous function to automate command execution
async def Automation(commands):
    async for result in TranslateAndExecute(commands):
        yield result
