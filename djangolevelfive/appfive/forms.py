from appfive.models import Usermodel
from django import forms
from django.contrib.auth.models import User

class userform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields=('username','email','password')


class usermodelform(forms.ModelForm):
    class Meta():
        model=Usermodel
        fields=('profile_pic','urlfield')
