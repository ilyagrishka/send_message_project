from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import forms
from django.utils.text import slugify

from service.forms import StyleFormMixin
from users.models import Owner


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = Owner
        fields = ("email", "password1", "password2")


class ProfileEditForm(StyleFormMixin):
    class Meta:
        model = User
        fields = "__all__"

