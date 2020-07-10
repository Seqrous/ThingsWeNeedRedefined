from django.urls import path
from . import views

app_name = 'shopping_app'

urlpatterns = [
    path('main/', views.MainPageView.as_view(), name='index'),
]