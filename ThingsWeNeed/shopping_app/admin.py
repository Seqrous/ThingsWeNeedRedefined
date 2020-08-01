from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Household)
admin.site.register(models.Address)
admin.site.register(models.UserProfileInfo)
admin.site.register(models.Product)
admin.site.register(models.HouseholdMember)