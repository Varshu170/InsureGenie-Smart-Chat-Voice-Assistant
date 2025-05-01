"""import json
import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

def load_intents(filename):
    # Load intents from JSON file with explicit encoding
    with open(filename, 'r', encoding='utf-8') as file:
        intents = json.load(file)['intents']
    return intents

def process_intent(intent_name, intents):
    # Find the intent by name
    intent = next((item for item in intents if item["name"] == intent_name), None)
    if intent:
        response = intent["responses"]
        return response
    else:
        return ["Sorry, I didn't understand that."]

def recognize_intent(text, intents):
    # This is a very basic example of intent recognition.
    # You can use more sophisticated techniques like NLP or machine learning for better results.
    for intent in intents:
        if any(keyword in text for keyword in intent["keywords"]):
            return intent["name"]
    return "unknown"

def listen_and_respond(intents, language):
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=5)  # Set a timeout of 5 seconds

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print("You said:", text)
            intent = recognize_intent(text, intents)
            print("Intent:", intent)
            response = process_intent(intent, intents)
            print("Assistant:", response)
            speak(response[0], language)  # Adjusted the function call to pass only the first response
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            speak("Sorry, I couldn't understand what you said.", language)
        except sr.RequestError:
            print("Sorry, I'm having trouble accessing Google Speech Recognition service.")
            speak("Sorry, I'm having trouble accessing Google Speech Recognition service.", language)
        except Exception as e:
            print("Error:", str(e))
            speak("Sorry, an error occurred.", language)


def speak(response, language):
    try:
        if language == 'hi':  # Hindi
            translated_text = translator.translate(response, dest='hi').text
            engine.setProperty('voice', 'hi')
        elif language == 'ta':  # Tamil
            translated_text = translator.translate(response, dest='ta').text
            engine.setProperty('voice', 'ta')
        else:
            translated_text = response  # Default to English if language is not specified
            engine.setProperty('voice', 'en')

        engine.say(translated_text)
        engine.runAndWait()
    except Exception as e:
        print("Error:", str(e))

def select_language():
    print("Select your language:")
    print("1. English")
    print("2. Hindi")
    print("3. Tamil")
    choice = input("Enter your choice (1/2/3): ")
    if choice == '1':
        return 'en', 'intents_en.json'  # English
    elif choice == '2':
        return 'hi', 'intents_hi.json'  # Hindi
    elif choice == '3':
        return 'ta', 'intents_ta.json'  # Tamil
    else:
        print("Invalid choice. Defaulting to English.")
        return 'en', 'intents_en.json'  # Default to English

# Main function to start the voice assistant
def main():
    language, intents_file = select_language()
    intents = load_intents(intents_file)
    listen_and_respond(intents, language)

# Run the main function
if __name__ == "__main__":
    main()
"""
import json
import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

def load_intents(filename):
    # Load intents from JSON file with explicit encoding
    with open(filename, 'r', encoding='utf-8') as file:
        intents = json.load(file)['intents']
    return intents

def process_intent(intent_name, intents):
    # Find the intent by name
    intent = next((item for item in intents if item["name"] == intent_name), None)
    if intent:
        response = intent["responses"]
        return response
    else:
        return "Sorry, I didn't understand that."

def recognize_intent(text, intents):
    # This is a very basic example of intent recognition.
    # You can use more sophisticated techniques like NLP or machine learning for better results.
    for intent in intents:
        if any(keyword in text for keyword in intent["keywords"]):
            return intent["name"]
    return "unknown"

def listen_and_respond(intents, language):
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print("You said:", text)
            intent = recognize_intent(text, intents)
            print("Intent:", intent)
            response = process_intent(intent, intents)
            print("Assistant:", response)
            speak(response[0], language)  # Adjusted the function call to pass only the first response
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            speak("Sorry, I couldn't understand what you said.", language)
        except sr.RequestError:
            print("Sorry, I'm having trouble accessing Google Speech Recognition service.")
            speak("Sorry, I'm having trouble accessing Google Speech Recognition service.", language)
        except Exception as e:
            print("Error:", str(e))
            speak("Sorry, an error occurred.", language)


def speak(response, language):
    try:
        if language == 'hi':  # Hindi
            translated_text = translator.translate(response, dest='hi').text
            engine.setProperty('voice', 'hi')
        elif language == 'ta':  # Tamil
            translated_text = translator.translate(response, dest='ta').text
            engine.setProperty('voice', 'ta')
        else:
            translated_text = response  # Default to English if language is not specified
            engine.setProperty('voice', 'en')

        engine.say(translated_text)
        engine.runAndWait()
    except Exception as e:
        print("Translation Error:", str(e))
        speak("Sorry, there was an error in translation.    ", 'en')


def select_language():
    print("Select your language:")
    print("1. English")
    print("2. Hindi")
    print("3. Tamil")
    choice = input("Enter your choice (1/2/3): ")
    if choice == '1':
        return 'en', 'intents_en.json'  # English
    elif choice == '2':
        return 'hi', 'intents_hi.json'  # Hindi
    elif choice == '3':
        return 'ta', 'intents_ta.json'  # Tamil
    else:
        print("Invalid choice. Defaulting to English.")
        return 'en', 'intents_en.json'  # Default to English

# Main function to start the voice assistant
def main():
    language, intents_file = select_language()
    intents = load_intents(intents_file)
    listen_and_respond(intents, language)

# Run the main function
if __name__ == "__main__":
    main()
