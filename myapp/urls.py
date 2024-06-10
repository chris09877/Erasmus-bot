from django.urls import path
from . import views, chatbot

urlpatterns = [
    path('', views.home, name='home'),
    path('chat', views.chat, name='chat'),
]