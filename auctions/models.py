from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing():
    #name, category, image_url, description, date_posted, bid_start, bid_last, bid_count, bid_date_end
    pass

class Comments():
    # name, comment, date
    pass

class Bids():
    # bid_start, bid_last, bid_count, bid_date
    pass