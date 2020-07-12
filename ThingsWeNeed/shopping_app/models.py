from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth import get_user_model


# Create your models here.

class UserProfileInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        self.user.username


class Address(models.Model):

    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.city + ", " + self.country + " " + self.postal_code

class Household(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    address = models.ForeignKey(Address, related_name='address', on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfileInfo, through='HouseholdMember')
    
    created_by = models.ForeignKey(User, related_name='creator', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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

    def __str__(self):
        return self.name