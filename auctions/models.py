from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
import uuid

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)

class Listing(models.Model):
    #name, id, category, image_url, description, date_posted, open(yes/no)
    name = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=64)
    image_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    bid_start = models.FloatField("starting bid", default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    open = models.BooleanField(default=True)

    class Meta:
        ordering =["-date_updated", "-date_created"]

    def __str__(self):
        return f"{self.name} in {self.category} open:{self.open}"

class Comment(models.Model):
    # name, comment, date, Listing_id
    id = models.BigAutoField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    date = models.DateField()

class Bid(models.Model):
    # bid_start, bid_last, bid_count, bid_date
    id = models.BigAutoField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bid_value = models.FloatField()
    bid_date = models.DateTimeField(auto_now_add=True)