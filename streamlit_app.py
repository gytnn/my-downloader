import streamlit as st
import yt_dlp
import os

st.title("YouTube Video & MP3 İndirici")

url = st.text_input("Video Linkini Buraya Yapıştırın:")
choice = st.radio("Format Seçin:", ["MP4 (Video)", "MP3 (Ses)"])

if st.button("Hazırla ve İndir"):
    if url:
        with st.spinner('İşleniyor... (Bu biraz zaman alabilir)'):
            # YouTube engelini aşmak için eklenen ayarlar
            ydl_opts = {
                'format': 'bestaudio/best' if choice == "MP3" else 'bestvideo+bestaudio/best',
                'outtmpl': 'downloaded_file.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                # BURASI ÖNEMLİ: YouTube'u kandırmak için sahte kimlik bilgileri
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'referer': 'https://www.google.com/',
                'nocheckcertificate': True,
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
                    
                    # MP3 uzantısı kontrolü
                    if choice == "MP3" and not filename.endswith(".mp3"):
                        filename = filename.rsplit('.', 1)[0] + ".mp3"
                
                with open(filename, "rb") as f:
                    st.download_button(
                        label="Dosyayı Bilgisayarına Kaydet", 
                        data=f, 
                        file_name=os.path.basename(filename)
                    )
                
                # İndirme bittikten sonra temizlik
                os.remove(filename)
            except Exception as e:
                st.error(f"Maalesef YouTube engeline takıldık: {e}")
    else:
        st.warning("Lütfen bir link girin.")
