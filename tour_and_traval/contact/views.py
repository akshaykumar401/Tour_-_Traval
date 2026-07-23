from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ContactForm

# Create your views here.
def contact_page(request):
  if request.method == "POST":
    form = ContactForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Your message has been sent successfully!")
      return redirect('contact_page')
  else:
    form = ContactForm()
  return render(request, "contact/contact_page.html", {
    'form': form,
  })