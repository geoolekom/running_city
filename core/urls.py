from core.views import IndexView
from core.views import LoginView
from core.views import LogoutView
from django.urls import path

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
