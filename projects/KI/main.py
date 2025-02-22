import os
import json
import subprocess
import threading
import time
from dotenv import dotenv_values
from asyncio import run

from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)

from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "KI")

DefaultMessage = f"{Username}: Hello {Assistantname}, How are you?\n{Assistantname}: Welcome {Username}. I am doing well. How may I help you?"

subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    try:
        with open(r'Data/ChatLog.json', "r", encoding='utf-8') as file:
            if len(file.read()) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as f:
                    f.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as f:
                    f.write(DefaultMessage)
    except FileNotFoundError:
        pass

def ReadChatLogJson():
    try:
        with open('Data/ChatLog.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    
    formatted_chatlog = formatted_chatlog.replace("User", Username)
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname)
    
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
            Data = file.read()
        
        if len(Data) > 0:
            with open(TempDirectoryPath('Responses.data'), "w", encoding="utf-8") as file:
                file.write(Data)
    except FileNotFoundError:
        pass

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def MainExecution():
    print("")
    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)
    print(f"Decision: {Decision}")
    
    if any(i.startswith("general") for i in Decision) or any(i.startswith("realtime") for i in Decision):
        MergedQuery = " ".join(i.split()[1:] for i in Decision if i.startswith("general") or i.startswith("realtime"))
    
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = queries
            ImageExecution = True
    
    if ImageExecution:
        try:
            with open("Frontend/Files/ImageGeneration.data", "w") as file:
                file.write(f"{ImageGenerationQuery}, True")
            p1 = subprocess.Popen(["python", r'Backend/ImageGeneration.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False)
            subprocesses.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")
    
    if "general" in Decision:
        SetAssistantStatus("Thinking...")
        Answer = ChatBot(QueryModifier(MergedQuery))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
    
    elif "realtime" in Decision:
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(MergedQuery))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)

def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." not in AIStatus:
                SetAssistantStatus("Available...")
        time.sleep(0.1)

def SecondThread():
    QueryFinal = "Okay, Bye!"
    Answer = ChatBot(QueryModifier(QueryFinal))
    ShowTextToScreen(f"{Assistantname}: {Answer}")
    SetAssistantStatus("Answering...")
    TextToSpeech(Answer)
    os.exit(1)

if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()