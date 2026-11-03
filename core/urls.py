from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-product/', views.add_product, name='add_product'),
    path('shop/', views.shop_list, name='shop_list'),
    path('shop/<slug:slug>/', views.business_storefront, name='business_storefront'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]