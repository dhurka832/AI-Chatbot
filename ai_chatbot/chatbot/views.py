import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read API Key from environment
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # You can change this if needed

# Chatbot API View
@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "")

            if not user_input:
                return JsonResponse({"error": "Message is empty"}, status=400)

            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7
            }

            # Call Together AI API
            response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)

            print("Status:", response.status_code)
            print("Response:", response.text)

            if response.status_code == 200:
                reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                if reply:
                    return JsonResponse({"reply": reply})
                else:
                    return JsonResponse({"error": "No reply from model"}, status=500)
            else:
                error_detail = response.json().get("error", "API call failed")
                return JsonResponse({"error": error_detail}, status=500)

        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


# Renders the chat interface HTML
def chat_page(request):
    return render(request, "chat.html")
