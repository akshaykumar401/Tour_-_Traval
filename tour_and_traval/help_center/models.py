from django.db import models

# Create your models here.
class Feedback(models.Model):
  full_name = models.CharField(max_length=100)
  email = models.EmailField()
  message = models.TextField()
  reating = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.full_name} Rate {self.reating} Stars"

class FutureUpdate(models.Model):
  email = models.EmailField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.email}"

