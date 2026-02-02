import streamlit as st
import joblib
import re

# 1. Konfigurasi Halaman & CSS Modern
st.set_page_config(page_title="Phishing Detector", layout="wide")

st.markdown("""
    <style>
    /* Mengatur palet warna dan font global */
    .stApp {
        background-color: #1a1a1a;
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Bar Judul Atas yang Minimalis */
    .header-bar {
        background-color: #262626;
        padding: 30px;
        text-align: center;
        border-bottom: 3px solid #10b981;
        margin-bottom: 50px;
    }

    .header-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Area Input Teks Modern */
    .stTextArea textarea {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        font-size: 16px !important;
    }

    .stTextArea textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 1px #10b981 !important;
    }

    /* Tombol Analisis Utama */
    .stButton>button {
        width: 100%;
        background-color: #10b981 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        height: 55px !important;
        border-radius: 8px !important;
        border: none !important;
        font-size: 16px !important;
        margin-top: 20px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #059669 !important;
        letter-spacing: 1px;
    }

    /* Tombol Share Minimalis */
    .share-btn button {
        background-color: transparent !important;
        color: #10b981 !important;
        border: 1px solid #10b981 !important;
        height: 35px !important;
    }

    /* Label Input */
    label {
        color: #a3a3a3 !important;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Logika Pemrosesan Data
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', 'link_url', text)
    text = re.sub(r'\S+@\S+', 'email_address', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

@st.cache_resource
def load_model():
    return joblib.load("phishing_model.joblib")

model = load_model()

# 3. Struktur Header
st.markdown('<div class="header-bar"><div class="header-title">Email Phishing Detector</div></div>', unsafe_allow_html=True)

# 4. Fungsi Share (Kanan Atas)
c1, c2 = st.columns([6, 1])
with c2:
    if st.button("Share Link"):
        st.code("https://share.streamlit.io/user/repo") # Ganti dengan link Anda

# 5. Konten Utama Tengah
col_a, col_b, col_c = st.columns([1, 2, 1])

with col_b:
    email_input = st.text_area("Input Teks Email", height=300)
    
    if st.button("Analisis Sekarang"):
        if email_input:
            cleaned_input = clean_text(email_input)
            prob = model.predict_proba([cleaned_input])[0]
            skor_phishing = prob[1]
            
            st.write("---")
            if skor_phishing > 0.75:
                st.error(f"Status: Terdeteksi Phishing ({skor_phishing*100:.1f}%)")
            elif skor_phishing > 0.40:
                st.warning(f"Status: Mencurigakan ({skor_phishing*100:.1f}%)")
            else:
                st.success(f"Status: Aman ({skor_phishing*100:.1f}%)")
        else:
            st.info("Silakan masukkan teks email terlebih dahulu")
