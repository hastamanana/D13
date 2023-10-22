from django import forms
from django.forms import ModelForm, HiddenInput
from .models import Ad, Offer


class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['author', 'title', 'category', 'content',
                  'image1', 'image2', 'image3', 'video']
        widgets = {
            'author': HiddenInput()
        }


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['user', 'ad', 'text']
        labels = {'text': ''}
        widgets = {
            'user': HiddenInput(),
            'ad': HiddenInput(),
            'text': forms.Textarea(attrs={'placeholder': 'Напишите здесь Ваш отклик'})
        }
