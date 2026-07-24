from django.shortcuts import render
from django.http import JsonResponse
from .models import Packages
# pyrefly: ignore [missing-import]
from help_center.forms import FutureUpdateForm
# pyrefly: ignore [missing-import]
from help_center.models import FutureUpdate
import requests

# Create your views here.
def packages_page_data_inJSON(request):
  packages = Packages.objects.prefetch_related('images').all()
  
  location = request.GET.get('location')
  date = request.GET.get('date')

  if location:
    packages = packages.filter(location__icontains=location)
  if date:
    packages = packages.filter(departure_dates__departure_date=date).distinct()

  data = []
  for p in packages:
    image_obj = p.images.first()
    image_url = str(image_obj.image) if image_obj and image_obj.image and str(image_obj.image).startswith('http') else (image_obj.image.url if image_obj and image_obj.image else None)
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
      'departure_date': p.departure_dates.first().departure_date if p.departure_dates.first() else None,
    })
  return data

def package_detail_data_inJSON(request, slug):
  package = Packages.objects.prefetch_related('images', 'features', 'itineraries', 'departure_dates').get(id=slug)
  
  images = [str(img.image) if img.image and str(img.image).startswith('http') else img.image.url for img in package.images.all() if img.image]
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

def send_future_request_success_mail(request, email):
  subject = 'Future Package Notification'
  domain = request.get_host()
  base_url = f"https://{domain}"
  html_message=f"""
      <div style="margin: 0; padding: 0; background-color: #f7fafc; font-family: 'Inter', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; width: 100% !important;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f7fafc; padding: 64px 20px;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" max-width="600" cellspacing="0" cellpadding="0" border="0" style="max-width: 600px; width: 100%; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(26, 54, 93, 0.05);">
            <tr>
              <td height="6" style="background-color: #875200; line-height: 6px; font-size: 6px;">&nbsp;</td>
            </tr>
            <tr>
              <td style="padding: 32px 32px 24px 32px; background-color: #ffffff;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                  <tr>
                    <td>
                      <span style="font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-size: 20px; font-weight: 700; color: #002045; letter-spacing: -0.02em;">
                        Next<span style="color: #875200;">Stop</span>
                      </span>
                    </td>
                    <td align="right">
                      <span style="font-family: 'Inter', Arial, sans-serif; font-size: 12px; font-weight: 600; color: #74777f; letter-spacing: 0.05em; text-transform: uppercase;">
                        🌐 Explorer Club
                      </span>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding: 0 32px 32px 32px; background-color: #ffffff;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #002045; border-radius: 12px; box-shadow: 0 12px 32px rgba(26, 54, 93, 0.12);">
                  <tr>
                    <td style="padding: 40px 32px; text-align: center;">
                      <div style="background-color: rgba(255, 255, 255, 0.12); display: inline-block; padding: 8px 16px; border-radius: 9999px; margin-bottom: 24px;">
                        <span style="font-family: 'Inter', Arial, sans-serif; font-size: 12px; font-weight: 600; color: #ffffff; letter-spacing: 0.05em; text-transform: uppercase;">
                          🧭 Your Passport Is Ready
                        </span>
                      </div>
                      <h1 style="margin: 0; font-family: 'Montserrat', Helvetica, Arial, sans-serif; color: #ffffff; font-size: 32px; font-weight: 700; line-height: 1.2; letter-spacing: -0.02em;">
                        You're on the map.
                      </h1>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding: 16px 32px 32px 32px; background-color: #ffffff;">
                <p style="margin: 0 0 16px 0; font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-size: 24px; font-weight: 600; line-height: 1.3; color: #181c1e;">
                  Adventure without the friction.
                </p>
                <p style="margin: 0 0 32px 0; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.6; font-weight: 400; color: #43474e;">
                  Welcome to NextStop. You've officially secured early access to tailored global itineraries, premium booking drops, and real-time hidden gem alerts. We’ve meticulously handled the logistics—all that’s left for you is to choose a destination.
                </p>
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;">
                  <tr>
                    <td align="center" style="border-radius: 8px; background-color: #875200; box-shadow: 0 4px 20px rgba(135, 82, 0, 0.25);">
                      <a href="{base_url}" target="_blank" style="border: 1px solid #875200; border-radius: 8px; color: #ffffff; display: inline-block; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 600; padding: 14px 32px; text-decoration: none; min-height: 48px; box-sizing: border-box;">
                        Set Up Your First Trip
                      </a>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding: 0 32px 48px 32px; background-color: #ffffff;">
                <div style="background-color: #f1f4f6; border-radius: 12px; padding: 24px; border: 1px solid #e0e3e5;">
                  <p style="margin: 0 0 16px 0; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; color: #181c1e; text-transform: uppercase; letter-spacing: 0.05em;">
                    What NextStop delivers:
                  </p>
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                    <tr>
                      <td valign="top" style="padding-bottom: 16px; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 16px; color: #875200; width: 28px;">📍</td>
                      <td valign="top" style="padding-bottom: 16px; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.5; color: #43474e;">
                        <strong>Curated Horizons:</strong> Tailored itineraries matching your precise travel style, curated by regional experts.
                      </td>
                    </tr>
                    <tr>
                      <td valign="top" style="padding-bottom: 16px; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 16px; color: #875200; width: 28px;">📍</td>
                      <td valign="top" style="padding-bottom: 16px; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.5; color: #43474e;">
                        <strong>Priority Alerts:</strong> Instant updates on fare drops, route availability, and local travel conditions.
                      </td>
                    </tr>
                    <tr>
                      <td valign="top" style="font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 16px; color: #875200; width: 28px;">📍</td>
                      <td valign="top" style="font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.5; color: #43474e;">
                        <strong>Verified Stays:</strong> Access crowdsourced accommodation lists that guarantee quality without sacrificing adventure.
                      </td>
                    </tr>
                  </table>
                </div>
              </td>
            </tr>
            <tr>
              <td style="background-color: #ebeef0; padding: 48px 32px; text-align: center; border-top: 1px solid #e0e3e5;">
                <p style="margin: 0 0 8px 0; font-family: 'Inter', Helvetica, Arial, sans-serif; font-size: 12px; line-height: 1.5; color: #74777f;">
                  © 2026 NextStop Technologies Inc. All rights reserved.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </div>
      """
  
  json_data = {
    'recipients': email,
    'subject': subject,
    'body': html_message
  }

  try:
    from django.conf import settings
    response = requests.post(
      settings.MAIL_SERVICE_URL,
      json=json_data,
      timeout=10,
    )
    return response.ok
  except requests.RequestException:
    return False

def packages_page(request):
  data = packages_page_data_inJSON(request)
  is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
  form = FutureUpdateForm()
  success = False

  if request.method == 'POST':
    form = FutureUpdateForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      if FutureUpdate.objects.filter(email=email).exists():
        form.add_error('email', 'This email is already subscribed.')
      elif send_future_request_success_mail(request, email):
        form.save()
        success = True
        if is_ajax:
          return JsonResponse({'success': True})
      else:
        form.add_error(None, 'Unable to send the confirmation email. Please try again.')
        if is_ajax:
          return JsonResponse(
            {'success': False, 'errors': form.errors.get_json_data()},
            status=502,
          )

    if is_ajax:
      return JsonResponse(
        {'success': False, 'errors': form.errors.get_json_data()},
        status=400,
      )

  return render(request, 'packages/packages_page.html', {
    'package_data': data,
    'form': form,
    'success': success,
  })

def packages_detail_page(request, slug):
  data = package_detail_data_inJSON(request, slug)
  return render(request, 'packages/packages_detail_page.html', {
    'packages_data': data,
  })
