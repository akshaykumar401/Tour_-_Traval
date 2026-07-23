from django.contrib import admin
from django.utils.html import format_html
from .models import Gallery

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
  list_display = ('id', 'thumbnail_preview', 'place', 'description', 'type', 'created_at')
  list_filter = ('place', 'type', 'created_at')
  search_fields = ('place', 'description', 'type')
  ordering = ('-created_at',)
  
  readonly_fields = ('image_preview',)

  @admin.display(description='Image')
  def thumbnail_preview(self, obj):
    if obj.image:
      return format_html(
        '<img src="{}" style="width: 50px; height: 35px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
        obj.image
      )
    return "No Image"

  @admin.display(description='Image Preview')
  def image_preview(self, obj):
    if obj.image:
      return format_html(
        '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd;" />',
        obj.image
      )
    return "No Image"

