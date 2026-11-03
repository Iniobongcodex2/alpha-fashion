from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Business, BusinessMembership, Product, ProductImage
from .forms import ProductForm

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

@login_required
def dashboard(request):
    # Find the business attached to the logged-in user
    membership = BusinessMembership.objects.filter(user=request.user).first()
    
    if not membership:
        # If the user isn't attached to a business, send them back home
        return redirect('home')
        
    business = membership.business
    # Get ONLY the products for this specific business
    products = Product.objects.filter(business=business)

    context = {
        'business': business,
        'products': products,
        'role': membership.role
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def add_product(request):
    # First, verify the user belongs to a business
    membership = BusinessMembership.objects.filter(user=request.user).first()
    if not membership:
        return redirect('home')

    if request.method == 'POST':
        # ADDED request.FILES HERE so Django accepts the image upload
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Don't save to database yet
            product = form.save(commit=False)
            # Attach the business automatically for security!
            product.business = membership.business
            # Save to database
            product.save()
            
            # NEW: Save the image if one was uploaded
            image = form.cleaned_data.get('image')
            if image:
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_primary=True
                )
                
            # Redirect back to the dashboard after saving
            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'core/add_product.html', {
        'form': form, 
        'business': membership.business
    })