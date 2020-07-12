from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

# Create your models here.

class UserProfileInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Address(models.Model):

    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=10)

class Household(models.Model):

    name = models.CharField(max_length=64)
    address = models.ForeignKey(Address, related_name='address', on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfileInfo, through='HouseholdMember')
    
    created_by = models.ForeignKey(UserProfileInfo, related_name='creator', on_delete=models.PROTECT)

class HouseholdMember(models.Model):
    
    user = models.ForeignKey(UserProfileInfo, related_name='member', on_delete=models.CASCADE)
    household = models.ForeignKey(Household, related_name='household', on_delete=models.CASCADE)

class Product(models.Model):

    name = models.CharField(max_length=64)
    max_price = models.FloatField(blank=True)
    quantity = models.PositiveIntegerField()
    info = models.TextField(max_length=256, blank=True)
    is_wish = models.BooleanField()

    posted_by = models.ForeignKey(UserProfileInfo, related_name='poster', on_delete=models.CASCADE)
    bought_by = models.ForeignKey(UserProfileInfo, related_name='buyer', null=True, blank=True, on_delete=models.SET_NULL)