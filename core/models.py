from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Business(models.Model):
    business_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, default='United Arab Emirates')
    currency = models.CharField(max_length=10, default='AED')
    phone = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    subscription_status = models.CharField(max_length=50, default='Free')
    account_status = models.CharField(max_length=50, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically create a URL-friendly slug if one isn't provided
        if not self.slug:
            self.slug = slugify(self.business_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.business_name

    class Meta:
        verbose_name_plural = "Businesses" # Fixes "Businesss" in admin


class BusinessMembership(models.Model):
    ROLE_CHOICES = (
        ('Owner', 'Owner'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Owner')
    membership_status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.user.username} - {self.business.business_name} ({self.role})"

    class Meta:
        verbose_name_plural = "Business Memberships"


class Category(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.business.business_name})"

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    PUBLICATION_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promotional_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    availability = models.BooleanField(default=True)
    publication_status = models.CharField(max_length=20, choices=PUBLICATION_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.business.business_name}"

    class Meta:
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    display_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.product_name}"

    class Meta:
        verbose_name_plural = "Product Images"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=50, blank=True)
    colour = models.CharField(max_length=50, blank=True)
    sku = models.CharField(max_length=50, blank=True)
    stock_quantity = models.IntegerField(default=0)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.size} / {self.colour}"

    class Meta:
        verbose_name_plural = "Product Variants"


class CustomerEnquiry(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Closed', 'Closed'),
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='enquiries')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
    customer_name = models.CharField(max_length=255)
    customer_contact = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    enquiry_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.customer_name} for {self.business.business_name}"

    class Meta:
        verbose_name_plural = "Customer Enquiries"