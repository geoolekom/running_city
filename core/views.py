from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from quiz.models import Quiz


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz_list"] = Quiz.objects.all()
        return context


class LoginView(BaseLoginView):
    redirect_authenticated_user = True
    template_name = "core/login.html"


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    http_method_names = ("get",)
    template_name = "core/logout.html"
    next_page = reverse_lazy("core:index")
