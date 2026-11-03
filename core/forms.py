from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    # We add a custom field here just for the form
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