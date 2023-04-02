from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
import uuid

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    #name, id, category, image_url, description, date_posted, open(yes/no)
    name = models.CharField(max_length=50)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=64, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    bid_start = models.DecimalField("starting bid",max_digits=8, decimal_places=2 , default=0.00)
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
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user} commented {self.comment} on {self.instance.listing.listing_name}"

class Bid(models.Model):
    # bid_start, bid_last, bid_count, bid_date
    id = models.BigAutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="listing_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bid_value = models.DecimalField(max_digits=8, decimal_places=2 , default=0.00)
    bid_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =["-bid_value"]

    def __str__(self):
        return f"{self.user} bid:${self.bid_value} on:{self.bid_date}"
    
class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return f"{self.user} watchlists {self.listing}"