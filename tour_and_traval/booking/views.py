from django.contrib.auth import base_user
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from datetime import datetime, timedelta

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from .models import Booking
# pyrefly: ignore [missing-import]
from packages.models import Packages, PackagesDepartureDate

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def send_ticket_on_mail(booking):
  user_name = booking.user.profile.full_name if hasattr(booking.user, 'profile') and booking.user.profile.full_name else booking.user.username
  user_email = booking.user.email
  
  template = f"""
  <div
    style="
      margin: 0;
      padding: 0;
      background-color: #f7fafc;
      font-family: &quot;Inter&quot;, Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      width: 100% !important;
    "
  >
    <table
      role="presentation"
      width="100%"
      cellspacing="0"
      cellpadding="0"
      border="0"
      style="background-color: #f7fafc; padding: 48px 20px"
    >
      <tr>
        <td align="center">
          <table
            role="presentation"
            width="100%"
            max-width="600"
            cellspacing="0"
            cellpadding="0"
            border="0"
            style="
              max-width: 600px;
              width: 100%;
              background-color: #ffffff;
              border-radius: 16px;
              overflow: hidden;
              box-shadow: 0 4px 20px rgba(26, 54, 93, 0.05);
            "
          >
            <tr>
              <td
                height="6"
                style="
                  background-color: #875200;
                  line-height: 6px;
                  font-size: 6px;
                "
              >
                &nbsp;
              </td>
            </tr>
            <tr>
              <td
                style="padding: 32px 32px 20px 32px; background-color: #ffffff"
              >
                <table
                  role="presentation"
                  width="100%"
                  cellspacing="0"
                  cellpadding="0"
                  border="0"
                >
                  <tr>
                    <td>
                      <span
                        style="
                          font-family:
                            &quot;Montserrat&quot;, Helvetica, Arial, sans-serif;
                          font-size: 22px;
                          font-weight: 700;
                          color: #002045;
                          letter-spacing: -0.02em;
                        "
                      >
                        Next<span style="color: #875200">Stop</span>
                      </span>
                    </td>
                    <td align="right">
                      <span
                        style="
                          font-family: &quot;Inter&quot;, Arial, sans-serif;
                          font-size: 12px;
                          font-weight: 600;
                          color: #74777f;
                          letter-spacing: 0.05em;
                          text-transform: uppercase;
                        "
                      >
                        Booking Confirmed ✓
                      </span>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="padding: 0 32px 24px 32px; background-color: #ffffff">
                <table
                  role="presentation"
                  width="100%"
                  cellspacing="0"
                  cellpadding="0"
                  border="0"
                  style="background-color: #002045; border-radius: 12px"
                >
                  <tr>
                    <td style="padding: 32px 24px; text-align: center">
                      <p
                        style="
                          margin: 0 0 8px 0;
                          font-family: &quot;Inter&quot;, Arial, sans-serif;
                          font-size: 13px;
                          font-weight: 600;
                          color: #86a0cd;
                          letter-spacing: 0.05em;
                          text-transform: uppercase;
                        "
                      >
                        Ticket Secured
                      </p>
                      <h1
                        style="
                          margin: 0;
                          font-family:
                            &quot;Montserrat&quot;, Helvetica, Arial, sans-serif;
                          color: #ffffff;
                          font-size: 28px;
                          font-weight: 700;
                          line-height: 1.2;
                        "
                      >
                        Pack Your Bags!
                      </h1>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td
                style="padding: 8px 32px 24px 32px; background-color: #ffffff"
              >
                <table
                  role="presentation"
                  width="100%"
                  cellspacing="0"
                  cellpadding="0"
                  border="0"
                  style="
                    border: 1px solid #c4c6cf;
                    border-radius: 12px;
                    padding: 20px;
                  "
                >
                  <tr>
                    <td style="padding-bottom: 12px">
                      <span
                        style="
                          font-family: &quot;Inter&quot;, sans-serif;
                          font-size: 12px;
                          font-weight: 700;
                          color: #875200;
                          letter-spacing: 0.05em;
                          text-transform: uppercase;
                        "
                      >
                        {booking.package.location}
                      </span>
                      <h2
                        style="
                          margin: 4px 0 8px 0;
                          font-family:
                            &quot;Montserrat&quot;, Helvetica, Arial, sans-serif;
                          font-size: 20px;
                          font-weight: 700;
                          color: #002045;
                        "
                      >
                        {booking.package.main_title}
                      </h2>
                    </td>
                  </tr>
                  <tr>
                    <td
                      style="
                        border-top: 1px dashed #e0e3e5;
                        padding-top: 12px;
                        font-family:
                          &quot;Inter&quot;, Helvetica, Arial, sans-serif;
                        font-size: 14px;
                        color: #43474e;
                      "
                    >
                      📅 <strong>{booking.start_date.strftime('%d %b %Y')}</strong> &nbsp;•&nbsp; 🕒
                      <strong>{booking.package.total_days} Days, {booking.package.total_nights} Nights</strong>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="padding: 0 32px 32px 32px; background-color: #ffffff">
                <table
                  role="presentation"
                  width="100%"
                  cellspacing="0"
                  cellpadding="0"
                  border="0"
                  style="
                    background-color: #f1f4f6;
                    border-radius: 12px;
                    padding: 24px;
                  "
                >
                  <tr>
                    <td valign="top" style="padding-bottom: 20px; width: 50%">
                      <span
                        style="
                          display: block;
                          font-family: &quot;Inter&quot;, sans-serif;
                          font-size: 11px;
                          font-weight: 600;
                          color: #74777f;
                          text-transform: uppercase;
                          letter-spacing: 0.05em;
                          margin-bottom: 4px;
                        "
                        >Primary Traveler</span
                      >
                      <strong
                        style="font-size: 15px; color: #181c1e; display: block"
                        >{user_name}</strong
                      >
                      <span style="font-size: 13px; color: #43474e"
                        >{user_email}</span
                      >
                    </td>
                    <td
                      valign="top"
                      align="right"
                      style="padding-bottom: 20px; width: 50%"
                    >
                      <span
                        style="
                          display: block;
                          font-family: &quot;Inter&quot;, sans-serif;
                          font-size: 11px;
                          font-weight: 600;
                          color: #74777f;
                          text-transform: uppercase;
                          letter-spacing: 0.05em;
                          margin-bottom: 4px;
                        "
                        >Booking Ticket Number</span
                      >
                      <strong
                        style="
                          font-size: 18px;
                          color: #875200;
                          font-family: &quot;Montserrat&quot;, sans-serif;
                        "
                        >{booking.ticket_number}</strong
                      >
                    </td>
                  </tr>

                  <tr>
                    <td valign="top" style="width: 50%">
                      <span
                        style="
                          display: block;
                          font-family: &quot;Inter&quot;, sans-serif;
                          font-size: 11px;
                          font-weight: 600;
                          color: #74777f;
                          text-transform: uppercase;
                          letter-spacing: 0.05em;
                          margin-bottom: 4px;
                        "
                        >Travel Party</span
                      >
                      <strong style="font-size: 15px; color: #181c1e"
                        >{booking.number_of_persons} {'Adult' if booking.number_of_persons == 1 else 'Adults'}</strong
                      >
                    </td>
                    <td valign="top" align="right" style="width: 50%">
                      <span
                        style="
                          display: block;
                          font-family: &quot;Inter&quot;, sans-serif;
                          font-size: 11px;
                          font-weight: 600;
                          color: #74777f;
                          text-transform: uppercase;
                          letter-spacing: 0.05em;
                          margin-bottom: 4px;
                        "
                        >Transaction ID</span
                      >
                      <span
                        style="
                          font-size: 12px;
                          font-family: monospace;
                          color: #43474e;
                          word-break: break-all;
                        "
                        >{booking.UTR_number}</span
                      >
                    </td>
                  </tr>

                  <tr>
                    <td
                      colspan="2"
                      style="
                        padding-top: 20px;
                        border-top: 1px solid #e0e3e5;
                        margin-top: 20px;
                      "
                    >
                      <table
                        role="presentation"
                        cellspacing="0"
                        cellpadding="0"
                        border="0"
                        align="right"
                      >
                        <tr>
                          <td
                            style="
                              background-color: #e8f5e9;
                              padding: 6px 14px;
                              border-radius: 20px;
                              border: 1px solid #c8e6c9;
                            "
                          >
                            <span
                              style="
                                font-family: &quot;Inter&quot;, sans-serif;
                                font-size: 12px;
                                font-weight: 700;
                                color: #2e7d32;
                                text-transform: uppercase;
                                letter-spacing: 0.05em;
                              "
                              >● Confirmed</span
                            >
                          </td>
                        </tr>
                      </table>
                      <span
                        style="
                          font-family: &quot;Inter&quot;, sans-serif;
                          font-size: 14px;
                          color: #43474e;
                          line-height: 32px;
                        "
                        >Reservation Status:</span
                      >
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="padding: 0 32px 40px 32px; background-color: #ffffff">
                <table
                  role="presentation"
                  width="100%"
                  cellspacing="0"
                  cellpadding="0"
                  border="0"
                  style="
                    border: 2px solid #002045;
                    border-radius: 12px;
                    padding: 20px 24px;
                  "
                >
                  <tr>
                    <td
                      style="
                        font-family: &quot;Montserrat&quot;, sans-serif;
                        font-size: 15px;
                        font-weight: 700;
                        color: #002045;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                      "
                    >
                      Total Amount Paid
                    </td>
                    <td
                      align="right"
                      style="
                        font-family: &quot;Montserrat&quot;, sans-serif;
                        font-size: 24px;
                        font-weight: 700;
                        color: #002045;
                      "
                    >
                      ₹{booking.amount}
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td
                style="
                  background-color: #ebeef0;
                  padding: 40px 32px;
                  text-align: center;
                  border-top: 1px solid #e0e3e5;
                "
              >
                <p
                  style="
                    margin: 0 0 16px 0;
                    font-family:
                      &quot;Inter&quot;, Helvetica, Arial, sans-serif;
                    font-size: 12px;
                    font-weight: 600;
                    color: #43474e;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                  "
                >
                  Need help with your journey?
                </p>
                <p
                  style="
                    margin: 0 0 24px 0;
                    font-family:
                      &quot;Inter&quot;, Helvetica, Arial, sans-serif;
                    font-size: 14px;
                    color: #74777f;
                  "
                >
                  Contact our 24/7 Premium Concierge desk straight through the
                  NextStop app.
                </p>
                <hr
                  style="
                    border: 0;
                    border-top: 1px solid #c4c6cf;
                    margin-bottom: 24px;
                  "
                />
                <p
                  style="
                    margin: 0 0 4px 0;
                    font-family:
                      &quot;Inter&quot;, Helvetica, Arial, sans-serif;
                    font-size: 11px;
                    color: #74777f;
                  "
                >
                  © 2026 NextStop Technologies Inc. All rights reserved.
                </p>
                <p
                  style="
                    margin: 0;
                    font-family:
                      &quot;Inter&quot;, Helvetica, Arial, sans-serif;
                    font-size: 11px;
                    color: #74777f;
                  "
                >
                  Ranchi Jharkhand 835103
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </div>
  """

  subject = f"NextStop - Booking Confirmed - {booking.package.main_title}"
  text_content = strip_tags(template)
  
  sender_email = getattr(settings, 'EMAIL_HOST_USER', 'noreply@nextstop.com')
  if not sender_email:
    sender_email = 'noreply@nextstop.com'
    
  msg = EmailMultiAlternatives(subject, text_content, sender_email, [user_email])
  msg.attach_alternative(template, "text/html")
  try:
    msg.send()
  except Exception as e:
    print(f"Failed to send email: {e}")


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
  
  # Check seat availability before creating pending booking or razorpay order
  departure = PackagesDepartureDate.objects.filter(
    package=package_obj, 
    departure_date=parsed_start_date
  ).first()
  
  if not departure:
    messages.error(request, "Invalid departure date selected.")
    return redirect('packages_detail_page', packages_id=package_id)
    
  if departure.available_seats < persons_count:
    messages.error(request, f"Sorry, only {departure.available_seats} seats are available for this date.")
    return redirect('packages_detail_page', packages_id=package_id)
  
  end_date = parsed_start_date + timedelta(days=package_obj.total_days)

  # Check if a pending booking already exists for these details
  booking = Booking.objects.filter(
    user=request.user,
    package=package_obj,
    payment_status='pending',
    status='pending',
    number_of_persons=persons_count,
    start_date=parsed_start_date,
  ).first()

  if booking:
    # Update total cost and end date in case pricing or duration changed
    booking.amount = total
    booking.total_cost = total
    booking.end_date = end_date
    booking.save()
  else:
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
  
  

  image_obj = package_obj.images.first()
  image_url = str(image_obj.image) if image_obj and image_obj.image and str(image_obj.image).startswith('http') else (image_obj.image.url if image_obj and image_obj.image else '')
  
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
      
      if booking.payment_status != 'paid':
        booking.payment_status = 'paid'
        booking.status = 'confirmed'
        booking.UTR_number = razorpay_payment_id
        booking.ticket_number = f"NEXT{booking.id}"
        booking.save()
        
        # Deduct available seats
        departure = PackagesDepartureDate.objects.filter(
          package=booking.package, 
          departure_date=booking.start_date
        ).first()
        
        if departure:
          departure.available_seats -= booking.number_of_persons
          if departure.available_seats < 0:
            departure.available_seats = 0
          departure.save()
          
        # Send confirmation email
        send_ticket_on_mail(booking)
      
      return redirect('booking_success_page', booking_id=booking.id, payment_id=razorpay_payment_id, transection_id=razorpay_order_id, package_id=booking.package.id)
      
    except razorpay.errors.SignatureVerificationError:
      return HttpResponseBadRequest("Payment verification failed")
  return HttpResponseBadRequest("Invalid request method")

@login_required
def booking_success_page(request, booking_id: int, payment_id: str, transection_id: str, package_id: int):
  package_obj = get_object_or_404(Packages, id=package_id)
  booking_obj = get_object_or_404(Booking, id=booking_id)
  
  image_obj = package_obj.images.first()
  image_url = str(image_obj.image) if image_obj and image_obj.image and str(image_obj.image).startswith('http') else (image_obj.image.url if image_obj and image_obj.image else '')
  
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

@login_required
def cancel_pending_booking(request, booking_id: int):
  booking_obj = get_object_or_404(Booking, id=booking_id)
  booking_obj.payment_status = 'cancelled'
  booking_obj.status = 'cancelled'
  booking_obj.save()
  return redirect('user_page')

