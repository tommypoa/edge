from django.db import models

# Create your models here.
# Stretch: Coordinate and ImPair has 1-to-1 relationship, but not defined for easier data extraction // no use for functionality.

class ImPair(models.Model):
    island = models.CharField(max_length=50)
    collection_id = models.CharField(max_length=50)
    im1id0 = models.IntegerField()
    im1id1 = models.IntegerField()
    im2id0 = models.IntegerField()
    im2id1 = models.IntegerField()
    linked = models.BooleanField(default=False)

class Coordinate(models.Model):
    im1_name = models.CharField(max_length=50)
    im2_name = models.CharField(max_length=50)
    im1_x = models.FloatField()
    im1_y = models.FloatField()
    im2_x = models.FloatField()
    im2_y = models.FloatField()
    pair = models.ForeignKey(ImPair, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

