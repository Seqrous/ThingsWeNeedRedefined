from django.urls import path
from . import views

app_name = 'shopping_app'

urlpatterns = [
    path('main/', views.MainPageView.as_view(), name='index'),
    path('households/', views.HouseholdPageView.as_view(), name='household_list')
]