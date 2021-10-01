from django import forms
from .models import *


class AnimalRegistrationForm(forms.ModelForm):
    livestock_name         = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type': 'text',}),)
    birth_date          = forms.DateField(widget=forms.NumberInput(attrs={'class':'form-control','type': 'date',}),)
    weight              = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','type': 'number',}),)
    ls_image            = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control','type': 'file',}),)


    class Meta:
        model = Livestock
        fields = (
            'livestock_name', 'gender', 'status', 'birth_date', 
            'location', 'weight', 'ls_image', 'cartegory'
        )
    
    
    def __init__(self, *args, **kwargs):
        super(AnimalRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['cartegory'].widget.attrs['class'] = 'form-control'
        self.fields['cartegory'].empty_label = 'Choose category'
        self.fields['cartegory'].widget.choices = self.fields['cartegory'].choices
        
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['birth_date'].widget.attrs['class'] = 'form-control'
        self.fields['livestock_name'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['weight'].widget.attrs['class'] = 'form-control'
        self.fields['ls_image'].widget.attrs['class'] = 'form-control'


class ExpenseIncomeForm(forms.ModelForm):
    due_date          = forms.DateField(widget=forms.NumberInput(attrs={'class':'form-control','type': 'date',}),)

    class Meta:
        model = ExpenseIncome
        fields = (
            'due_date', 'amount', 'descriptions', 'ei_type'
        )


    def __init__(self, *args, **kwargs):
        super(ExpenseIncomeForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['descriptions'].widget.attrs['class'] = 'form-control'
        self.fields['due_date'].widget.attrs['class'] = 'form-control'
        self.fields['ei_type'].widget.attrs['class'] = 'form-control'

