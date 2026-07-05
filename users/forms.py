from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("avatar", "phone", "country")
