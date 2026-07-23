from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import cloudinary.uploader

def delete_from_cloudinary(url):
  if url and str(url).startswith('http'):
    try:
      parts = str(url).split('/upload/')
      if len(parts) > 1:
        path = parts[1]
        if path.startswith('v') and '/' in path:
          first_slash = path.find('/')
          if path[1:first_slash].isdigit():
            path = path[first_slash+1:]
          public_id = path.rsplit('.', 1)[0]
          cloudinary.uploader.destroy(public_id)
    except Exception as e:
      print(f"Error deleting image from Cloudinary: {e}")
      
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
  image = models.ImageField(upload_to='packages_images/', max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)

  def save(self, *args, **kwargs):
    if self.pk:
      try:
        old_instance = PackagesImage.objects.get(pk=self.pk)
        if old_instance.image and self.image != old_instance.image:
          delete_from_cloudinary(old_instance.image)
      except PackagesImage.DoesNotExist:
        pass
    
    if self.image and not str(self.image).startswith('http'):
      upload_result = cloudinary.uploader.upload(self.image.file, folder='packages_images')
      self.image = upload_result.get('secure_url')

    super().save(*args, **kwargs)

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

@receiver(pre_delete, sender=PackagesImage)
def delete_packages_image_from_cloudinary(sender, instance, **kwargs):
    if instance.image:
        delete_from_cloudinary(instance.image)
