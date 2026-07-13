from django.shortcuts import render

# Create your views here.
def packages_page(request):
  return render(request, 'packages/packages_page.html')

def packages_detail_page(request, packages_id):
  return render(request, 'packages/packages_detail_page.html')