import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import requests

# Set page config with dark theme
st.set_page_config(
    page_title="WordWise - Language Learning Hub",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cosmic Purple/Blue Gradient Background with Nebula Effect
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, 
                                  rgba(67, 0, 107, 0.9) 0%, 
                                  rgba(12, 5, 64, 0.95) 90%) !important;
        background-attachment: fixed !important;
    }
    .main {
        background: rgba(15, 5, 40, 0.85) !important;
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 900px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1 {
        color: #ff6ec7 !important;
        text-align: center;
        font-size: 2.8rem !important;
        margin-bottom: 1rem;
        text-shadow: 0 0 12px rgba(255, 110, 199, 0.4);
    }
    .subheader {
        color: #a7ffeb !important;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stTextInput>div>div>input {
        background: rgba(0, 0, 30, 0.7) !important;
        color: white !important;
        border: 1px solid #6a5acd !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    .stSelectbox>div>div>select {
        background: rgba(0, 0, 30, 0.7) !important;
        color: white !important;
        border: 1px solid #6a5acd !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6e45e2 0%, #88d3ce 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        margin: 1rem auto;
        display: block;
        width: 100%;
        max-width: 300px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(110, 69, 226, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(110, 69, 226, 0.6);
    }
    .card {
        background: rgba(20, 10, 50, 0.7) !important;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 4px solid #6e45e2;
    }
    .card h4 {
        color: #88d3ce !important;
        margin-top: 0 !important;
        font-size: 1.4rem !important;
    }
    .card p {
        color: white !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
    }
    .stAudio {
        width: 100% !important;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main App Content
st.markdown("<div class='main'>", unsafe_allow_html=True)

# Header
st.markdown("<h1>WORDWISE: LANGUAGE LEARNING HUB</h1>", unsafe_allow_html=True)
st.markdown(
    """<p class='subheader'>
    Type a word in English and get translations, meanings, and pronunciation!
    </p>""", 
    unsafe_allow_html=True
)

# Input Section
col1, col2 = st.columns(2)
with col1:
    text = st.text_input("Enter a word or phrase in English:", key="input_text")

with col2:
    translator = GoogleTranslator()
    languages = translator.get_supported_languages(as_dict=True)
    language_names = list(languages.keys())
    target_lang = st.selectbox(
        "Choose target language:", 
        language_names,
        key="lang_select"
    )

# Action Button
if st.button("✨ TRANSLATE & SPEAK", key="translate_btn"):
    if text:
        try:
            lang_code = languages[target_lang]
            translated = GoogleTranslator(source='auto', target=lang_code).translate(text)

            # Results Display
            st.markdown(
                f"""<div class='card'>
                <h4>🔤 ORIGINAL (ENGLISH)</h4>
                <p>{text}</p>
                </div>""", 
                unsafe_allow_html=True
            )

            st.markdown(
                f"""<div class='card'>
                <h4>🌐 TRANSLATED ({target_lang.upper()})</h4>
                <p>{translated}</p>
                </div>""", 
                unsafe_allow_html=True
            )

            # Dictionary API
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{text.lower()}")
            if response.status_code == 200:
                meaning = response.json()[0]['meanings'][0]['definitions'][0]['definition']
                st.markdown(
                    f"""<div class='card'>
                    <h4>📖 DEFINITION</h4>
                    <p>{meaning}</p>
                    </div>""", 
                    unsafe_allow_html=True
                )
            else:
                st.warning("Couldn't fetch definition. Try another word.")

            # Text-to-Speech
            try:
                tts = gTTS(text=translated, lang=lang_code)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                    tts.save(tmpfile.name)
                    st.audio(tmpfile.name, format="audio/mp3")
            except ValueError:
                st.warning("Voice not available for this language.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter some text first!")

st.markdown("</div>", unsafe_allow_html=True)