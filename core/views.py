from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Business, BusinessMembership, Product, ProductImage, Category, ProductVariant
from .forms import RegisterForm, ProductForm, CategoryForm, BusinessForm

def home(request):
    return render(request, 'core/home.html')

def shop_list(request):
    businesses = Business.objects.filter(account_status='Active')
    return render(request, 'core/shop_list.html', {'businesses': businesses})

def business_storefront(request, slug):
    business = get_object_or_404(Business, slug=slug)
    
    # Start with all published products for this business
    products = Product.objects.filter(business=business, publication_status='Published')
    
    # 1. Handle Search Query (q)
    query = request.GET.get('q')
    if query:
        products = products.filter(product_name__icontains=query) # Case-insensitive search
        
    # 2. Handle Category Filter (category)
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'business': business,
        'products': products
    }
    return render(request, 'core/storefront.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Security check: Only show if published and business is active
    if product.publication_status != 'Published' or product.business.account_status != 'Active':
        return redirect('home')
        
    return render(request, 'core/product_detail.html', {'product': product, 'business': product.business})

@login_required
def dashboard(request):
    membership = BusinessMembership.objects.filter(user=request.user).first()
    if not membership:
        return redirect('home')
        
    business = membership.business
    products = Product.objects.filter(business=business)
    
    return render(request, 'core/dashboard.html', {
        'business': business, 
        'products': products, 
        'role': membership.role
    })

@login_required
def add_product(request):
    membership = BusinessMembership.objects.filter(user=request.user).first()
    if not membership:
        return redirect('home')
        
    business = membership.business

    # --- SUBSCRIPTION LIMIT CHECK ---
    # If the business is on the Free plan and has 20 or more products, block them
    current_product_count = Product.objects.filter(business=business).count()
    if business.subscription_status == 'Free' and current_product_count >= 20:
        # Redirect back to the dashboard if the limit is reached
        return redirect('dashboard')
    # --------------------------------

    if request.method == 'POST':
        # Pass the business so the form can filter categories
        form = ProductForm(request.POST, request.FILES, business=business)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = business
            product.save()
            
            image = form.cleaned_data.get('image')
            if image:
                ProductImage.objects.create(product=product, image=image, is_primary=True)
                
            return redirect('dashboard')
    else:
        form = ProductForm(business=business)

    return render(request, 'core/add_product.html', {'form': form, 'business': business})

@login_required
def manage_categories(request):
    membership = BusinessMembership.objects.filter(user=request.user).first()
    if not membership:
        return redirect('home')

    business = membership.business
    categories = Category.objects.filter(business=business)

    if request.method == 'POST':
        # Added request.FILES so category images work
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.business = business
            category.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    return render(request, 'core/manage_categories.html', {
        'categories': categories,
        'form': form,
        'business': business
    })

@login_required
def manage_profile(request):
    membership = BusinessMembership.objects.filter(user=request.user).first()
    if not membership:
        return redirect('home')

    business = membership.business

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BusinessForm(instance=business)

    return render(request, 'core/manage_profile.html', {
        'form': form,
        'business': business
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # transaction.atomic ensures that if creating the business fails, the user isn't created either
            with transaction.atomic():
                user = form.save()
                
                # Create the business
                business_name = form.cleaned_data.get('business_name')
                business = Business.objects.create(
                    business_name=business_name,
                    email=user.email # Use email if they provided one, otherwise it's blank
                )
                
                # Link the user to the business
                BusinessMembership.objects.create(
                    user=user,
                    business=business,
                    role='Owner'
                )
                
                # Log the user in
                login(request, user)
                return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def manage_variants(request, pk):
    membership = BusinessMembership.objects.filter(user=request.user).first()
    if not membership:
        return redirect('home')
        
    business = membership.business
    
    # Security: Ensure the product belongs to this business
    product = get_object_or_404(Product, pk=pk, business=business)

    if request.method == 'POST':
        # Get the data from the form
        size = request.POST.get('size')
        colour = request.POST.get('colour')
        stock = request.POST.get('stock_quantity')
        
        if size and stock:
            # Create the variant
            ProductVariant.objects.create(
                product=product,
                size=size,
                colour=colour,
                stock_quantity=stock
            )
            return redirect('manage_variants', pk=product.pk)

    variants = ProductVariant.objects.filter(product=product)
    
    return render(request, 'core/manage_variants.html', {
        'product': product,
        'variants': variants,
        'business': business
    })