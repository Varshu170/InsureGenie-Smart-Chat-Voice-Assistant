import json
import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

# Load intents from JSON file with explicit encoding
with open('intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)['intents']

def process_intent(intent_name, language):
    # Find the intent by name
    intent = next((item for item in intents if item["name"] == intent_name), None)
    if intent:
        response = intent["responses"]
        return response
    else:
        return "Sorry, I didn't understand that."

def recognize_intent(text):
    # This is a very basic example of intent recognition.
    # You can use more sophisticated techniques like NLP or machine learning for better results.
    for intent in intents:
        if any(keyword in text for keyword in intent["keywords"]):
            return intent["name"]
    return "unknown"

def listen_and_respond():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            intent = recognize_intent(text)
            print("Intent:", intent)
            response = process_intent(intent, intents)
            print("Assistant:", response)
            speak(response,'ta')
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            speak("Sorry, I couldn't understand what you said.",'ta')
        except sr.RequestError:
            print("Sorry, I'm having trouble accessing Google Speech Recognition service.")
            speak("Sorry, I'm having trouble accessing Google Speech Recognition service.",'ta')
        except Exception as e:
            print("Error:", str(e))
            speak("Sorry, an error occurred.",'ta')


def speak(text, language):
    engine.setProperty('voice', 'ta')  # Set the voice to Tamil
    engine.say(text)
    engine.runAndWait()

def detect_language(text):
    # Detect language using Google Translate API
    result = translator.detect(text)
    return result.lang

# Main loop to continuously listen for user input
while True:
    listen_and_respond()