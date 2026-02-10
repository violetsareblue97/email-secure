import streamlit as st
import joblib
import re
import unicodedata

st.set_page_config(page_title="EmailSafe+ AI", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=Inter:wght@400;600&display=swap');
    
    .stApp {
        background: #050505;
        color: #e6edf3;
        font-family: 'Inter', sans-serif;
    }

    /* Header Section */
    .main-header {
        text-align: center;
        padding: 50px 0 30px 0;
        border-bottom: 1px solid #1f2937;
        margin-bottom: 40px;
    }
    
    .brand-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 11px;
        letter-spacing: 6px;
        color: #10b981;
        text-transform: uppercase;
    }

    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 40px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -1.5px;
        margin-top: 5px;
    }

    /* Input Field */
    .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #30363d !important;
        padding: 20px !important;
        background: #0d1117 !important;
        color: #ffffff !important;
        font-size: 15px !important;
    }

    .stTextArea textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 1px #10b981 !important;
    }

    /* Action Button */
    .stButton>button {
        background: #ffffff !important;
        color: #000000 !important;
        padding: 12px !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        border: none !important;
        width: 100% !important;
        margin-top: 10px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background: #10b981 !important;
        color: #ffffff !important;
    }

    /* Sidenote Section */
    .info-container {
        margin-top: 60px;
        padding: 30px;
        background: #0a0a0a;
        border: 1px solid #1f2937;
        border-radius: 4px;
    }
    
    .info-title {
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .info-text {
        color: #9ca3af;
        font-size: 13px;
        line-height: 1.7;
        text-align: justify;
    }

    .result-card {
        padding: 24px;
        margin-top: 30px;
        border-radius: 4px;
        background: #111111;
        border: 1px solid #1f2937;
    }
    </style>
    """, unsafe_allow_html=True)

#LOGIKA ANALISIS
def clean_text_accurate(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', 'link_url', text)
    text = re.sub(r'\S+@\S+', 'email_address', text)
    
    urgency_list = ['action required', 'pending', 'selected', 'reward', 'confirm', 'immediately']
    for word in urgency_list:
        text = text.replace(word, f' urgent_{word} ')
        
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    return " ".join(text.split())

@st.cache_resource
def load_model():
    return joblib.load("phishing_model.joblib")

model = load_model()

#UI LAYOUT
st.markdown("""
    <div class="main-header">
        <div class="brand-name">Neural Protocol v4</div>
        <div class="main-title">Phishing Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.05, 0.9, 0.05])

with col2:
    email_input = st.text_area("", height=220, placeholder="Input raw telemetry or email text for analysis...")
    
    if st.button("Run Diagnostic"):
        if email_input:
            cleaned = clean_text_accurate(email_input)
            prob = model.predict_proba([cleaned])[0]
            skor = prob[1]
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            if skor > 0.65:
                st.error(f"CRITICAL ({skor*100:.1f}%)")
                st.caption("Email ini merupakan email Phishing.")
            elif skor > 0.35:
                st.warning(f"WARNING ({skor*100:.1f}%)")
                st.caption("Email ini mencurigakan.")
            else:
                st.success(f"CLEAR ({skor*100:.1f}%)")
                st.caption("Email ini bukan phishing.")
            st.markdown('</div>', unsafe_allow_html=True)

    #SIDENOTE
    st.markdown("""
        <div class="info-container">
            <div class="info-title">Security Advisory: Image-Based Obfuscation</div>
            <div class="info-text">
                Dalam kasus di mana konten email tidak dapat disalin, kemungkinan besar email tersebut adalah 
                <b>Visual Phishing</b>. Metode ini digunakan oleh penyerang untuk menghindari inspeksi berbasis teks 
                oleh filter keamanan. Kebijakan keamanan standar menyarankan untuk tidak melakukan interaksi klik 
                pada elemen visual dan segera melakukan terminasi pada pesan tersebut.
            </div>
        </div>
    """, unsafe_allow_html=True)
