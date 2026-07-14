from django.shortcuts import render
from .models import Gallery

# Create your views here.
def gallery_page(request):
  gallery = Gallery.objects.order_by('-created_at')
  categories = Gallery.IMAGE_TYPE_CHOICES
  
  # Filter categories that have images and ensure uniqueness
  seen = set()
  filtered_categories = []
  for category in categories:
    if category[0] not in seen and Gallery.objects.filter(type=category[0]).exists():
      seen.add(category[0])
      filtered_categories.append(category)

  return render(request, 'gallery/gallery_page.html', {
    'gallery': gallery,
    'categories': filtered_categories
  })

  