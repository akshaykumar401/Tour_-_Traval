from django.shortcuts import render
from .forms import FeedbackForm
from .models import Feedback

# Create your views here.
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
  return render(request, 'help_center/FAQ_page.html')
