from django import forms
from .models import Address


#------------------------------------------------------------------
# Form to get user's address :
class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['user']

    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))