from django.shortcuts import render, redirect
from django.views.generic import ListView
from . import models
from . import forms

# Create your views here.

class MainPageView(ListView):
    template_name = 'shopping_app/index.html'
    model = models.Household

class HouseholdPageView(ListView):
    form_class = forms.JoinHouseholdForm
    template_name = 'shopping_app/household_list.html'

    def get_queryset(self, *args, **kwargs):
        # filter by user id
        households = models.Household.objects.all()
        return households

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # process form cleaned data
            # redirect to join_household()
            print('form is valid')
            return redirect('shopping_app:household_list')
        
        return render(request, self.template_name, {'form':form})

