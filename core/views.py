from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Business, BusinessMembership, Product, ProductImage
from .forms import ProductForm

def home(request):
    return render(request, 'core/home.html')

def shop_list(request):
    businesses = Business.objects.filter(account_status='Active')
    return render(request, 'core/shop_list.html', {'businesses': businesses})

def business_storefront(request, slug):
    business = get_object_or_404(Business, slug=slug)
    products = Product.objects.filter(business=business, publication_status='Published')
    return render(request, 'core/storefront.html', {'business': business, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.publication_status != 'Published' or product.business.account_status != 'Active':
        return redirect('home')
    return render(request, 'core/product_detail.html', {'product': product})

@login_required
def dashboard(request):
    membership = BusinessMembership.objects.filter(user=request.user).first()
    if not membership:
        return redirect('home')
    business = membership.business
    products = Product.objects.filter(business=business)
    return render(request, 'core/dashboard.html', {'business': business, 'products': products, 'role': membership.role})

@login_required
def add_product(request):
    membership = BusinessMembership.objects.filter(user=request.user).first()
    if not membership:
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = membership.business
            product.save()
            
            image = form.cleaned_data.get('image')
            if image:
                ProductImage.objects.create(product=product, image=image, is_primary=True)
                
            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'core/add_product.html', {'form': form, 'business': membership.business})
