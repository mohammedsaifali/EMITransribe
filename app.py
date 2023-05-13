import streamlit as st
from google.cloud import speech
from google.cloud import translate_v2 as translate
from pydub import AudioSegment
import io
import os

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "transcribe-386609-94023ff24190.json"

def transcribe_audio(file, file_format):
    client = speech.SpeechClient()

    # convert ogg to wav if necessary
    if file_format == 'ogg':
        audio = AudioSegment.from_ogg(file)
        file = io.BytesIO()
        audio.export(file, format="wav")
        file.seek(0)

    audio = speech.RecognitionAudio(content=file.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ar",
    )

    response = client.recognize(config=config, audio=audio)
    
    for result in response.results:
        return result.alternatives[0].transcript

def translate_text(text):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language='en')
    return result['translatedText']

st.title('Arabic Audio to English Text Transcription')

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "ogg"])
if uploaded_file is not None:
    try:
        st.write("Transcribing and translating, please wait...")
        file_format = uploaded_file.name.split('.')[-1]  # get the file extension
        arabic_text = transcribe_audio(uploaded_file, file_format)
        english_text = translate_text(arabic_text)
        st.write("Transcription in Arabic:")
        st.write(arabic_text)
        st.write("Translation in English:")
        st.write(english_text)
    except Exception as e:
        st.write("Sorry, an error occurred. Please make sure that the uploaded file is a valid audio file.")
        st.write(str(e))
