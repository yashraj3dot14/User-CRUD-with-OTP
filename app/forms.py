from django import forms
from .models import MyCustomUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model =MyCustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'mobile', 'sec_email', 'password']