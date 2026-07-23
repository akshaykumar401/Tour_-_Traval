from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  phone = models.CharField(max_length=20)
  full_name = models.CharField(max_length=100)
  address = models.CharField(max_length=250, blank=True, null=True, default="")
  image = models.ImageField(upload_to='profile_pics', blank=True, null=True, max_length=500)  

  def __str__(self):
    return f'{self.user.username} Profile'    

