from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    text_content = models.TextField(null=True, blank=True)
    transcription_text = models.TextField(null=True, blank=True)  # Texte transcrit à partir de la vidéo
    pdf_text = models.TextField(null=True, blank=True)  # Texte extrait du PDF

    def __str__(self):
        return f"Content for {self.course.title}"

class Transcription(models.Model):
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    transcription_text = models.TextField()

    def __str__(self):
        return f"Transcription for {self.content.course.title}"

class QuizQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.question
    
from django.db import models

class Prompte(models.Model):
    prompt_text = models.TextField()  # Pour stocker le texte du prompt
    created_at = models.DateTimeField(auto_now_add=True)  # Horodatage de création

    def __str__(self):
        return f"Prompt created at {self.created_at}"

class Prompt(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    prompt_text = models.TextField()  # Texte combiné pour OpenAI
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt for {self.course.title}"
    
from django.db import models

class UploadedContent(models.Model):
    # Champ pour les fichiers PDF (plusieurs fichiers possibles)
    pdf_files = models.ManyToManyField('UploadedPDF', blank=True)

    # Champ pour les fichiers vidéo (plusieurs fichiers possibles)
    video_files = models.ManyToManyField('UploadedVideo', blank=True)

    # Champ pour le contenu texte (peut être rempli manuellement ou par transcription vocale)
    text_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Content Uploaded at {self.created_at}"

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.pdf_file.name

class UploadedVideo(models.Model):
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.video_file.name