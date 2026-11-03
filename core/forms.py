from django import forms
from .models import Product, Category, Business

class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'price', 'promotional_price', 'availability', 'publication_status']
        
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'promotional_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_status': forms.Select(attrs={'class': 'form-control'}),
        }

    # This is the magic part that filters the categories!
    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if business:
            self.fields['category'].queryset = Category.objects.filter(business=business)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'is_active']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['business_name', 'description', 'phone', 'whatsapp_number', 'email', 'address', 'logo']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 971501234567'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }