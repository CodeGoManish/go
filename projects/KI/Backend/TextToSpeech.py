import pygame  # For audio playback
import random  # For generating random choices
import asyncio  # For asynchronous operations
import edge_tts  # For text-to-speech functionality
import os  # For file handling
import threading  # For running playback without blocking execution
from dotenv import dotenv_values  # For reading environment variables

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")  # Default voice if not set

# Define the speech file path
speech_dir = os.path.join(os.getcwd(), "Data")
speech_file = os.path.join(speech_dir, "speech.mp3")
os.makedirs(speech_dir, exist_ok=True)

# Function to generate TTS audio asynchronously
async def TextToAudioFile(Text):
    try:
        communicate = edge_tts.Communicate(Text, AssistantVoice)
        await communicate.save(speech_file)
    except Exception as e:
        print(f"Error generating TTS audio: {e}")

# Function to play the generated speech file (runs in a separate thread)
def PlayAudio(func=lambda: True):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(speech_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if not func():
                pygame.mixer.music.stop()
                break
            pygame.time.Clock().tick(10)

        return True
    except Exception as e:
        print(f"Error in audio playback: {e}")
        return False
    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in cleanup: {e}")

# Function to handle text-to-speech with intelligent responses
def TextToSpeech(Text, func=lambda: True):
    sentences = Text.split(".")  # Split the text into sentences
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # Adjust response for long texts
    if len(sentences) > 4 and len(Text) >= 250:
        short_text = " ".join(sentences[:2]) + ". " + random.choice(responses)
    else:
        short_text = Text

    # Run async TTS generation
    try:
        asyncio.run(TextToAudioFile(short_text))
    except RuntimeError:
        asyncio.new_event_loop().run_until_complete(TextToAudioFile(short_text))

    # Run playback in a separate thread for better performance
    audio_thread = threading.Thread(target=PlayAudio, args=(func,))
    audio_thread.start()
    audio_thread.join()

# Main execution loop
if __name__ == "__main__":
    while True:
        user_text = input("Enter the text: ")
        TextToSpeech(user_text)
