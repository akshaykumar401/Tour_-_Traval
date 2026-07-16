from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserProfileForm, UpdateUserProfilePhotoForm
from django.contrib.auth import login
from .models import User_Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# pyrefly: ignore [missing-import]
from booking.models import Booking

def user_data_dict(request):
  user = request.user
  user_profile_data = User_Profile.objects.get(user=user)
  # Filtring the booking as per start_date
  user_bookings = Booking.objects.filter(user=user).order_by('start_date')
  my_booking = []
  for booking in user_bookings:
    booking_dict = {
      "id": booking.id,
      "ticket_number": booking.ticket_number,
      "package_image": booking.package.images.first().image.url if booking.package.images.exists() else None,
      "package": booking.package.mini_title,
      "number_of_persons": booking.number_of_persons,
      "start_date": booking.start_date,
      "total_cost": booking.total_cost,
      "payment_status": booking.payment_status,
      "status": booking.status,
      "UTR_number": booking.UTR_number,
      "amount": booking.amount,
      "updated_at": booking.updated_at,
      "created_at": booking.created_at,
      "package_id": booking.package.id,
    }
    my_booking.append(booking_dict)


  # Formatting the User Data.
  return {
    'email': user.email,
    'full_name': user_profile_data.full_name,
    'phone': user_profile_data.phone,
    'address': user_profile_data.address,
    'image': user_profile_data.image.url if user_profile_data.image else None,
    'username': user.username,
    'date_joined': user.date_joined,
    "my_booking": my_booking,
  }

# Create your views here.
@login_required
def user_page(request):
  if not request.user.is_authenticated:
    return redirect('login')
  
  user_profile = User_Profile.objects.get(user=request.user)
  
  photo_form = UpdateUserProfilePhotoForm()
  profile_form = UserProfileForm(initial={
    'full_name': user_profile.full_name,
    'phone_number': user_profile.phone,
    'address': user_profile.address
  })
  
  # Handle form submission for updating user profile photo
  if request.method == 'POST' and 'image' in request.FILES:
    photo_form = UpdateUserProfilePhotoForm(request.POST, request.FILES)
    if photo_form.is_valid():
      user_profile.image = photo_form.cleaned_data['image']
      user_profile.save()
      messages.success(request, 'Profile photo updated successfully!')
      return redirect('user_page')
  
  # Handle form submission for updating user profile
  elif request.method == 'POST':
    profile_form = UserProfileForm(request.POST)
    if profile_form.is_valid():
      user_profile.full_name = profile_form.cleaned_data['full_name']
      user_profile.phone = profile_form.cleaned_data['phone_number']
      user_profile.address = profile_form.cleaned_data['address']
      user_profile.save()
      messages.success(request, 'Profile updated successfully!')
      return redirect('user_page')
  
  # Get the formatted user data to pass to the template
  formatted_user_data = user_data_dict(request)
  return render(request, "user/user_page.html", {
    'user_data': formatted_user_data,
    'form': profile_form,
    'form_photo': photo_form
  })

def register(request):
  # if user is logged in, redirect to user_page
  if request.user.is_authenticated:
    return redirect('user_page')

  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password1'])
      user.save()
      User_Profile.objects.create(
        user=user,
        full_name=form.cleaned_data['full_name'],
        phone=form.cleaned_data['phone_number'],
        image=None,
      )
      # Login the user
      login(request, user)
      return redirect('user_page')
  else:
    form = UserRegistrationForm()

  return render(request, 'registration/register.html', {
    'form': form,
  })
  
