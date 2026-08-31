from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address',
        'class': 'form-input'
    }))
    first_name = forms.CharField(max_length=50, required=True, label="Full Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter your full name',
        'class': 'form-input'
    }))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Full Name", widget=forms.TextInput(attrs={
        'class': 'form-input'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'email']
