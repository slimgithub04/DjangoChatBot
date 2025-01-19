from django.urls import path
from . import views

app_name = 'student'
urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
    path('quizzes/', views.view_quizzes, name='view_quizzes'),
]