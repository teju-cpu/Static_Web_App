rom flask import Flask, request, jsonify
import os
import requests
import azure.cognitiveservices.speech as speechsdk
from azure.ai.language import LanguageClient
from azure.core.credentials import AzureKeyCredential
 
app = Flask(__name__)
 
# Set your keys and endpoints from environment variables
TRANSLATOR_KEY = os.getenv('DEhHCE5cQjvgQKgGED6jnRXsHy35nitDr3s08vxI9vxFi2L4ZRKxJQQJ99BCAC8vTInXJ3w3AAAbACOGsQDG')
TRANSLATOR_REGION = os.getenv('westus2')
LANGUAGE_KEY = os.getenv('Efh0ZjH4GEbT6Efq7uzKW8ZFHYDivdLlAry1iatizJDsh0ptGE5rJQQJ99BCAC8vTInXJ3w3AAAaACOGD1Po')
LANGUAGE_ENDPOINT = os.getenv('https://coglanguagedemo.cognitiveservices.azure.com/')
SPEECH_KEY = os.getenv('2zmUjopIuml8BZ90sJrwhAVBmOpigL90C6sxRuskiTiP7Ubb8BTXJQQJ99BCAC8vTInXJ3w3AAAYACOGL6Ku')
SPEECH_REGION = os.getenv('westus2')
 
# Function to detect the language of a given text using Azure Language Service
def detect_language(text):
    client = LanguageClient(endpoint=LANGUAGE_ENDPOINT, credential=AzureKeyCredential(LANGUAGE_KEY))
    response = client.detect_language(text)
    return response.primary_language.iso6391_name
 
# Function to translate text to a target language using Azure Translator
def translate_text(text, target_language):
    endpoint = f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}"
    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-Type": "application/json"  # Ensure the correct content type
    }
    body = [{"Text": text}]
    # Make the request to the Translator API
    response = requests.post(endpoint, headers=headers, json=body)
    # Ensure the response is successful
    if response.status_code != 200:
        return "Error in translation"
    # Parse the translated text from the API response
    translation = response.json()[0]["translations"][0]["text"]
    return translation
 
# Function to convert text to speech using Azure Speech Service
def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text).get()
 
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    input_text = data['text']
    target_language = data['target_language']
    # Detect the language of the input text using the Azure Language Service
    detected_language = detect_language(input_text)
    print(f"Detected Language: {detected_language}")
 
    # Translate the text to the target language using the Azure Translator service
    translated_text = translate_text(input_text, target_language)
    # Convert the translated text to speech using the Azure Speech service
    text_to_speech(translated_text)
    return jsonify({
        "detectedLanguage": detected_language,
        "translatedText": translated_text
    })
 
if __name__ == "__main__":
    app.run(debug=True)
