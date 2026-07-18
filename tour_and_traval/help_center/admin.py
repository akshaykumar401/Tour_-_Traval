from django.urls import path
from django.contrib import admin
from .models import Feedback, FutureUpdate, SendEmailToAll

from .admin_views import SendMailAdminView
from django.shortcuts import redirect

# Register your models here.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
  list_display = ('full_name', 'email', 'reating', 'created_at')
  list_filter = ('reating', 'created_at')
  search_fields = ('full_name', 'email', 'message')

@admin.register(FutureUpdate)
class FutureUpdateAdmin(admin.ModelAdmin):
  list_display = ('email', 'created_at')
  list_filter = ('created_at',)
  search_fields = ('email',)

@admin.register(SendEmailToAll)
class SendEmailToAllAdmin(admin.ModelAdmin):
  def changelist_view(self, request, extra_context=None):
    return redirect('admin:send-mail')


def get_admin_urls(urls):
  def get_urls():
    return [
      path(
        "send-emails/",
        admin.site.admin_view(SendMailAdminView.as_view()),
        name="send-mail",
      ),
    ] + urls()
  return get_urls

admin.site.get_urls = get_admin_urls(admin.site.get_urls)