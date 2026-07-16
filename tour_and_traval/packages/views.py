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
      'image': image_url,
      'departure_date': p.departure_dates.all().first().departure_date,
    })
  return data

def package_detail_data_inJSON(request, package_id):
  package = Packages.objects.prefetch_related('images', 'features', 'itineraries', 'departure_dates').get(id=package_id)
  
  images = [img.image.url for img in package.images.all() if img.image]
  features = [{'id': f.id, 'feature': f.feature} for f in package.features.all()]
  itineraries = [{'id': i.id, 'day_number': i.day_number, 'title': i.title, 'description': i.description} for i in package.itineraries.all()]
  departure_dates = [{'id': d.id, 'departure_date': d.departure_date, 'total_seats': d.total_seats, 'available_seats': d.available_seats} for d in package.departure_dates.all()]

  data = {
    'id': package.id,
    'tag_line': package.tag_line,
    'category': package.category,
    'location': package.location,
    'mini_title': package.mini_title,
    'total_days': package.total_days,
    'total_nights': package.total_nights,
    'starting_price': package.starting_price,
    'max_people': package.max_people,
    'main_title': package.main_title,
    'description': package.description,
    'created_at': package.created_at,
    'images': images,
    'features': features,
    'itineraries': itineraries,
    'departure_dates': departure_dates
  }
  return data

def packages_page(request):
  data = packages_page_data_inJSON(request)
  return render(request, 'packages/packages_page.html', {'package_data': data})

def packages_detail_page(request, packages_id):
  data = package_detail_data_inJSON(request, packages_id)
  return render(request, 'packages/packages_detail_page.html', {
    'packages_data': data,
  })