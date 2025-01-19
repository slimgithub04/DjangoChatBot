from django.urls import path
from . import views

app_name = 'professor'
urlpatterns = [
    path('upload/', views.upload_content, name='upload_content'),
    path('upload/success/', views.upload_success, name='upload_success'),
    
]