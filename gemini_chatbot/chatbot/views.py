from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os
import logging

# Configure Gemini API key
API_KEY = os.environ.get("GOOGLE_API_KEY", "**************")
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-pro"

def index(request):
    return render(request, "chat/chat.html")

def get_response(request):
    user_message = request.GET.get("message", "").strip()

    # Return empty if user didn't type anything
    if not user_message:
        return JsonResponse({"response": ""})

    # Prompt for structured, medium-length response
    prompt = f"""
Answer the following question in medium-length content (250–300 words).

Use HTML format with clear headings and examples. Keep spacing between headings and content minimal:

<strong style='color:#0d47a1;'>Definition:</strong><br>
Explain in 4–6 lines.<br>

<strong style='color:#0d47a1;'>Types:</strong>
<ul>
<li>Type 1 – explain in 2–3 lines</li>
<li>Type 2 – explain in 2–3 lines</li>
</ul>

<strong style='color:#0d47a1;'>Applications:</strong>
<ul>
<li>Application 1 – explain briefly</li>
<li>Application 2 – explain briefly</li>
</ul>

<strong style='color:#0d47a1;'>Benefits:</strong>
<ul>
<li>Benefit 1 – explain briefly</li>
<li>Benefit 2 – explain briefly</li>
</ul>

<strong style='color:#0d47a1;'>Simple Example:</strong><br>
Provide 2–3 lines practical example.<br>

Question: {user_message}
"""

    try:
        chat = genai.GenerativeModel(MODEL_NAME).start_chat(history=[])
        response = chat.send_message(prompt)
        bot_response = response.text
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        bot_response = "Sorry, I could not generate a response. Please try again."

    return JsonResponse({"response": bot_response})
