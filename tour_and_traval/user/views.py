from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth import login
from .models import User_Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def user_data_dict(request):
  user = request.user
  user_profile_data = User_Profile.objects.get(user=user)
  
  # Formatting the User Data.
  return {
    'email': user.email,
    'full_name': user_profile_data.full_name,
    'phone': user_profile_data.phone,
    'address': user_profile_data.address,
    'image': user_profile_data.image.url if user_profile_data.image else None,
    'username': user.username,
    'date_joined': user.date_joined,
  }

# Create your views here.
@login_required
def user_page(request):
  if not request.user.is_authenticated:
    return redirect('login')
  
  user_profile = User_Profile.objects.get(user=request.user)
  
  if request.method == 'POST':
    # Handle form submission for updating user profile
    form = UserProfileForm(request.POST)
    if form.is_valid():
      user_profile.full_name = form.cleaned_data['full_name']
      user_profile.phone = form.cleaned_data['phone_number']
      user_profile.address = form.cleaned_data['address']
      user_profile.save()
      messages.success(request, 'Profile updated successfully!')
      return redirect('user_page')
  else:
    form = UserProfileForm(initial={
      'full_name': user_profile.full_name,
      'phone_number': user_profile.phone,
      'address': user_profile.address
    })
  
  # Get the formatted user data to pass to the template
  formatted_user_data = user_data_dict(request)
  return render(request, "user/user_page.html", {
    'user_data': formatted_user_data,
    'form': form
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
  
