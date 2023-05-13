import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
import tempfile

def transcribe_audio(file, file_format):
    r = sr.Recognizer()
    
    # convert ogg to wav if necessary
    if file_format == 'ogg':
        audio = AudioSegment.from_ogg(file)
        file = tempfile.NamedTemporaryFile(delete=False)
        file_name = file.name+'.wav'
        audio.export(file_name, format="wav")
        file = file_name
    
    with sr.AudioFile(file) as source:
        audio_data = r.record(source)
        text_in_arabic = r.recognize_google(audio_data, language='ar')
    return text_in_arabic

def translate_text(text):
    translator = Translator()
    translation = translator.translate(text, src='ar', dest='en')
    return translation.text

st.title('EMI Arabic Audio to English Text Transcription')
st.text('Developed by Saif')

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])
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
