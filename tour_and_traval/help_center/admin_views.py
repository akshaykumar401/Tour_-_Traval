from django.views import View
from django.shortcuts import render, redirect
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.conf import settings
from .models import FutureUpdate

class SendMailAdminView(View):
  template_name = "admin/send_mail.html"

  def get(self, request):
    future_updates = FutureUpdate.objects.all()
    context = dict(
        admin.site.each_context(request),
        future_updates=future_updates,
        title="Send Mail To All Subscribers",
    )
    return render(request, self.template_name, context)

  def post(self, request):
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    future_updates = FutureUpdate.objects.all()
    
    if not subject and not message:
        messages.error(request, "Both Subject and Message are missing.")
        return redirect('admin:send-mail')
    elif not subject:
        messages.error(request, "Subject is required.")
        return redirect('admin:send-mail')
    elif not message:
        messages.error(request, "Message body is required. (If you wrote one, your browser didn't send it!)")
        return redirect('admin:send-mail')
        
    recipient_list = [update.email for update in future_updates]
    
    if recipient_list:
        try:
            plain_message = "<p>This email contains rich HTML content. Please view it in an HTML-compatible email client.</p>"
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
                html_message=message,
            )
            messages.success(request, f'Successfully sent email to {len(recipient_list)} subscribers.')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
    else:
        messages.warning(request, "No subscribers found to send email to.")
        
    return redirect('admin:send-mail')