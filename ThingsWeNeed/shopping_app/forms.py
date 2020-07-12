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
        self.fields['name'].label = "Household's name:"

class CreateHouseholdAddressForm(forms.ModelForm):

    class Meta():
        model = models.Address
        fields = ('country', 'city', 'postal_code')
