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

    def __str__(self):
        return "{5} {0}: {1}_{2} and {3}_{4}".format(self.collection_id, self.im1id0, \
            self.im1id1, self.im2id0, self.im2id1, self.island)


class Coordinate(models.Model):
    im1_name = models.CharField(max_length=100)
    im2_name = models.CharField(max_length=100)
    im1_x = models.FloatField()
    im1_y = models.FloatField()
    im2_x = models.FloatField()
    im2_y = models.FloatField()
    pair = models.ForeignKey(ImPair, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self):
        return "Coordinate for " + str(self.pair)
