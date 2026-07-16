from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import (
  Packages,
  PackagesDepartureDate,
  PackagesFeatures,
  PackagesImage,
  PackagesItinerary,
)


class PackagesImageInline(admin.TabularInline):
  model = PackagesImage
  extra = 1
  max_num = 4
  validate_max = True
  fields = ("image", "thumbnail_preview", "created_at")
  readonly_fields = ("thumbnail_preview", "created_at")
  show_change_link = True
  verbose_name = "Gallery image"
  verbose_name_plural = "Gallery (maximum 4 images)"

  @admin.display(description="Preview")
  def thumbnail_preview(self, obj):
    if obj and obj.image:
      return format_html(
        '<img src="{}" alt="Package image" width="90" height="60">',
        obj.image.url,
      )
    return "—"


class PackagesFeaturesInline(admin.TabularInline):
  model = PackagesFeatures
  extra = 1
  max_num = 4
  validate_max = True
  fields = ("feature", "created_at")
  readonly_fields = ("created_at",)
  verbose_name = "Package feature"
  verbose_name_plural = "Included features (maximum 4)"


class PackagesItineraryInline(admin.StackedInline):
  model = PackagesItinerary
  extra = 0
  fields = ("day_number", "title", "description", "created_at")
  readonly_fields = ("created_at",)
  verbose_name = "Itinerary day"
  verbose_name_plural = "Day-by-day itinerary"


class PackagesDepartureDateInline(admin.TabularInline):
  model = PackagesDepartureDate
  extra = 1
  max_num = 2
  validate_max = True
  fields = ("departure_date", "total_seats", "available_seats", "created_at")
  readonly_fields = ("created_at",)
  verbose_name = "Departure"
  verbose_name_plural = "Available departures (maximum 2)"


@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
  list_display = (
    "package_name",
    "location_badge",
    "category",
    "tag_badge",
    "duration",
    "formatted_price",
    "max_people",
    "image_count",
    "created_at",
  )
  list_filter = ("category", "tag_line", "created_at")
  search_fields = ("main_title", "mini_title", "category", "location", "description")
  ordering = ("-created_at",)
  date_hierarchy = "created_at"
  list_per_page = 25
  list_display_links = ("package_name",)
  save_on_top = True
  show_full_result_count = True
  readonly_fields = ("created_at",)
  inlines = (
    PackagesImageInline,
    PackagesFeaturesInline,
    PackagesItineraryInline,
    PackagesDepartureDateInline,
  )
  fieldsets = (
    ("Package identity", {
      "fields": ("main_title", "mini_title", "category", "tag_line", "location"),
      "description": "The details travellers see when browsing your tours.",
    }),
    ("Trip details", {
      "fields": (("total_days", "total_nights"), ("starting_price", "max_people")),
    }),
    ("About this trip", {"fields": ("description",)}),
    ("Record information", {"fields": ("created_at",), "classes": ("collapse",)}),
  )

  def get_queryset(self, request):
    return super().get_queryset(request).annotate(_image_count=Count("images"))

  @admin.display(description="Package", ordering="main_title")
  def package_name(self, obj):
    return format_html(
      '<span>{}</span><br><small>{}</small>',
      obj.main_title,
      obj.mini_title,
    )

  @admin.display(description="Destination", ordering="location")
  def location_badge(self, obj):
    return obj.location

  @admin.display(description="Style", ordering="tag_line")
  def tag_badge(self, obj):
    return obj.get_tag_line_display()

  @admin.display(description="Duration", ordering="total_days")
  def duration(self, obj):
    return f"{obj.total_days} days / {obj.total_nights} nights"

  @admin.display(description="Starting price", ordering="starting_price")
  def formatted_price(self, obj):
    return f"₹{obj.starting_price:,.2f}"

  @admin.display(description="Images", ordering="_image_count")
  def image_count(self, obj):
    return obj._image_count


@admin.register(PackagesImage)
class PackagesImageAdmin(admin.ModelAdmin):
  list_display = ("thumbnail_preview", "package", "created_at")
  list_filter = ("created_at",)
  search_fields = ("package__main_title", "package__location")
  ordering = ("-created_at",)
  list_select_related = ("package",)
  date_hierarchy = "created_at"
  save_on_top = True
  readonly_fields = ("image_preview", "created_at")
  fields = ("package", "image", "image_preview", "created_at")
  autocomplete_fields = ("package",)

  @admin.display(description="Image")
  def thumbnail_preview(self, obj):
    if obj.image:
      return format_html(
        '<img src="{}" alt="Package image" width="90" height="60">',
        obj.image.url,
      )
    return "—"

  @admin.display(description="Image preview")
  def image_preview(self, obj):
    if obj and obj.image:
      return format_html('<img src="{}" alt="Package image" width="420">', obj.image.url)
    return "—"
