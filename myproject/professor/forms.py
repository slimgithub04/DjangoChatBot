from django import forms
from .models import CourseContent, Course

class CourseContentForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    pdf_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    video_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = CourseContent
        fields = ['course', 'pdf_file', 'video_file', 'text_content']

from django import forms

class QuestionForm(forms.Form):
    topic = forms.CharField(label="Sujet", max_length=100)
    difficulty = forms.ChoiceField(label="Difficulté", choices=[
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    ])

class ScenarioForm(forms.Form):
    topic = forms.CharField(label="Sujet", max_length=100)

class QuizForm(forms.Form):
    topic = forms.CharField(label="Sujet", max_length=100)
    num_questions = forms.IntegerField(label="Nombre de questions", min_value=1, max_value=20)

class SummaryForm(forms.Form):
    content = forms.CharField(label="Contenu", widget=forms.Textarea)

class ContentForm(forms.Form):
    title = forms.CharField(label="Titre", max_length=100)
    file = forms.FileField(label="Fichier")


from django import forms
from .models import UploadedContent, UploadedPDF, UploadedVideo

class UploadContentForm(forms.ModelForm):
    # Champ pour l'upload de fichiers PDF (multiple)
    pdf_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Upload PDF Files"
    )

    # Champ pour l'upload de fichiers vidéo (multiple)
    video_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Upload Video Files"
    )

    # Champ pour le contenu texte (peut être rempli manuellement ou par transcription vocale)
    text_content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        label="Text Content"
    )

    class Meta:
        model = UploadedContent
        fields = ['pdf_files', 'video_files', 'text_content']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        # Sauvegarder les fichiers PDF
        for pdf_file in self.cleaned_data.get('pdf_files', []):
            pdf = UploadedPDF(pdf_file=pdf_file)
            pdf.save()
            instance.pdf_files.add(pdf)

        # Sauvegarder les fichiers vidéo
        for video_file in self.cleaned_data.get('video_files', []):
            video = UploadedVideo(video_file=video_file)
            video.save()
            instance.video_files.add(video)

        return instance