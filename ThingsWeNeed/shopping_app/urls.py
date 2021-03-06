from django.urls import path
from . import views

app_name = 'shopping_app'

urlpatterns = [
    path('main/', views.MainPageView.as_view(), name='index'),
    path('<slug:username>/households/', views.HouseholdPageView.as_view(), name='household_list'),
    path('households/create/', views.CreateHouseholdView.as_view(), name='household_create'),
    path('<slug:username>/households/join/', views.JoinHousehold.as_view(), name='household_join'),
    path('<slug:username>/households/leave/<slug:household_slug>/', views.LeaveHousehold.as_view(), name='household_leave'),
    path('<slug:username>/<slug:household_slug>/add-product/', views.AddProduct.as_view(), name='product_add'),
    path('<slug:username>/<slug:household_slug>/<int:pk>/remove/', views.RemoveProduct.as_view(), name='product_remove'),
    path('<slug:username>/<slug:household_slug>/<int:pk>/confirm-purchase/', views.ConfirmProductPurchase.as_view(), name='product_confirm_purchase'),
    path('<slug:username>/wishes/', views.WishPageView.as_view(), name='wish_list')
]