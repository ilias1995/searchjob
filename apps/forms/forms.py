# coding: utf-8
from django import forms
from django.db import models
from models import Job, UserProfile
from django.contrib.auth.models import User
from collections import OrderedDict
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'phone')


class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True, label='Логин')
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label= ("Пароль"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class Reg(forms.ModelForm):
	class Meta:
		model = Job
		fields = ('name_town', 'jobtype' , 'phone_number', 'date_job', 'name_job', 'email', 'how_many', 'about', 'jobtype')


class Register(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	check = forms.BooleanField( label='Соглосна ли вы правилами сайта ' )
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password')


