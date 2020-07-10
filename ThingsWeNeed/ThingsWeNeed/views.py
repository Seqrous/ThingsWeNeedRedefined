from django.views.generic import CreateView, TemplateView
from . import forms
from django.urls import reverse_lazy

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

class ThanksPage(TemplateView):
    template_name = 'thanks.html'