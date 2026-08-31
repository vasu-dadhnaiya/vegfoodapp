import re
from django import forms
from foodapp.models import Order

class CheckoutForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Your Full Name',
        'class': 'form-input'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-input'
    }))
    phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number (e.g. +91 9876543210)',
        'class': 'form-input'
    }))
    delivery_address = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Complete Delivery Address',
        'rows': 3,
        'class': 'form-input'
    }))
    delivery_note = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Optional delivery instructions',
        'class': 'form-input'
    }))

    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'delivery_address', 'delivery_note']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter a valid full name (at least 2 characters).")
        if not re.match(r'^[a-zA-Z\s\.\'-]+$', name):
            raise forms.ValidationError("Name must contain valid characters.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits_only = re.sub(r'[\s\-()+\+]', '', phone)
        if not digits_only.isdigit() or not (10 <= len(digits_only) <= 15):
            raise forms.ValidationError("Please enter a valid phone number (10-15 digits).")
        return phone

    def clean_delivery_address(self):
        address = self.cleaned_data.get('delivery_address', '').strip()
        if len(address) < 10:
            raise forms.ValidationError("Please provide a detailed delivery address (at least 10 characters).")
        return address
