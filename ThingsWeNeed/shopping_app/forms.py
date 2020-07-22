from django import forms
from . import models

class JoinHouseholdForm(forms.Form):
    household_id = forms.IntegerField()
    household_name = forms.CharField()

class CreateHouseholdInfoForm(forms.ModelForm):
    
    class Meta():
        model = models.Household
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Household's name: "

class CreateHouseholdAddressForm(forms.ModelForm):

    class Meta():
        model = models.Address
        fields = ('country', 'city', 'postal_code', 'street_address')

class AddProductForm(forms.ModelForm):

    class Meta():
        model = models.Product
        fields = ('name', 'quantity', 'max_price', 'info', 'is_wish')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Product's name"
        self.fields['max_price'].label = "Max price"
        self.fields['info'].label = "Additional information"

class ConfirmPurchaseForm(forms.ModelForm):

    class Meta():
        model = models.Product
        fields = ('actual_price',)
