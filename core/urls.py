from django.urls import path
from . import views

urlpatterns = [
    # Public Storefront URLs
    path('', views.home, name='home'),
    path('shop/', views.shop_list, name='shop_list'),
    path('shop/<slug:slug>/', views.business_storefront, name='business_storefront'),
    
    # Product Details
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Authentication URLs
    path('register/', views.register, name='register'),

    # Dashboard URLs (Secured)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-product/', views.add_product, name='add_product'),
    path('dashboard/product/<int:pk>/variants/', views.manage_variants, name='manage_variants'), 
    path('dashboard/product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('dashboard/product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('dashboard/categories/', views.manage_categories, name='manage_categories'),
    path('dashboard/profile/', views.manage_profile, name='manage_profile'),
    path('dashboard/pricing/', views.pricing, name='pricing'),
    path('dashboard/upgrade-plan/', views.upgrade_plan, name='upgrade_plan'),
    
    # ALPHA Super-Admin URLs
    path('control-center/', views.super_admin_dashboard, name='super_admin_dashboard'),
]
