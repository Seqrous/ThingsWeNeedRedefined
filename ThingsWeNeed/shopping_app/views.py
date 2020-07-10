from django.shortcuts import render
from django.views.generic import ListView
from . import models

# Create your views here.

class MainPageView(ListView):
    template_name = 'shopping_app/index.html'
    model = models.Household