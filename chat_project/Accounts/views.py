from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from Accounts.forms import RegistrationForm

class registerUser(CreateView):
    
    form_class =RegistrationForm
    template_name = 'registration/register.html'      
    success_url = reverse_lazy('login')
    
class home(TemplateView):
    template_name = "home.html"
