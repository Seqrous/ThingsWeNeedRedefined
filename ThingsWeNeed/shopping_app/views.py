from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    ListView, RedirectView, 
    CreateView, TemplateView, DeleteView
)

from . import models
from . import forms
from django.contrib import messages
from django.utils.text import slugify

from django.db import IntegrityError


# Create your views here.

class MainPageView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'shopping_app/index.html'
    model = models.Household
    form_classes = {
        'add_product_form':forms.AddProductForm,
        'confirm_purchase_form':forms.ConfirmPurchaseForm,
    }

    def get_queryset(self, *args, **kwargs):
        current_user = self.request.user
        households = current_user.household_set.all()
        return households
    
    def get(self, request, *args, **kwargs):
        add_product_form = self.form_classes.get('add_product_form')
        confirm_purchase_form = self.form_classes.get('confirm_purchase_form')
        context = {
           'add_product_form':add_product_form,
           'confirm_purchase_form':confirm_purchase_form, 
           'household_list':self.get_queryset(*args, **kwargs),
        }
        return render(request, self.template_name, context)

class HouseholdPageView(LoginRequiredMixin, ListView):
    login_url = 'login'
    form_class = forms.JoinHouseholdForm
    template_name = 'shopping_app/household_list.html'

    def get_queryset(self, *args, **kwargs):
        current_user = self.request.user
        households = current_user.household_set.all()
        return households

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form, 'household_list':self.get_queryset(*args, **kwargs)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            # process form cleaned data
            # redirect to join_household()
            print('form is valid')
            return redirect('shopping_app:household_join', kwargs={'slug':self.kwargs.get('slug')})
        
        return render(request, self.template_name, {'form':form})

class CreateHouseholdView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
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

            # Makes sure such name doesn't already exist
            if not models.Household.objects.filter(slug=slugify(household.name)).exists():
                # Makes sure such address doesn't already exist
                if not models.Address.objects.filter(country=address.country, city=address.city, street_address=address.postal_code).exists():
                    
                    # Save to database
                    address.save()
                    household.save()

                    # Add the creator to members of a household
                    try:
                        models.HouseholdMember.objects.create(user=self.request.user, household=household)
                    except IntegrityError:
                        messages.warning(self.request, 'Something went wrong')
                    
                    return redirect(reverse('shopping_app:household_list', kwargs={'username':request.user.username}))

                else:
                    messages.error(request, 'There is already a household registered on this address')
                    return render(request, self.template_name, {'form_info':form_info, 'form_address':form_address})

            else:
                messages.error(request, 'A household with this name already exists')
                return render(request, self.template_name, {'form_info':form_info, 'form_address':form_address})

        else:
            return render(request, self.template_name, {'form_info':form_info, 'form_address':form_address})


class JoinHousehold(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        return reverse('shopping_app:household_list', kwargs={'username':kwargs.get('username')})

    def get(self, request, *args, **kwargs):
        form = forms.JoinHouseholdForm(request.GET)

        # form validation
        if form.is_valid():
            
            # look for an object in the database
            household = None
            try:
                household = models.Household.objects.filter(pk=form.cleaned_data.get('household_id'), name=form.cleaned_data.get('household_name')).get()
            except models.Household.DoesNotExist:
                messages.error(request, 'Household with such name and id does not exist')
            
            # is household exists then try to join
            if not household is None:
                if not request.user in household.members.all():
                    models.HouseholdMember.objects.create(user=self.request.user, household=household)
                    messages.success(self.request, "You are now a member")
                else:
                    messages.warning(self.request, "You are already a member")
        else:
            messages.error(request, 'The provided information is invalid')

        return super().get(request, *args, **kwargs)

class LeaveHousehold(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        return reverse('shopping_app:household_list', kwargs={'username':kwargs.get('username')})

    def get(self, request, *args, **kwargs):
        
        try:
            household_member = models.HouseholdMember.objects.filter(
                user = self.request.user,
                household__slug = self.kwargs.get('household_slug')
            ).get()
        except models.HouseholdMember.DoesNotExist:
            messages.warning(self.request, 'Sorry, but you are not in this group')
        else:
            household_member.delete()
            messages.success(self.request, 'You have left the group')
        
        return super().get(request, *args, **kwargs)

class AddProduct(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        return reverse('shopping_app:index')

    def post(self, request, *args, **kwargs):
        product_form = forms.AddProductForm(request.POST)

        if product_form.is_valid():

            product = models.Product(
                name = product_form.cleaned_data.get('name'),
                quantity = product_form.cleaned_data.get('quantity'),
                max_price = product_form.cleaned_data.get('max_price'),
                info = product_form.cleaned_data.get('info'),
                is_wish = product_form.cleaned_data.get('is_wish'),
                household = models.Household.objects.get(slug=kwargs.get('household_slug')),
                posted_by = request.user
            )
            product.save()

            return redirect(reverse('shopping_app:index'))

        else:
            render(request, 'shopping_app:index', {'add_product_form':product_form})

class RemoveProduct(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = models.Product
    success_url = reverse_lazy('shopping_app:index')

class ConfirmProductPurchase(LoginRequiredMixin, RedirectView):
    login_url = 'login'
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('shopping_app:index')
    
    def get(self, request, *args, **kwargs):
        form = forms.ConfirmPurchaseForm(request.GET)

        if form.is_valid():
            actual_price = form.cleaned_data.get('actual_price')
            print(form.cleaned_data)
            print(actual_price)
            pk = self.kwargs.get('pk')
            try:
                product = models.Product.objects.get(pk=pk)
            except models.Product.DoesNotExist:
                messages.error('This product does not exist')
            else:
                product.acutal_price = actual_price
                product.bought_by = self.request.user
                product.save()
        
        return super().get(request, *args, **kwargs)


class WishPageView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'shopping_app/wish_list.html'
    model = models.Product

    def get_queryset(self, *args, **kwargs):
        current_user = self.request.user
        wish_list = models.Product.objects.filter(posted_by=current_user, is_wish=True)
        return wish_list

    def get(self, request, *args, **kwargs):
        wish_list = self.get_queryset(args, kwargs)
        return render(request, self.template_name, {'wish_list':wish_list})