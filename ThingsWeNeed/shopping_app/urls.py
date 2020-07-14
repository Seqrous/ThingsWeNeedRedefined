from django.urls import path
from . import views

app_name = 'shopping_app'

urlpatterns = [
    path('main/', views.MainPageView.as_view(), name='index'),
    path('households/', views.HouseholdPageView.as_view(), name='household_list'),
    path('households/create/', views.CreateHouseholdView.as_view(), name='household_create'),
    path('households/join/', views.JoinHousehold.as_view(), name='household_join')
]