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
class Gallery(models.Model):
  # Image Type Choices
  IMAGE_TYPE_CHOICES = [
    ('mountain', 'Mountains'),
    ('forest', 'Forest'),
    ('river', 'River'),
    ('lake', 'Lake'),
    ('ocean', 'Ocean'),
    ('desert', 'Desert'),
    ('city', 'City'),
    ('town', 'Town'),
    ('village', 'Village'),
    ('countryside', 'Countryside'),
    ('beach', 'Beach'),
    ('island', 'Island'),
    ('waterfall', 'Waterfall'),
    ('canyon', 'Canyon'),
    ('cave', 'Cave'),
    ('volcano', 'Volcano'),
    ('glacier', 'Glacier'),
    ('park', 'Park'),
    ('garden', 'Garden'),
    ('zoo', 'Zoo'),
    ('museum', 'Museum'),
    ('gallery', 'Gallery'),
    ('monument', 'Monument'),
    ('historical', 'Historical'),
    ('religious', 'Religious'),
    ('cultural', 'Cultural'),
    ('traditional', 'Traditional'),
    ('modern', 'Modern'),
    ('architectural', 'Architectural'),
    ('natural', 'Natural'),
    ('artificial', 'Artificial'),
    ('commercial', 'Commercial'),
    ('industrial', 'Industrial'),
    ('residential', 'Residential'),
    ('agricultural', 'Agricultural'),
    ('wildlife', 'Wildlife'),
    ('bird', 'Bird'),
    ('animal', 'Animal'),
    ('plant', 'Plant'),
    ('flower', 'Flower'),
    ('tree', 'Tree'),
  ]

  image = models.ImageField(upload_to='gallery/images/', max_length=500)
  place = models.CharField(max_length=100)
  description = models.CharField(max_length=250)
  type = models.CharField(max_length=100, choices=IMAGE_TYPE_CHOICES)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.place} Gallery **** {self.type} **** {self.created_at}'

  def save(self, *args, **kwargs):
    if self.pk:
      try:
        old_instance = Gallery.objects.get(pk=self.pk)
        if old_instance.image and self.image != old_instance.image:
          delete_from_cloudinary(old_instance.image)
      except Gallery.DoesNotExist:
        pass
    
    if self.image and not str(self.image).startswith('http'):
      upload_result = cloudinary.uploader.upload(self.image, folder='gallery/images')
      self.image = upload_result.get('secure_url')

    super().save(*args, **kwargs)

@receiver(pre_delete, sender=Gallery)
def delete_gallery_image_from_cloudinary(sender, instance, **kwargs):
    if instance.image:
        delete_from_cloudinary(instance.image)
