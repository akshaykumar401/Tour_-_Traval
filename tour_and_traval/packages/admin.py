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
  fields = ("image", "thumbnail_preview", "created_at")
  readonly_fields = ("thumbnail_preview", "created_at")
  show_change_link = True
  verbose_name = "Gallery image"
  verbose_name_plural = "Gallery"

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
  fields = ("feature", "created_at")
  readonly_fields = ("created_at",)
  verbose_name = "Package feature"
  verbose_name_plural = "Included features"


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
  fields = ("departure_date", "total_seats", "available_seats", "created_at")
  readonly_fields = ("created_at",)
  verbose_name = "Departure"
  verbose_name_plural = "Available departures"


@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
  list_display = (
    "package_name",
    "location_badge",
    "tag_badge",
    "duration",
    "formatted_price",
    "max_people",
    "image_count",
    "created_at",
  )
  list_filter = ("tag_line", "created_at")
  search_fields = ("main_title", "mini_title", "location", "description")
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
      "fields": ("main_title", "mini_title", "tag_line", "location"),
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
      '<span class="package-admin-title">{}</span><span class="package-admin-subtitle">{}</span>',
      obj.main_title,
      obj.mini_title,
    )

  @admin.display(description="Destination", ordering="location")
  def location_badge(self, obj):
    return format_html('<span class="package-admin-location">⌖ {}</span>', obj.location)

  @admin.display(description="Style", ordering="tag_line")
  def tag_badge(self, obj):
    return format_html('<span class="package-admin-tag">{}</span>', obj.get_tag_line_display())

  @admin.display(description="Duration", ordering="total_days")
  def duration(self, obj):
    return format_html('<strong>{}</strong> days <span class="package-admin-muted">/ {} nights</span>', obj.total_days, obj.total_nights)

  @admin.display(description="Starting price", ordering="starting_price")
  def formatted_price(self, obj):
    price = f"₹{obj.starting_price:,.2f}"
    return format_html('<span class="package-admin-price">{}</span>', price)

  @admin.display(description="Images", ordering="_image_count")
  def image_count(self, obj):
    return format_html('<span class="package-admin-count">{}</span>', obj._image_count)


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
      return format_html(
        '<img src="{}" alt="Package image" width="420">',
        obj.image.url,
      )
    return "—"
