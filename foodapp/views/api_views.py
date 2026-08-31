from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from foodapp.decorators import superuser_required
from foodapp.models import FoodItem, Category, Order

@superuser_required
@require_POST
def api_update_price(request, food_id):
    """
    Super User Protected API to update food price & discount.
    """
    food = get_object_or_404(FoodItem, id=food_id)
    
    try:
        new_price = float(request.POST.get('price', 0))
        discount_price = request.POST.get('discount_price', None)
        
        if new_price <= 0:
            return JsonResponse({'error': 'Price must be greater than zero.'}, status=400)
            
        food.price = new_price
        if discount_price and float(discount_price) > 0:
            if float(discount_price) >= new_price:
                return JsonResponse({'error': 'Discount price must be lower than original price.'}, status=400)
            food.discount_price = float(discount_price)
        else:
            food.discount_price = None
            
        food.save()
        return JsonResponse({
            'success': True,
            'price': float(food.price),
            'effective_price': float(food.effective_price),
            'has_discount': food.has_discount,
            'discount_percent': food.discount_percent
        })
    except (ValueError, TypeError) as e:
        return JsonResponse({'error': f'Invalid input: {str(e)}'}, status=400)

@superuser_required
@require_POST
def api_update_stock(request, food_id):
    """
    Super User Protected API to update inventory stock.
    """
    food = get_object_or_404(FoodItem, id=food_id)
    
    try:
        new_stock = int(request.POST.get('stock', 0))
        if new_stock < 0:
            return JsonResponse({'error': 'Stock quantity cannot be negative.'}, status=400)
            
        food.stock = new_stock
        if new_stock == 0:
            food.is_available = False
        food.save()
        
        return JsonResponse({
            'success': True,
            'stock': food.stock,
            'is_available': food.is_available
        })
    except (ValueError, TypeError) as e:
        return JsonResponse({'error': f'Invalid stock value: {str(e)}'}, status=400)
