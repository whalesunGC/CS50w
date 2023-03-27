from django import forms

class PageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    content= forms.CharField(label="Page content", widget=forms.Textarea)
