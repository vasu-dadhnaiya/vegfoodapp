from django import forms
from foodapp.models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(5, 0, -1)],
        widget=forms.Select(attrs={'class': 'form-input rating-select'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Write your food review here...',
            'rows': 4,
            'class': 'form-input'
        })
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
