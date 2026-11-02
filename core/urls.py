from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop_list, name='shop_list'),
    path('shop/<slug:slug>/', views.business_storefront, name='business_storefront'),
]