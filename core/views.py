from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Business, BusinessMembership, Product, ProductImage, Category
from .forms import ProductForm, CategoryForm, BusinessForm

def home(request):
    return render(request, 'core/home.html')

def shop_list(request):
    businesses = Business.objects.filter(account_status='Active')
    return render(request, 'core/shop_list.html', {'businesses': businesses})

def business_storefront(request, slug):
    business = get_object_or_404(Business, slug=slug)
    products = Product.objects.filter(business=business, publication_status='Published')
    return render(request, 'core/storefront.html', {'business': business, 'products': products})

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

    if request.method == 'POST':
        # Pass the business so the form can filter categories
        form = ProductForm(request.POST, request.FILES, business=membership.business)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = membership.business
            product.save()
            
            image = form.cleaned_data.get('image')
            if image:
                ProductImage.objects.create(product=product, image=image, is_primary=True)
                
            return redirect('dashboard')
    else:
        form = ProductForm(business=membership.business)

    return render(request, 'core/add_product.html', {'form': form, 'business': membership.business})

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