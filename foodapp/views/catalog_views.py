from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Q
from foodapp.models import Category, FoodItem, Review, OrderItem
from foodapp.forms import ReviewForm

def home(request):
    featured_foods = FoodItem.objects.filter(is_available=True, stock__gt=0)[:6]
    categories = Category.objects.all()
    testimonials = Review.objects.select_related('user', 'food_item').filter(rating__gte=4)[:4]
    
    return render(request, 'home.html', {
        'featured_foods': featured_foods,
        'categories': categories,
        'testimonials': testimonials
    })

def menu(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', '')
    filter_discount = request.GET.get('discount', '')

    foods = FoodItem.objects.all().select_related('category')
    categories = Category.objects.all()

    if query:
        foods = foods.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        if category_id.isdigit():
            foods = foods.filter(category_id=category_id)
        else:
            foods = foods.filter(category__slug__iexact=category_id) | foods.filter(category__name__iexact=category_id)

    if filter_discount == '1':
        foods = foods.filter(discount_price__isnull=False, discount_price__gt=0)

    if sort_by == 'price_asc':
        foods = foods.order_by('price')
    elif sort_by == 'price_desc':
        foods = foods.order_by('-price')
    elif sort_by == 'name':
        foods = foods.order_by('name')

    return render(request, 'menu.html', {
        'foods': foods,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
        'sort_by': sort_by,
        'filter_discount': filter_discount,
    })

def food_detail(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    reviews = food.reviews.select_related('user').order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rating:
        avg_rating = round(avg_rating, 1)
    
    review_form = ReviewForm()
    
    has_reviewed = False
    can_review = False
    if request.user.is_authenticated:
        has_reviewed = Review.objects.filter(user=request.user, food_item=food).exists()
        can_review = OrderItem.objects.filter(
            order__user=request.user,
            order__status='delivered',
            food_item=food
        ).exists()

    related_foods = FoodItem.objects.filter(category=food.category, is_available=True).exclude(pk=food.pk)[:4]

    return render(request, 'food_detail.html', {
        'food': food,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
        'has_reviewed': has_reviewed,
        'can_review': can_review,
        'related_foods': related_foods,
    })
