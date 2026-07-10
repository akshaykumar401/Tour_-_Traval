from django.shortcuts import render

# Create your views here.
def review_page(request):
  return render(request, 'help_center/review_page.html')

def FAQ_page(request):
  return render(request, 'help_center/FAQ_page.html')

