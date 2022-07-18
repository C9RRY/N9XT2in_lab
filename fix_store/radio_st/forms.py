from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class AddRadioSt(forms.ModelForm):
    class Meta:
        model = Radios
        fields = ['title', 'url']
