from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, widgets
from django.utils.translation import gettext_lazy as _
from ordering.models import Food, Order

class CanteenLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].max_length = 255
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class CanteenRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


    
    
    

class FoodPostForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    food_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Food
        fields = ('name', 'price', 'menu', 'bonus', 'description', 'food_image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['menu'].widget.attrs['class'] = 'form-control'
        self.fields['bonus'].widget.attrs['class'] = 'form-control'
