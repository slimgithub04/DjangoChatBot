import os
import requests
import time
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CourseContentForm
from .models import Prompte
from PyPDF2 import PdfReader
from pydub import AudioSegment

GLADIA_API_KEY = settings.GLADIA_API_KEY

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    return " ".join(page.extract_text() for page in reader.pages)

def extract_audio_from_video(video_file):
    audio_output_path = os.path.join(settings.MEDIA_ROOT, 'audio', f"{video_file.name}.mp3")
    os.makedirs(os.path.dirname(audio_output_path), exist_ok=True)
    audio = AudioSegment.from_file(video_file, format="mp4")
    audio.export(audio_output_path, format="mp3")
    return audio_output_path

def transcribe_audio(audio_url):
    gladia_url = "https://api.gladia.io/v2/transcription/"
    headers = {"x-gladia-key": GLADIA_API_KEY, "Content-Type": "application/json"}
    request_data = {"audio_url": audio_url}
    initial_response = requests.post(gladia_url, headers=headers, json=request_data).json()
    result_url = initial_response.get("result_url")
    
    if result_url:
        while True:
            poll_response = requests.get(result_url, headers=headers).json()
            if poll_response.get("status") == "done":
                return poll_response.get("result", {}).get("transcription", {}).get("full_transcript")
            time.sleep(1)
    return None

def upload_content(request):
    if request.method == 'POST':
        form = CourseContentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pdf_texts = [extract_text_from_pdf(pdf_file) for pdf_file in request.FILES.getlist('pdf_file')]
                transcription_texts = []
                
                for video_file in request.FILES.getlist('video_file'):
                    audio_url = extract_audio_from_video(video_file)
                    transcription = transcribe_audio(audio_url)
                    if transcription:
                        transcription_texts.append(transcription)
                
                combined_text = f"""
                === Transcription Vidéo ===
                {" ".join(transcription_texts)}

                === Texte PDF ===
                {" ".join(pdf_texts)}

                === Texte Manuel ===
                {form.cleaned_data['text_content']}
                """

                Prompte.objects.create(prompt_text=combined_text)
                return redirect('upload_success')

            except Exception as e:
                return render(request, 'upload_content.html', {'error': str(e), 'form': form})
    else:
        form = CourseContentForm()

    return render(request, 'upload_content.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')