from django import forms
from foodapp.models import Category
from foodapp.utils import validate_image_file

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=80,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Category Name (e.g. Italian Pizza)', 'class': 'form-input'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Short category description...', 'rows': 3, 'class': 'form-input'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-file-input', 'accept': 'image/*'})
    )

    class Meta:
        model = Category
        fields = ['name', 'description', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Category name must be at least 2 characters long.")
        
        # Check uniqueness excluding self instance
        qs = Category.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A category with this name already exists.")
            
        return name

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            validate_image_file(image, max_size_mb=5)
        return image
