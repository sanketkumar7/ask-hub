from .models import User
from django import forms
import re
class user_form(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('first_name','last_name','username','password','confirm_password','email','phone_no')
        widgets={
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name=cleaned_data.get('first_name')
        last_name=cleaned_data.get('last_name')
        email=cleaned_data.get('email')
        phone_no=cleaned_data.get('phone_no')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not re.match('^[a-zA-Z][a-zA-Z0-9]{3,15}$',first_name):
            self.add_error('first_name','Please enter valid first name.')
        if not re.match('^[a-zA-Z][a-zA-Z0-9]{3,15}$',last_name):
            self.add_error('last_name','Please enter valid last name.')
        if not re.match('^[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9.]+$',email):
            self.add_error('email','Please enter valid email address.')
        if not re.match('^[0-9]{10}$',phone_no):
            self.add_error('phone_no','Please enter valid 10 digit number')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data
