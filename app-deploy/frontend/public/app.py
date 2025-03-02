import streamlit as st
import requests
import azure.cognitiveservices.speech as speechsdk
import base64

# ✅ Azure Credentials
TRANSLATOR_KEY = "DEhHCE5cQjvgQKgGED6jnRXsHy35nitDr3s08vxI9vxFi2L4ZRKxJQQJ99BCAC8vTInXJ3w3AAAbACOGsQDG"
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"
SPEECH_KEY = "2zmUjopIuml8BZ90sJrwhAVBmOpigL90C6sxRuskiTiP7Ubb8BTXJQQJ99BCAC8vTInXJ3w3AAAYACOGL6Ku"
SPEECH_REGION = "westus2"

# ✅ Available languages
LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "Hindi": "hi",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru"
}

# ✅ Speech to Text Function
def speech_to_text():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    st.write("Listening... Speak now.")

    result = recognizer.recognize_once()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech recognized, please try again."
    elif result.reason == speechsdk.ResultReason.Canceled:
        return "Speech recognition canceled. Check your subscription key or region."


# ✅ Text Translation Function
def translate_text(text, target_language):
    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": "westus3",
        "Content-Type": "application/json"
    }

    params = {
        "api-version": "3.0",
        "to": target_language
    }

    body = [{"text": text}]
    response = requests.post(TRANSLATOR_ENDPOINT, params=params, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()[0]['translations'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

# ✅ Encode Image for Background
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

image_path = "kyndryl_838x472.jpg"  # Make sure to have an image in the working directory or provide full path
image_base64 = encode_image(image_path)

# ✅ Streamlit App
st.markdown(f"""
<style>
    body {{
        background: url('data:image/jpg;base64,{image_base64}') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Arial', sans-serif;
        color: white;
    }}
    .marquee {{
        font-size: 20px;
        font-weight: bold;
        color: yellow;
        white-space: nowrap;
        overflow: hidden;
        display: block;
        width: 100%;
        animation: marquee 10s linear infinite;
    }}
    @keyframes marquee {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}
</style>
<div class='marquee'>🌍 Welcome to the Azure AI Translator & Speech Service! 🎤🌎</div>
""", unsafe_allow_html=True)

# Title of the page
st.title("🌐 Azure Speech-to-Text & Translator")

# Speech-to-Text
if st.button("🎤 Start Speech Recognition"):
    recognized_text = speech_to_text()
    st.text_area("Recognized Speech", recognized_text, height=150)

# Text Translation
text_input = st.text_area("Enter or Speak Text to Translate", height=150)
language_dropdown = st.selectbox("Select Language", list(LANGUAGES.keys()))

if st.button("Translate"):
    translated_text = translate_text(text_input, LANGUAGES[language_dropdown])
    st.text_area("Translated Text", translated_text, height=150)
