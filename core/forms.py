from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # We only want the user to fill out these specific fields. 
        # We will handle 'business' in the view for security.
        fields = ['product_name', 'category', 'description', 'price', 'promotional_price', 'availability', 'publication_status']
        
        # Add some styling to the inputs
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'promotional_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_status': forms.Select(attrs={'class': 'form-control'}),
        }