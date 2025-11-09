// --- HTML Selectors ---
let btn = document.querySelector("#btn");
let content = document.querySelector("#content");
let voice = document.querySelector("#voice");

// --- FIX 1: Voice Loading ---
// We need to store the voices in a global variable
let voices = [];
let hasWished = false; // FIX 2: Flag for first-time greeting

// This function loads the voices and is called when they are ready
function loadVoices() {
    voices = window.speechSynthesis.getVoices();
}

// Listen for the 'onvoiceschanged' event.
// This tells us when the voice list is ready.
window.speechSynthesis.onvoiceschanged = loadVoices;

// Call it once just in case they are already loaded
loadVoices();

// --- Core Functions ---

function speak(text) {
    let text_speak = new SpeechSynthesisUtterance(text);
    text_speak.rate = 1;
    text_speak.pitch = 1;
    text_speak.volume = 1;
    text_speak.lang = "en-US"; // FIX 1: Changed to English as all replies are in English

    // FIX 1: Use the pre-loaded 'voices' array
    // Find a good English female voice
    let femaleVoice = voices.find(voice =>
        voice.lang.includes("en") &&
        (voice.name.includes("Female") || voice.name.includes("Samantha") || voice.name.includes("Google US English"))
    );

    if (femaleVoice) {
        text_speak.voice = femaleVoice;
    } else {
        console.log("Female voice not found, using default.");
    }

    window.speechSynthesis.speak(text_speak);
}

function wishMe() {
    let day = new Date();
    let hours = day.getHours();
    if (hours >= 0 && hours < 12) {
        speak("Good Morning Manish");
    } else if (hours >= 12 && hours < 16) {
        speak("Good afternoon Manish");
    } else {
        speak("Good Evening Manish");
    }
}

// --- Speech Recognition Setup ---
let speechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = new speechRecognition();

recognition.onresult = (event) => {
    let currentIndex = event.resultIndex;
    let transcript = event.results[currentIndex][0].transcript;
    content.innerText = transcript;
    takeCommand(transcript.toLowerCase());
};

// --- Event Listeners ---
btn.addEventListener("click", () => {
    // FIX 2: Greet the user on their first click
    if (!hasWished) {
        wishMe();
        hasWished = true;
    }
    
    recognition.start();
    voice.style.display = "block";
    btn.style.display = "none";
});

// --- Command Handling ---
function takeCommand(message) {
    voice.style.display = "none";
    btn.style.display = "flex";

    if (message.includes("hello") || message.includes("hey") || message.includes("hi") || message.includes("hey ki") || message.includes("aur batao")) {
        speak("Hello Manish, how's your day going?");
    } else if (message.includes("how are you")) {
        speak("I am fine, Manish! Thank you for asking. Would you like me to do something for you?");
    } else if (message.includes("yes")) {
        speak("What can I do for you?");
    } else if (message.includes("who are you")) {
        speak("I am virtual assistant KI, created by Manish");
    } else if (message.includes("open youtube")) {
        speak("Opening YouTube...");
        window.open("https://youtube.com/", "_blank");
    } else if (message.includes("open google")) {
        speak("Opening Google...");
        window.open("https://google.com/", "_blank");
    } else if (message.includes("open facebook")) {
        speak("Opening Facebook...");
        window.open("https://facebook.com/", "_blank");
    } else if (message.includes("open instagram")) {
        speak("Opening Instagram...");
        window.open("https://instagram.com/", "_blank");
    } else if (message.includes("open calculator")) {
        // Note: This only works if the OS has a 'calculator://' protocol.
        // It may not work for all users.
        speak("Opening calculator...");
        window.open("calculator://");
    } else if (message.includes("open whatsapp")) {
        // Note: Same as calculator, this is not guaranteed to work.
        speak("Opening WhatsApp...");
        window.open("whatsapp://");
    } else if (message.includes("time")) {
        let time = new Date().toLocaleString(undefined, { hour: "numeric", minute: "numeric" });
        speak(time);
    } else if (message.includes("date")) {
        let date = new Date().toLocaleString(undefined, { day: "numeric", month: "short" });
        speak(date);
    } else {
        // FIX 3: Simplified the fallback Google search
        let query = message.replace("ki", "").trim(); // Clean up the query
        let finalText = "This is what I found on the internet regarding " + query;
        speak(finalText);
        window.open(`https://www.google.com/search?q=${query}`, "_blank");
    }
}
