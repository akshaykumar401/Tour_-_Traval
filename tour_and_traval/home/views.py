from django.shortcuts import render
# pyrefly: ignore [missing-import]
from packages.views import packages_page_data_inJSON

# Create your views here.
def home(request):
    packages_data = packages_page_data_inJSON(request)[:3] # [:3] -> Slice the top 3 data
    return render(request, "home/home_page.html", {'package_data': packages_data})