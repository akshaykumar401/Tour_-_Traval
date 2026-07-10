from django.shortcuts import render

# Create your views here.
def gallery_page(request):
  return render(request, 'gallery/gallery_page.html')

  