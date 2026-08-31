from django import forms
from foodapp.models import FoodItem, Category
from foodapp.utils import validate_image_file

class FoodItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        empty_label="-- Select Category --",
        widget=forms.Select(attrs={'class': 'form-input select-input'})
    )
    
    name = forms.CharField(
        max_length=120,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Item Name (e.g., Paneer Tikka Burger)', 'class': 'form-input'})
    )
    
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Detailed item description...', 'rows': 4, 'class': 'form-input'})
    )
    
    price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=True,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01', 'class': 'form-input'})
    )
    
    discount_price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'placeholder': 'Optional discount price', 'step': '0.01', 'class': 'form-input'})
    )
    
    stock = forms.IntegerField(
        min_value=0,
        required=True,
        initial=50,
        widget=forms.NumberInput(attrs={'placeholder': 'Current Inventory Stock', 'class': 'form-input'})
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-file-input', 'accept': 'image/*'})
    )
    
    is_available = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'description', 'price', 'discount_price', 'stock', 'image', 'is_available']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            validate_image_file(image, max_size_mb=5)
        return image

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Food item name must be at least 2 characters long.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')

        if price is not None and discount_price is not None:
            if discount_price >= price:
                self.add_error('discount_price', "Discount price must be lower than the original price.")
            if discount_price <= 0:
                self.add_error('discount_price', "Discount price must be greater than zero.")

        return cleaned_data
