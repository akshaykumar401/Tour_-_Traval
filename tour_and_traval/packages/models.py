from django.db import models

# Create your models here.
# Packages Model....
class Packages(models.Model):
  # Tag line ENUM
  TAG_LINE = (
    ('Adventure', 'Adventure'),
    ('Relaxation', 'Relaxation'),
    ('Cultural', 'Cultural'),
    ('Romantic', 'Romantic'),
    ('Family', 'Family'),
    ('Luxury', 'Luxury'),
    ('Budget', 'Budget'),
    ('Best Seller', 'Best Seller'),
    ('None', 'None')
  )
  
  # Category ENUM
  CATEGORY = (
    ('Beach', 'Beach'),
    ('Adventure', 'Adventure'),
    ('Culture', 'Culture'),
    ('Diving', 'Diving')
  )
  
  tag_line = models.CharField(max_length=100, choices=TAG_LINE, default='None')
  category = models.CharField(max_length=100, default='Uncategorized')
  location = models.CharField(max_length=255)
  mini_title = models.CharField(max_length=255)
  total_days = models.IntegerField()
  total_nights = models.IntegerField()
  starting_price = models.FloatField()
  max_people = models.IntegerField()
  main_title = models.CharField(max_length=255)
  description = models.TextField()
  category = models.CharField(max_length=100, choices=CATEGORY)
  created_at = models.DateTimeField(auto_now_add=True)

class PackagesImage(models.Model):
  package = models.ForeignKey(Packages, on_delete=models.CASCADE, related_name='images')
  image = models.ImageField(upload_to='packages_images/')
  created_at = models.DateTimeField(auto_now_add=True)

class PackagesFeatures(models.Model):
  package = models.ForeignKey(Packages, on_delete=models.CASCADE, related_name='features')
  feature = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)

class PackagesItinerary(models.Model):
  package = models.ForeignKey(Packages, on_delete=models.CASCADE, related_name='itineraries')
  day_number = models.IntegerField()
  title = models.CharField(max_length=255)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

class PackagesDepartureDate(models.Model):
  package = models.ForeignKey(Packages, on_delete=models.CASCADE, related_name='departure_dates')
  departure_date = models.DateField()
  total_seats = models.IntegerField()
  available_seats = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)


