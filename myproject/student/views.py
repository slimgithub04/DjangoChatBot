from django.shortcuts import render, redirect
from django.conf import settings
from professor.models import CourseContent, Transcription, Prompte, QuizQuestion
import google.generativeai as genai
from PyPDF2 import PdfReader
from pydub import AudioSegment

# Vue pour le chatbot
def chatbot(request):
    if request.method == 'POST':
        # Récupérer la question de l'utilisateur
        user_question = request.POST.get('question')

        # Récupérer le dernier prompt généré
        try:
            latest_prompt = Prompte.objects.latest('created_at')
            prompt_text = latest_prompt.prompt_text
        except Prompte.DoesNotExist:
            # Si aucun prompt n'est disponible
            prompt_text = "No course material available."

        # Configurer l'API Gemini avec la clé API
        genai.configure(api_key=settings.GOOGLE_API_KEY)

        # Créer le modèle Gemini
        model = genai.GenerativeModel('gemini-pro')

        # Préparer le prompt pour l'API Gemini
        prompt = f"""
        You are an AI tutor. Your role is to assist students with their questions.

        === Course Material ===
        {prompt_text}

        Answer the following question. If the question is related to the course material, use the information above. If not, provide a general response.

        Question: {user_question}
        """

        try:
            # Générer une réponse avec l'API Gemini
            response = model.generate_content(prompt)
            answer = response.text.strip()
        except Exception as e:
            # Gérer les erreurs
            answer = f"An error occurred: {str(e)}"

        # Renvoyer la réponse à l'utilisateur
        return render(request, 'chatbot.html', {'answer': answer, 'user_question': user_question})

    # Si la méthode n'est pas POST, afficher le formulaire vide
    return render(request, 'chatbot.html')

# Vue pour afficher les quiz
def view_quizzes(request):
    quizzes = QuizQuestion.objects.all()
    return render(request, 'view_quizzes.html', {'quizzes': quizzes})