from django import forms
from .models import Listing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_value"]

    def __init__(self, *args, **kwargs):
        listing = kwargs.pop("listing", None)
        top_bid = kwargs.pop("top_bid", None)
        super().__init__(*args, **kwargs)
        self.instance.listing = listing
        self.top_bid = top_bid

    def clean_bid_value(self):
        bid_value = self.cleaned_data.get('bid_value')
        listing = self.instance.listing
        top_bid = self.top_bid
        if bid_value <= listing.bid_start:
            raise forms.ValidationError('Bid must be greater than starting bid')
        elif bid_value <= top_bid:
            raise forms.ValidationError('Bid must be greater than current bid')
        return bid_value
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
    