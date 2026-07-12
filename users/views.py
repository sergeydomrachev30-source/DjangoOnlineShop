from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from config import settings

# 1. ДОБАВИЛИ UserLoginForm В ИМПОРТ:
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject="Добро пожаловать в наш Интернет магазин",
            message=f"Привет, {user.email}! Спасибо за регистрацию на нашем сайте.",
            from_email=getattr(settings, "EMAIL_HOST_USER", "no-reply@shop.com"),
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    # 2. ПОДКЛЮЧИЛИ ФОРМУ ДЛЯ ВХОДА ПО EMAIL:
    form_class = UserLoginForm
    template_name = "users/login.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """Метод get_object говорит Django обновлять профиль именно того пользователя,
        который сейчас авторизован на сайте"""
        return self.request.user
