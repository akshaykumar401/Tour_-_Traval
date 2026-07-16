from django.shortcuts import render
# pyrefly: ignore [missing-import]
from packages.views import packages_page_data_inJSON
# pyrefly: ignore [missing-import]
from gallery.models import Gallery

import random

# Create your views here.
def home(request):
    packages_data = packages_page_data_inJSON(request)[:3] # [:3] -> Slice the top 3 data
    
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

    return render(request, "home/home_page.html", {
        'package_data': packages_data,
        'gallery_data': gallery_data,
    })