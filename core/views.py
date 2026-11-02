from django.shortcuts import render, get_object_or_404
from .models import Business, Product

def home(request):
    return render(request, 'core/home.html')

def shop_list(request):
    # Fetch all active businesses
    businesses = Business.objects.filter(account_status='Active')
    return render(request, 'core/shop_list.html', {'businesses': businesses})

def business_storefront(request, slug):
    # Fetch the specific business based on the URL slug
    business = get_object_or_404(Business, slug=slug)
    
    # Fetch only this business's published products
    products = Product.objects.filter(business=business, publication_status='Published')
    
    context = {
        'business': business,
        'products': products
    }
    return render(request, 'core/storefront.html', context)