from django.urls import path

from users.views import ProfileUpdateView, RegisterView, UserLoginView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]
