from django.views.generic.edit import CreateView
from .forms import CreateUserForm, LoginUserForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'app_auth/create_user.html'
    success_url = reverse_lazy('auth:login')


class LoginViewP(LoginView):
    template_name = 'app_auth/login.html'
    success_url = reverse_lazy('posts:post')
    redirect_authenticated_user = True


class LogoutViewP(LogoutView):
    next_page = reverse_lazy('posts:post')