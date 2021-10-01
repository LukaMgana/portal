from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password','placeholder':'password'}))
    class Meta:
        model = User
        fields = ['username', 'password']




class FarmerRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


    