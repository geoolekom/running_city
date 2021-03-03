from core.forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
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


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "core/register.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        form.instance.is_active = True
        response = super().form_valid(form)
        messages.info(self.request, "Вы успешно зарегистрировались. Войдите, используя указанный пароль.")
        return response
