from .models import User,Question,Answer
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

class question_form(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ('question','author','category')
        widgets={
            'question':forms.TextInput(attrs={'placeholder':'Ask Question'}),
            'author':forms.HiddenInput()
        }

    def clean(self):
        clean_data=super().clean()
        new_question=clean_data.get('question')
        category=clean_data.get('category')
        question=Question.objects.filter(question=new_question,category=category)
        if question:
            self.add_error('question','Same Question is already exists.')
        if not re.match('^[a-zA-Z0-9!@#\.&$-()? ]{10,255}$',new_question):
            self.add_error('question','Allowed Alphanumeric values and !@#$&-()? symbols.10 - 255 characters... ')
        return clean_data

