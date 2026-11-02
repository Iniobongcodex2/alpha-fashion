from django.contrib import admin
from .models import Business, BusinessMembership, Category, Product, ProductImage, ProductVariant, CustomerEnquiry

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'subscription_status', 'account_status', 'created_at')
    prepopulated_fields = {'slug': ('business_name',)}
    search_fields = ('business_name', 'email', 'phone')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'is_active')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'business', 'price', 'publication_status', 'availability')
    list_filter = ('publication_status', 'availability', 'business')
    search_fields = ('product_name', 'sku')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'display_order')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'colour', 'stock_quantity')

@admin.register(CustomerEnquiry)
class CustomerEnquiryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'business', 'enquiry_status', 'created_at')
    list_filter = ('enquiry_status', 'business')

@admin.register(BusinessMembership)
class BusinessMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'business', 'role', 'membership_status')