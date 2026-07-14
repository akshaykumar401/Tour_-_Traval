from django.db import models

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

  image = models.ImageField(upload_to='gallery/images/')
  place = models.CharField(max_length=100)
  description = models.CharField(max_length=250)
  type = models.CharField(max_length=100, choices=IMAGE_TYPE_CHOICES)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.place} Gallery **** {self.type} **** {self.created_at}'

