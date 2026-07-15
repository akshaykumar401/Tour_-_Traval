from django.http import JsonResponse
from django.shortcuts import render
from .forms import FeedbackForm, AIAgentForm
from .models import Feedback
import os
from google import genai

# Create your views here.
def ai_agent(query):
  PREDEFINED_ANSWERS = {
    "how to book?": (
      "To book a tour, visit the Tours page, choose your itinerary, select your "
      "travel dates and number of guests, then click Book Now and complete checkout."
    ),
    "cancellation policy": (
      "You can cancel your trip up to 1 day before the start date and receive a "
      "90% refund."
    ),
    "payment secure?": (
      "Yes. Payments are processed through a secure, PCI-compliant gateway with "
      "256-bit SSL encryption. We do not store your full card details."
    ),
    "do i need insurance?": (
      "We strongly recommend comprehensive travel insurance. It can help cover "
      "medical expenses, cancellations, lost luggage, and other travel emergencies."
    ),
  }

  normalized_query = query.lower().strip()
  for keyword, predefined_reply in PREDEFINED_ANSWERS.items():
    if keyword in normalized_query:
      return predefined_reply

  api_key = os.getenv('GEMINI_API_KEY')
  if not api_key:
    return "The AI assistant is not configured yet. Add GEMINI_API_KEY to the project .env file."

  try:
    client = genai.Client(api_key=api_key)
    result = client.models.generate_content(
      model="gemini-3.5-flash",
      contents=(
        "You are NextStop's travel support assistant. Answer the user's "
        "question clearly and concisely.\n\n"
        f"User question: {query}"
      ),
    )
    return result.text or "I couldn't generate an answer for that question. Please try again."
  except Exception:
    return "Sorry, the AI assistant is temporarily unavailable. Please try again shortly."

def review_page(request):
  all_reviews = Feedback.objects.order_by('-created_at')
  
  # Calculating Average Rating
  average_rating = 0
  for review in all_reviews:
    average_rating = average_rating + review.reating
  average_rating_rounded = round(average_rating / len(all_reviews)) if all_reviews else 0
  
  if request.method == 'POST':
    form = FeedbackForm(request.POST)
    if form.is_valid():
      form.save()
      all_reviews = Feedback.objects.order_by('-created_at')
      average_rating = sum(review.reating for review in all_reviews)
      average_rating_rounded = round(average_rating / len(all_reviews)) if all_reviews else 0
      return render(request, 'help_center/review_page.html', {
        'form': FeedbackForm(), 
        'success': True,
        'all_reviews': all_reviews,
        'average_rating': f"{average_rating / len(all_reviews):.1f}" if len(all_reviews) > 0 else 0,
        'average_rating_rounded': average_rating_rounded,
      })
  else:
    form = FeedbackForm()
  return render(request, 'help_center/review_page.html', {
    'form': form, 
    'all_reviews': all_reviews,
    'average_rating': f"{average_rating / len(all_reviews):.1f}" if len(all_reviews) > 0 else 0,
    'average_rating_rounded': average_rating_rounded,
  })

def FAQ_page(request):
  if request.method == 'POST':
    form = AIAgentForm(request.POST)
    if form.is_valid():
      query = form.cleaned_data['query']
      response = ai_agent(query)
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'query': query, 'response': response})
      return render(request, 'help_center/FAQ_page.html', {
        'form': AIAgentForm(),
        'query': query,
        'response': response,
      })
  else:
    form = AIAgentForm()
  return render(request, 'help_center/FAQ_page.html', {'form': form})
