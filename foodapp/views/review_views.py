from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from foodapp.models import FoodItem, Review, OrderItem
from foodapp.forms import ReviewForm

@login_required
@require_POST
def add_review(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id, is_available=True)
    
    if Review.objects.filter(user=request.user, food_item=food).exists():
        messages.error(request, "You have already reviewed this item.")
        return redirect('food_detail', pk=food_id)
        
    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        order__status='delivered',
        food_item=food
    ).exists()
    
    if not has_purchased:
        messages.error(request, "You can only review items that you have purchased and had delivered.")
        return redirect('food_detail', pk=food_id)
        
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.food_item = food
        review.save()
        messages.success(request, "Thank you for your feedback! Review posted.")
    else:
        messages.error(request, "Could not post review. Please check your inputs.")
        
    return redirect('food_detail', pk=food_id)
