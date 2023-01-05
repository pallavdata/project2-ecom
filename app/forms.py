from django import forms
import re
from .models import LoginData, address
from django.contrib.auth.forms import UserCreationForm

class addressForm(forms.ModelForm):
    class Meta:
        model = address
        exclude = ["userId",]

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255,label="Email Id", widget = forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=8,max_length=16,label="Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}))

class RegForm(UserCreationForm):
    username = forms.CharField(min_length=4,max_length=255,label="Username", widget = forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255,label="Email Id", widget = forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(min_length=8,max_length=16,label="Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(min_length=8,max_length=16,label="Re Enter Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = LoginData
        fields = ['username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


    def clean(self):
        super(RegForm, self).clean()
        try:
            password = self.cleaned_data['password1']
        except:
            password = ""
        try:
            pass2 = self.cleaned_data['password2']
        except:
            pass2 = ""


        pattern = re.compile('[A-Z]')
        pattern2 = re.compile('[a-z]')
        pattern3 = re.compile('[0-9]')
        pattern4 = re.compile('[!@#$%^&*(),.?":{}|<>]')

        if not pattern.search(password) or not pattern2.search(password) or not pattern3.search(password) or not pattern4.search(password):
                list = ['should contain at least one upper case','should contain at least one lower case','should contain at least one digit','should contain at least one Special character']
                self.add_error('password1',list)
                try:
                    del self._errors['password2']
                except:
                    pass
        return self.cleaned_data




    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = LoginData.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")
        

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user_name = LoginData.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")