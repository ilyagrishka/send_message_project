from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from users.views import UserCreate, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"),
         name="login"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"),name="logout"),
    path("register/", UserCreate.as_view(), name="register"),
    path("email-confirms/<str:token>/", email_verification, name="email-confirm")
    ]
