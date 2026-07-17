from django.contrib import admin
from .models import Feedback, FutureUpdate

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

