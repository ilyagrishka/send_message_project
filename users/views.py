from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404, redirect
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, ProfileEditForm
from users.models import Owner
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
import secrets
from django.core.mail import send_mail


class UserCreate(CreateView):
    model = Owner
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirms/{token}/"
        send_mail(
            subject="подтверждение почты",
            message=f"перейди по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

    def profile_view(self, username):
        user = get_object_or_404(User, username=username)

        context = {
            'user_profile': user
        }

        return render(self.request, 'profile.html', context)

    @login_required
    def edit_profile(self):
        if self.request.method == 'POST':
            form = ProfileEditForm(self.request.POST, self.request.FILES, instance=self.request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = ProfileEditForm(instance=self.request.user)

        return render(self.request, 'users/edit.html', {'form': form})


def email_verification(request, token):
    user = get_object_or_404(Owner, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))
