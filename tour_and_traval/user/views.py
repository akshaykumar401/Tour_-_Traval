from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from .models import User_Profile

# Create your views here.
def user_page(request):
  if not request.user.is_authenticated:
    return redirect('login')
  return render(request, "user/user_page.html")

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