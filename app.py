import streamlit as st
import joblib
import re
import unicodedata

st.set_page_config(page_title="EmailSecure", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=Plus+Jakarta+Sans:wght@400;600&display=swap');
    
    .stApp {
        background-color: #050505;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e6edf3;
    }

    /* Futuristic Header */
    .main-header {
        text-align: center;
        padding: 60px 0 40px 0;
        border-bottom: 1px solid #1f2937;
        margin-bottom: 40px;
    }
    
    .brand-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 14px;
        letter-spacing: 4px;
        color: #10b981;
        text-transform: uppercase;
        margin-bottom: 10px;
        text-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
    }

    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 42px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -1px;
        line-height: 1.2;
    }

    /* Dark Input Area */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid #30363d !important;
        padding: 24px !important;
        background: #0d1117 !important;
        font-size: 16px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }

    .stTextArea textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.15) !important;
        background: #0d1117 !important;
    }

    /* Glow Button */
    .stButton>button {
        background: #ffffff !important;
        color: #000000 !important;
        padding: 16px 28px !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 15px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #10b981 !important;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
    }

    /* Result Container */
    .result-container {
        margin-top: 40px;
        padding: 24px;
        border-radius: 12px;
        background: #111111;
        border: 1px solid #1f2937;
    }

    /* Sidenote: Refined Futuristic */
    .info-container {
        margin-top: 50px;
        padding: 25px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #1f2937;
        border-left: 4px solid #10b981;
        border-radius: 4px;
    }

    .info-title {
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }

    .info-text {
        color: #8b949e;
        font-size: 14px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# Logika Akurasi
def clean_text_accurate(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    
    text = re.sub(r'http\S+|www\S+|https\S+', 'link_url', text)
    text = re.sub(r'\S+@\S+', 'email_address', text)

    urgency_list = ['action required', 'pending', 'selected', 'reward', 'confirm', 'immediately']
    for word in urgency_list:
        text = text.replace(word, f' urgent_{word} ')
        
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = " ".join(text.split())
    return text

@st.cache_resource
def load_model():
    return joblib.load("phishing_model.joblib")

model = load_model()

# Header
st.markdown("""
    <div class="main-header">
        <div class="brand-name">Email Safe+</div>
        <div class="main-title">Deteksi Email Phishing<br>Berbasis AI</div>
    </div>
    """, unsafe_allow_html=True)

# Input Area
email_input = st.text_area("", height=220, placeholder="Tempel isi badan email yang ingin diperiksa disini...")

if st.button("Analisis Keamanan"):
    if email_input:
        cleaned = clean_text_accurate(email_input)
        prob = model.predict_proba([cleaned])[0]
        skor = prob[1]
        
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        
        if skor > 0.65:
            st.error(f"Peringatan: Terdeteksi Phishing ({skor*100:.1f}%)")
            st.markdown("<small>Ditemukan manipulasi teks atau indikasi penipuan yang kuat.</small>", unsafe_allow_html=True)
        elif skor > 0.35:
            st.warning(f"Perhatian: Email Mencurigakan ({skor*100:.1f}%)")
            st.markdown("<small>Pola email ini menyerupai phishing. Harap waspada.</small>", unsafe_allow_html=True)
        else:
            st.success(f"Aman: Email Terverifikasi ({skor*100:.1f}%)")
            st.markdown("<small>Tidak ditemukan tanda-tanda ancaman siber yang mencurigakan.</small>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Silakan masukkan teks email terlebih dahulu.")

# SIDENOTE
st.markdown("""
    <div class="info-container">
        <div class="info-title">Tidak bisa menyalin/copy isi email?</div>
        <div class="info-text">
            Jika email Anda sepenuhnya berupa gambar (tidak bisa di-salin), ini adalah tanda kuat <b>Image-Based Phishing</b>. 
            Scammer menggunakan teknik ini untuk menghindari filter keamanan teks. 
            <b>Jangan klik bagian mana pun dari gambar tersebut!</b> Segera hapus dan lapor sebagai spam.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#30363d; font-size:10px; letter-spacing:3px;'>NEURAL ENGINE v4.0</p>", unsafe_allow_html=True)
