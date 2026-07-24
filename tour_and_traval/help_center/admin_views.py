from django.views import View
from django.shortcuts import render, redirect
from django.contrib import admin, messages
import requests

from .models import FutureUpdate


from django.conf import settings
MAIL_SERVICE_URL = settings.MAIL_SERVICE_URL

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
        sent_count = 0
        failed_count = 0

        for recipient in recipient_list:
            try:
                response = requests.post(
                    MAIL_SERVICE_URL,
                    json={
                        'recipients': recipient,
                        'subject': subject,
                        'body': message,
                    },
                    timeout=10,
                )
                response.raise_for_status()
                sent_count += 1
            except requests.RequestException:
                failed_count += 1

        if sent_count:
            messages.success(request, f'Successfully sent email to {sent_count} subscribers.')
        if failed_count:
            messages.error(request, f'Unable to send email to {failed_count} subscribers.')
    else:
        messages.warning(request, "No subscribers found to send email to.")
        
    return redirect('admin:send-mail')
