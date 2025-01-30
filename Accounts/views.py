from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from braces.views import GroupRequiredMixin # type: ignore
from django.urls import reverse_lazy
from django.contrib.auth.models import AbstractUser
from django.views.generic import CreateView
from Accounts.forms import RegistrationForm

class CustomLoginView(LoginView):
    group_required = ['Staff', 'admin']
    def get_redirect_url(self):
         
        if self.request.user.groups.filter(name__in=self.group_required).exists():
            return reverse_lazy('staff_index')
        return reverse_lazy('core_index')
    
class registerUser(CreateView):
    
    form_class =RegistrationForm
    template_name = 'registration/register.html'      
    success_url = reverse_lazy('login')


