import streamlit as st
import joblib

# Memuat otak AI yang kita buat di Colab
model = joblib.load("phishing_model.joblib")

st.set_page_config(page_title="Email Phishing Detector")
st.title("Phishing Email Detector")
st.write("Cek apakah email yang Anda dapatkan merupakan email phishing!")

# Input teks dari user
email_text = st.text_area("Tempel isi email di sini:", height=200)

if st.button("Cek Email"):
    if email_text:
        prediction = model.predict([email_text])[0]
        prob = model.predict_proba([email_text])[0]

        if prediction == 1:
            st.error(f" Hati-hati! Email terdeteksi PHISHING (Akurasi: {prob[1]*100:.2f}%)")
        else:
            st.success(f"Aman. Terlihat seperti email normal ✔ (Akurasi: {prob[0]*100:.2f}%)")
    else:
        st.warning("Silakan masukkan teks email terlebih dahulu.")
