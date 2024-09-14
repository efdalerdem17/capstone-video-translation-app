# capstone-video-translation-app

This project is a Streamlit-based application that converts videos to audio, transcribes the audio, and translates the transcription into multiple languages.

## Features

- Convert video files to audio format.
- Transcribe audio to text using Whisper.
- Translate the transcribed text into multiple languages using Google Translator.
- Generate and download subtitle files (SRT) for each target language.

## Installation

To run this application locally, you'll need to have Python and the following packages installed. You can install the required packages using `pip`.

1. Clone the repository:

   ```bash
   git clone https://github.com/efdalerdem17/capstone-video-translation-app.git
   cd capstone-video-translation-app
   
2. Install the required packages:
   pip install -r requirements.txt
   
3. Create a requirements.txt file with the following content:
   streamlit
  ffmpeg-python
  whisper
  deep-translator

4.Run the Streamlit application:
streamlit run capstone-proje-video-translation.py

## Usage

Select the target languages for translation from the sidebar.
Upload a video file (supported formats: MP4, AVI, MOV).
Click on the "Process Video" button.
The application will convert the video to an audio file, transcribe the audio, and translate the text into the selected languages.
You can view the transcriptions and translations directly on the app and download subtitle files (SRT) for each target language.

## Dependencies

Streamlit
FFmpeg
Whisper
Deep Translator





