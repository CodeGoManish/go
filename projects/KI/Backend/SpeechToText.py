from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt  # Importing mtranslate for translation

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Get the input language setting from the environment variables
InputLanguage = env_vars.get("InputLanguage")  # Default to English if not set

# Define the HTML code for the speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>
'''


# Replace the language setting in the HTML code with the input language from the environment variables
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file
html_file_path = os.path.join(os.getcwd(), "Data", "Voice.html")
os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Get the current working directory
current_dir = os.getcwd()

# Generate the file path for the HTML file
Link = f"file:///{html_file_path}"

# Set Chrome options for the WebDriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"

chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")  # Ensures headless mode works correctly

# Initialize the Chrome WebDriver using the ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary files
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

# Function to set the assistant's status by writing it to a file
def SetAssistantStatus(Status):
    status_file = os.path.join(TempDirPath, "Status.data")
    with open(status_file, "w", encoding="utf-8") as file:
        file.write(Status)

# Function to clean up and format user queries
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's"]

    # Check if the query is a question and add a question mark if necessary
    if any(word in query_words[0] for word in question_words):
        if new_query[-1] not in ['.', '?', '!']:
            new_query += "?"
    else:
        if new_query[-1] not in ['.', '?', '!']:
            new_query += "."

    return new_query.capitalize()

# Function to translate text to English
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition using the WebDriver
def SpeechRecognition():
    # Open the HTML file in the browser
    driver.get(Link)

    # Start speech recognition by clicking the start button
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            # Get the recognized text from the HTML output element
            Text = driver.find_element(By.ID, "output").text

            if Text:
                # Stop recognition by clicking the stop button
                driver.find_element(By.ID, "start").click()

                # If the input language is English, return the modified query
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    return UniversalTranslator(Text)

        except Exception as e:
            print(f"Error: {e}")
            break

# Run Speech Recognition
if __name__ == "__main__":
    print("Speak now...")
    result = SpeechRecognition()
    print("Recognized Speech:", result)

    # Close the WebDriver
    driver.quit()
# Compare this snippet from Backend/Model.py:
# # Define the function to process user queries
# def first_layer_dmm(prompt: str = "test"):
#     messages.append({"role": "user", "content": prompt})
#
#     # Create a streaming chat session with the Cohere model   
#     stream = co.chat_stream(