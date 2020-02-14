from django.db import models

# Create your models here.

class Coordinate(models.Model):
    im1_name = models.CharField(max_length=50)
    im2_name = models.CharField(max_length=50)
    im1_x = models.FloatField()
    im1_y = models.FloatField()
    im2_x = models.FloatField()
    im2_y = models.FloatField()
    created_at = models.DateTimeField()