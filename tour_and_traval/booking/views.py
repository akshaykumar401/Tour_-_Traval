import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from datetime import datetime, timedelta

from .models import Booking
# pyrefly: ignore [missing-import]
from packages.models import Packages

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def booking_page(request):
  return render(request, "booking/booking_page.html")

@login_required
def payment_page(request, package_id: int, start_date: str, persons: str):
  package_obj = get_object_or_404(Packages, id=package_id)
  
  try:
    persons_count = int(persons)
  except ValueError:
    persons_count = 1

  base_fare = package_obj.starting_price * persons_count
  
  # Calculate taxes (e.g. 5% + ₹250 convenience fee)
  taxes = int(base_fare * 0.05 + 250)
  total = base_fare + taxes
  
  # Parse start_date and calculate end_date
  try:
    parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
  except ValueError:
    parsed_start_date = datetime.now().date()
  
  end_date = parsed_start_date + timedelta(days=package_obj.total_days)

  # Create a pending Booking
  booking = Booking.objects.create(
    user=request.user,
    package=package_obj,
    payment_status='pending',
    status='pending',
    amount=total,
    total_cost=total,
    number_of_persons=persons_count,
    start_date=parsed_start_date,
    end_date=end_date,
  )

  # Create Razorpay Order
  razorpay_order = razorpay_client.order.create({
    "amount": int(100), # Amount in paise
    "currency": "INR",
    "receipt": f"booking_{booking.id}",
    "payment_capture": "1"
  })
  
  # Store order_id in ticket_number temporarily to retrieve in verify
  booking.ticket_number = razorpay_order['id']
  booking.save()

  image_obj = package_obj.images.first()
  image_url = image_obj.image.url if image_obj and image_obj.image else ''
  
  package = {
    "name": package_obj.main_title,
    "price": base_fare,
    "duration": f"{package_obj.total_days} Days, {package_obj.total_nights} Nights",
    "image": image_url,
  }
  
  return render(request, "booking/payment_page.html", {
    "package": package,
    "taxes": taxes,
    "total": total,
    "package_id": package_id,
    "persons": persons_count,
    "start_date": start_date,
    "razorpay_order_id": razorpay_order['id'],
    "razorpay_amount": int(100),
    "razorpay_key_id": settings.RAZORPAY_KEY_ID,
    "booking_id": booking.id,
  })

@csrf_exempt
def payment_verify(request):
  if request.method == "POST":
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')
    booking_id = request.POST.get('booking_id', '')
    
    try:
      # Verify signature
      razorpay_client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
      })
      
      # Payment is verified successfully
      booking = get_object_or_404(Booking, id=booking_id)
      booking.payment_status = 'paid'
      booking.status = 'confirmed'
      booking.UTR_number = razorpay_payment_id
      booking.save()
      
      return redirect('booking_success_page', booking_id=booking.id, payment_id=razorpay_payment_id, transection_id=razorpay_order_id, package_id=booking.package.id)
      
    except razorpay.errors.SignatureVerificationError:
      return HttpResponseBadRequest("Payment verification failed")
  return HttpResponseBadRequest("Invalid request method")


@login_required
def booking_success_page(request, booking_id: int, payment_id: str, transection_id: str, package_id: int):
  package_obj = get_object_or_404(Packages, id=package_id)
  booking_obj = get_object_or_404(Booking, id=booking_id)
  
  image_obj = package_obj.images.first()
  image_url = image_obj.image.url if image_obj and image_obj.image else ''
  
  package = {
    "name": package_obj.main_title,
    "price": package_obj.starting_price,
    "duration": f"{package_obj.total_days} Days, {package_obj.total_nights} Nights",
    "image": image_url,
  }

  return render(request, "booking/booking_success_page.html", {
    "booking": booking_obj,
    "booking_id": booking_id,
    "payment_id": payment_id,
    "transection_id": transection_id,
    "package": package,
  })