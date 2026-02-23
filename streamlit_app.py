import streamlit as st
import yt_dlp
import os

st.title("YouTube Video & MP3 İndirici")

url = st.text_input("Video Linkini Buraya Yapıştırın:")
choice = st.radio("Format Seçin:", ["MP4 (Video)", "MP3 (Ses)"])

if st.button("Hazırla ve İndir"):
    if url:
        with st.spinner('İşleniyor... Lütfen bekleyin.'):
            ydl_opts = {
                'format': 'bestaudio/best' if choice == "MP3" else 'best',
                'outtmpl': 'downloaded_file.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if choice == "MP3" else [],
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    if choice == "MP3":
                        filename = filename.rsplit('.', 1)[0] + ".mp3"
                
                with open(filename, "rb") as f:
                    st.download_button(label="Dosyayı Bilgisayarına Kaydet", data=f, file_name=filename)
                
                os.remove(filename) # Sunucuda yer kaplamasın diye siliyoruz
            except Exception as e:
                st.error(f"Hata oluştu: {e}")
    else:
        st.warning("Lütfen bir link girin.")
