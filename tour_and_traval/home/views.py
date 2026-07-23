from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
# pyrefly: ignore [missing-import]
from packages.views import packages_page_data_inJSON
# pyrefly: ignore [missing-import]
from gallery.models import Gallery
# pyrefly: ignore [missing-import]
from help_center.models import Feedback
import random
from .forms import SearchPackageForm

# Create your views here.
def home(request):
    packages_data = packages_page_data_inJSON(request)[:3] # [:3] -> Slice the top 3 data
    # getting those feedback which has 5 stars and only 5 feedbacks
    feedback_data = Feedback.objects.filter(reating=5)[:5]
    
    # Getting random 4 Images from Gallery (avoiding redundant places)
    all_galleries = list(Gallery.objects.all())
    random.shuffle(all_galleries)
    
    gallery_data = []
    seen_places = set()
    for item in all_galleries:
        if item.place not in seen_places:
            gallery_data.append(item)
            seen_places.add(item.place)
        if len(gallery_data) == 4:
            break
    
    # Handling Form
    if request.method == 'POST':
        form = SearchPackageForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            date = form.cleaned_data['date']
            query_string = urlencode({'location': location, 'date': date})
            return redirect(f"{reverse('packages_page')}?{query_string}")
    else:
        form = SearchPackageForm()

    return render(request, "home/home_page.html", {
        'package_data': packages_data,
        'gallery_data': gallery_data,
        'feedback_data': feedback_data,
        'form': form
    })