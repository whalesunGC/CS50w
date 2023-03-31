from django import forms
from .models import Listing, Bid

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_value"]

    #def __init__(self, *args, **kwargs):
       # listing = kwargs.pop('listing', None)
        #super().__init__(*args, **kwargs)
       # if listing:
          #  self.fields['bid_value'].widget.attrs.update({'min': listing.bid})