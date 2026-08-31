import os
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count, Q
from foodapp.models import Order, FoodItem, Category, Review

def validate_image_file(image_obj, max_size_mb=5):
    """
    Validates uploaded image format and file size.
    """
    if not image_obj:
        return
        
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(image_obj.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported image format. Allowed formats: {', '.join(valid_extensions)}")
        
    max_bytes = max_size_mb * 1024 * 1024
    if image_obj.size > max_bytes:
        raise ValidationError(f"Image file size exceeds maximum limit of {max_size_mb}MB.")

def get_dashboard_stats():
    """
    Calculates summary metrics and statistical counts for the Super User Dashboard.
    """
    completed_orders = Order.objects.exclude(status='cancelled')
    total_revenue = completed_orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    active_orders = Order.objects.filter(status__in=['pending', 'confirmed', 'preparing', 'out_for_delivery']).count()
    
    total_products = FoodItem.objects.count()
    out_of_stock = FoodItem.objects.filter(Q(stock=0) | Q(is_available=False)).count()
    low_stock = FoodItem.objects.filter(stock__gt=0, stock__lte=10, is_available=True).count()
    
    total_categories = Category.objects.count()
    total_reviews = Review.objects.count()

    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'active_orders': active_orders,
        'total_products': total_products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'total_categories': total_categories,
        'total_reviews': total_reviews,
    }
