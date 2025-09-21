from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

genai.configure(api_key="*************************")

model = genai.GenerativeModel("gemini-1.5-flash")

def home(request):
    return render(request, "chatbot/chat.html")

def get_response(request):
    user_message = request.GET.get("message", "")
    if not user_message:
        return JsonResponse({"response": "Please enter a message."})

    response = model.generate_content(
        user_message,
        generation_config={"max_output_tokens": 50}
    )

    return JsonResponse({"response": response.text})
