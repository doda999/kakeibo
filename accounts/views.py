from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView,CreateView,DetailView,UpdateView
from django.shortcuts import resolve_url
from .forms import LoginForm, RegistrationForm, AccountsUpdateForm
import datetime

# Create your views here.
class Login(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

class Top(LoginRequiredMixin,TemplateView):
    template_name = 'top.html'
    redirect_field_name = 'redirect_to'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        context["year"] = int(now.year)
        context["month"] = int(now.month)

        return context        

class Logout(LoginRequiredMixin,LogoutView):
    template_name = 'logout.html'

User = get_user_model()

class Registration(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/registration/complete'

class RegistrationComp(TemplateView):
    template_name = "registration_complete.html"

# ユーザー限定のクラス
class UserOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class Profile(UserOnlyMixin, DetailView):
    model = User
    template_name = 'profile.html'

class ProfileUpdate(UserOnlyMixin,UpdateView):
    model = User
    form_class = AccountsUpdateForm
    template_name = 'profile_update.html'

    def get_success_url(self):
        return resolve_url('accounts:profile', pk=self.kwargs['pk'])

class PasswordChange(UserOnlyMixin,PasswordChangeView):
    model = User
    template_name = 'password_change.html'

    def get_success_url(self):
        return resolve_url('accounts:password_complete', pk=self.kwargs['pk'])

class PasswordChangeComp(UserOnlyMixin,PasswordChangeDoneView):
    template_name = "password_change_complete.html"


