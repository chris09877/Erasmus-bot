from django.shortcuts import render, HttpResponse
# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot import get_chatbot_response


# Create your views here.
def home(request):
    return render(request, "home.html")


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        user_message = body.get('message')
        response_text = get_chatbot_response(user_message)
        return JsonResponse({'response': response_text})

    return JsonResponse({'error': 'Invalid request method'}, status=405)