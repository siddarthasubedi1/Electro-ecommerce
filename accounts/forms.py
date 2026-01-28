from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
    )
  
    first_name = forms.CharField(
        label='first name',
        widget= forms.TextInput(
            attrs={'class':'form-control'}
        ),
        required=True,
    )
    last_name = forms.CharField(
        label='last name',
        widget= forms.TextInput(
            attrs={'class':'form-control'}
        ),
        required=True,
    )
    
    password1 = forms.CharField(
        label='password',
        widget = forms.PasswordInput(
            attrs={'class':'form-control'},
        )
    )
    password2 = forms.CharField(
        label=' confirm password',
        widget = forms.PasswordInput(
            attrs={'class':'form-control'},
        )
    )
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')