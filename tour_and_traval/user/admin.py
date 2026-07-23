from django.contrib import admin
from django.utils.html import format_html
from .models import User_Profile

@admin.register(User_Profile)
class User_ProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'thumbnail_preview', 'get_username', 'full_name', 'phone', 'address')
  search_fields = ('user__username', 'full_name', 'phone', 'address')
  ordering = ('id',)
  
  readonly_fields = ('image_preview',)
  
  fieldsets = (
    ('User Account Info', {
      'fields': ('user',)
    }),
    ('Personal Details', {
      'fields': ('full_name', 'phone', 'address')
    }),
    ('Profile Image', {
      'fields': ('image', 'image_preview')
    }),
  )

  @admin.display(description='Username')
  def get_username(self, obj):
    return obj.user.username

  @admin.display(description='Photo')
  def thumbnail_preview(self, obj):
    if obj.image:
      return format_html(
        '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%; border: 1px solid #ddd;" />',
        obj.image
      )
    return "No Image"

  @admin.display(description='Current Photo')
  def image_preview(self, obj):
    if obj.image:
      return format_html(
        '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd;" />',
        obj.image
      )
    return "No Image"
