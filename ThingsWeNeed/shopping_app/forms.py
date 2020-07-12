from django import forms

class JoinHouseholdForm(forms.Form):
    household_id = forms.IntegerField()
    household_name = forms.CharField()
    