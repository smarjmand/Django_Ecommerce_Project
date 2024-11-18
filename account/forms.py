from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError


#------------------------------------------------------------------
# Form to create new user :
class CreateUserForm(UserCreationForm):

    # Define model and fields
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # To add class for front-end
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    # To add required to email-input
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    # To validate email :
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(message='این ایمیل قبلا ثبت نام کرده است')
        if len(email) >= 100:
            raise forms.ValidationError(message='ایمیل بیش از حد طولانی است')
        return email


#------------------------------------------------------------------
# Form for login :
class LoginForm(AuthenticationForm):
    # To add class for front-end
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=PasswordInput(attrs={
        'class': 'form-control'
    }))

    # Customize errors :
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)

        self.error_messages['inactive'] = 'ابتدا حساب کاربری خود را فعال کنید'
        self.error_messages['invalid_login'] = 'نام کاربری یا کلمه ی عبور صحیح نمی باشد'


#------------------------------------------------------------------
# Form to update user's infos :
class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        exclude = ['password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'required': 'required'
            }),
        }

    # To validate new-email :
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError('ایمیل تکراری است')
        return email

    # To validate new-username :
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError('نام کاربری تکراری است')
        return username
