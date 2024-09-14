import streamlit as st
import os
import tempfile
import ffmpeg
import whisper
from deep_translator import GoogleTranslator

def convert_video_to_audio(video_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            video_path = temp_video.name

        audio_path = os.path.splitext(video_path)[0] + '.mp3'

        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='libmp3lame', ac=2, ar='44100')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )

        return audio_path
    except ffmpeg.Error as e:
        st.error(f'FFmpeg hatası: {e.stderr.decode()}')
        return None
    finally:
        if os.path.exists(video_path):
            os.unlink(video_path)

def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"], result["language"]
    except Exception as e:
        st.error(f'Ses çevirme hatası: {e}')
        return None, None

def translate_text(text, source_lang, target_languages):
    try:
        translations = {}
        for lang in target_languages:
            if lang == source_lang:
                translations[lang] = text
            else:
                translator = GoogleTranslator(source=source_lang, target=lang)
                translation = translator.translate(text)
                translations[lang] = translation
        return translations
    except Exception as e:
        st.error(f'Çeviri hatası: {e}')
        return None

def create_srt(translations):
    srt_files = {}
    for lang, text in translations.items():
        srt_content = "1\n00:00:00,000 --> 00:00:05,000\n" + text
        srt_files[lang] = srt_content
    return srt_files

def main():
    st.title("Video Çeviri Uygulaması")
    
    st.header("1. Hedef Dil Seçimi")
    languages = {
        "Türkçe": "tr",
        "İngilizce": "en",
        "Fransızca": "fr",
        "Almanca": "de"
    }
    selected_languages = st.multiselect("Çevirmek istediğiniz dilleri seçin:", list(languages.keys()))
    
    st.header("2. Video Yükleme")
    uploaded_file = st.file_uploader("Video dosyasını seçin", type=["mp4", "avi", "mov"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("Video İşle"):
            with st.spinner("Video işleniyor ve çeviriliyor..."):
                audio_path = convert_video_to_audio(uploaded_file)
                
                if audio_path:
                    st.success("Video başarıyla ses dosyasına dönüştürüldü.")
                    st.audio(audio_path)
                    
                    transcript, detected_lang = transcribe_audio(audio_path)
                    
                    if transcript and detected_lang:
                        st.success(f"Ses dosyası metne çevrildi. Algılanan dil: {detected_lang}")
                        st.text_area("Transkripsiyon:", value=transcript, height=200)
                        
                        if selected_languages:
                            target_lang_codes = [languages[lang] for lang in selected_languages]
                            translations = translate_text(transcript, detected_lang, target_lang_codes)
                            
                            if translations:
                                st.subheader("Çeviri Sonuçları")
                                srt_files = create_srt(translations)
                                for lang, text in translations.items():
                                    lang_name = [k for k, v in languages.items() if v == lang][0]
                                    st.text_area(f"{lang_name} çevirisi:", value=text, height=100)
                                    st.download_button(f"{lang_name} Çevirisini İndir (SRT)", srt_files[lang], f"{lang_name.lower()}_ceviri.srt")
                            else:
                                st.error("Metin çeviri işlemi başarısız oldu.")
                        else:
                            st.warning("Çeviri için hedef dil seçilmedi.")
                    else:
                        st.error("Ses dosyası metne çevrilirken hata oluştu.")
                else:
                    st.error("Video dönüştürme işlemi başarısız oldu.")

if __name__ == "__main__":
    main()
