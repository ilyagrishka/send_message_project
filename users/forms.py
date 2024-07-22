from django.contrib.auth.forms import UserCreationForm
from service.forms import StyleFormMixin
from users.models import Owner


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = Owner
        fields = ("email", "password1", "password2")
