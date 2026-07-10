from django.shortcuts import render

# Create your views here.
def packages_page(request):
  return render(request, 'packages/packages_page.html')