from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import json

app = Flask(__name__)

# Initialize the speech recognizer, text-to-speech engine, and translator
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

# Directory for saving audio files
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

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
    # Basic example of intent recognition
    for intent in intents:
        if any(keyword in text for keyword in intent["keywords"]):
            return intent["name"]
    return "unknown"

def text_to_speech(text, filename, language='en'):
    try:
        if language == 'hi':  # Hindi
            translated_text = translator.translate(text, dest='hi').text
        elif language == 'ta':  # Tamil
            translated_text = translator.translate(text, dest='ta').text
        else:
            translated_text = text  # Default to English if language is not specified

        engine.say(translated_text)
        engine.runAndWait()

        # Save the speech to an MP3 file
        filepath = os.path.join(AUDIO_DIR, filename)
        engine.save_to_file(translated_text, filepath)
        engine.runAndWait()
        return filepath
    except Exception as e:
        print("Error:", str(e))
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice')
def voice():
    return render_template('voice.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    # Process voice input and recognize intent
    audio_file = request.files['audio']
    language = request.form.get('language', 'en')
    intents_file = request.form.get('intents_file', 'intents_en.json')

    intents = load_intents(intents_file)
    try:
        with sr.AudioFile(audio_file) as source:
            audio_text = recognizer.record(source)
            text = recognizer.recognize_google(audio_text, language=language)
            text = text.lower()
            intent = recognize_intent(text, intents)
            response = process_intent(intent, intents)

            # Convert response to speech
            audio_filepath = text_to_speech(response[0], "response.mp3", language)
            return jsonify({'text': text, 'intent': intent, 'response': response[0], 'audio_url': f'/audio/response.mp3'})
    except sr.UnknownValueError:
        error_message = "Sorry, I couldn't understand what you said."
        audio_filepath = text_to_speech(error_message, "error.mp3", language)
        return jsonify({'error': error_message, 'audio_url': f'/audio/error.mp3'})
    except sr.RequestError:
        error_message = "Sorry, I'm having trouble accessing Google Speech Recognition service."
        audio_filepath = text_to_speech(error_message, "error.mp3", language)
        return jsonify({'error': error_message, 'audio_url': f'/audio/error.mp3'})
    except Exception as e:
        error_message = "Sorry, an error occurred."
        audio_filepath = text_to_speech(error_message, "error.mp3", language)
        return jsonify({'error': error_message, 'audio_url': f'/audio/error.mp3'})

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
