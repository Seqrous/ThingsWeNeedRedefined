from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, RedirectView, CreateView, TemplateView
from . import models
from . import forms
from django.contrib import messages
from django.utils.text import slugify

from django.db import IntegrityError


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
        return render(request, self.template_name, {'form':form, 'household_list':self.get_queryset()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            # process form cleaned data
            # redirect to join_household()
            print('form is valid')
            return redirect('shopping_app:household_join', kwargs={'slug':self.kwargs.get('slug')})
        
        return render(request, self.template_name, {'form':form})

class CreateHouseholdView(TemplateView):
    template_name = 'shopping_app/household_create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form_info':forms.CreateHouseholdInfoForm, 'form_address':forms.CreateHouseholdAddressForm})


    def post(self, request, *args, **kwargs):
        form_info = forms.CreateHouseholdInfoForm(request.POST)
        form_address = forms.CreateHouseholdAddressForm(request.POST)

        if (form_info.is_valid() and form_address.is_valid()):

            # Create new instances
            address = models.Address(
                country=form_address.cleaned_data['country'], 
                city=form_address.cleaned_data['city'], 
                postal_code=form_address.cleaned_data['postal_code'],
                street_address=form_address.cleaned_data['street_address']
            )
            household = models.Household(name=form_info.cleaned_data['name'], address=address, created_by=request.user)

            # Ensure entries do not exist
            # to implement: handle slug uniquness
            if (not models.Household.objects.filter(name=household.name).exists() and 
                not models.Address.objects.filter(country=address.country, city=address.city, postal_code=address.postal_code, street_address=address.postal_code).exists()):
            
                # Save to database
                address.save()
                household.save()

                return redirect('shopping_app:household_list')
            else:
                messages.error(request, 'A household with this name or address already exists')
        else:
            return render(request, self.template_name, {'form_info':form_info, 'form_address':form_address})


class JoinHousehold(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('shopping_app:household_list')

    def get(self, request, *args, **kwargs):
        household = get_object_or_404(models.Household, pk=request.GET['household_id'], slug=slugify(request.GET['household_name']))

        try:
            models.HouseholdMember.objects.create(user=self.request.user, household=household)
        except IntegrityError:
            messages.warning(self.request, "You are already a member")
        else:
            messages.success(self.request, "You are not a member")

        return super().get(request, *args, **kwargs)
