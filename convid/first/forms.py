# forms.py
from django import forms

class ProfileForm(forms.Form):
    img = forms.ImageField()
