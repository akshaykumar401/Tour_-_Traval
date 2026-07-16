from django.shortcuts import render
from django.http import JsonResponse
from .models import Packages

# Create your views here.
def packages_page_data_inJSON(request):
  packages = Packages.objects.prefetch_related('images').all()
  data = []
  for p in packages:
    image_obj = p.images.first()
    image_url = image_obj.image.url if image_obj and image_obj.image else None
    data.append({
      'id': p.id,
      'tag_line': p.tag_line,
      'category': p.category,
      'location': p.location,
      'mini_title': p.mini_title,
      'total_days': p.total_days,
      'total_nights': p.total_nights,
      'starting_price': p.starting_price,
      'max_people': p.max_people,
      'main_title': p.main_title,
      'description': p.description,
      'created_at': p.created_at,
      'image': image_url
    })
  return data

def packages_page(request):
  data = packages_page_data_inJSON(request)
  return render(request, 'packages/packages_page.html', {'package_data': data})

def packages_detail_page(request, packages_id):
  return render(request, 'packages/packages_detail_page.html', {'packages_id': packages_id})