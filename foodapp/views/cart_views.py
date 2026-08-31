import decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from foodapp.models import FoodItem

def get_cart_details(request):
    """Helper function to calculate cart subtotals and fetch items with stock awareness"""
    cart_session = request.session.get('cart', {})
    cart_items = []
    subtotal = decimal.Decimal('0.00')

    food_ids = [int(fid) for fid in cart_session.keys() if fid.isdigit()]
    foods = FoodItem.objects.filter(id__in=food_ids, is_available=True)
    
    for food in foods:
        qty = int(cart_session[str(food.id)])
        # Clamp quantity to available stock
        if qty > food.stock:
            qty = max(1, food.stock)
            cart_session[str(food.id)] = qty
            request.session['cart'] = cart_session
            request.session.modified = True

        item_price = food.effective_price
        item_total = item_price * qty
        subtotal += item_total
        cart_items.append({
            'food': food,
            'quantity': qty,
            'price': item_price,
            'total': item_total,
        })
        
    delivery_charge = decimal.Decimal('40.00') if subtotal > 0 and subtotal < 500 else decimal.Decimal('0.00')
    grand_total = subtotal + delivery_charge

    return {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
        'total_items': sum(int(qty) for qty in cart_session.values())
    }

def cart_detail(request):
    cart_data = get_cart_details(request)
    return render(request, 'cart.html', cart_data)

def cart_add(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id, is_available=True)
    
    if food.stock <= 0:
        messages.error(request, f"Sorry, '{food.name}' is currently out of stock.")
        return redirect('menu')

    cart = request.session.get('cart', {})
    
    try:
        qty = int(request.POST.get('quantity', 1) if request.method == 'POST' else request.GET.get('quantity', 1))
    except (ValueError, TypeError):
        qty = 1

    if qty < 1:
        qty = 1
        
    food_id_str = str(food_id)
    current_in_cart = int(cart.get(food_id_str, 0))
    total_requested = current_in_cart + qty

    if total_requested > food.stock:
        allowed_add = max(0, food.stock - current_in_cart)
        if allowed_add > 0:
            cart[food_id_str] = food.stock
            messages.warning(request, f"Only {food.stock} units of '{food.name}' are in stock. Added maximum available.")
        else:
            messages.error(request, f"Cannot add more '{food.name}' to cart. Stock limit reached ({food.stock}).")
            return redirect('cart_detail')
    else:
        cart[food_id_str] = total_requested
        messages.success(request, f"{qty} x {food.name} added to cart!")
        
    request.session['cart'] = cart
    request.session.modified = True
    
    next_url = request.GET.get('next', 'menu')
    if next_url == 'cart':
        return redirect('cart_detail')
    return redirect('menu')

def cart_clear(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.info(request, "Your cart has been cleared.")
    return redirect('cart_detail')

def cart_remove(request, food_id):
    cart = request.session.get('cart', {})
    food_id_str = str(food_id)
    
    if food_id_str in cart:
        del cart[food_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, "Item removed from cart.")
        
    return redirect('cart_detail')

@require_POST
def cart_update(request):
    food_id = request.POST.get('food_id')
    action = request.POST.get('action')
    cart = request.session.get('cart', {})
    
    if not food_id or str(food_id) not in cart:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Item not found in cart'}, status=400)
        return redirect('cart_detail')
        
    food_id_str = str(food_id)
    qty = int(cart[food_id_str])
    food = FoodItem.objects.filter(id=food_id).first()

    if action == 'increase':
        if food and qty + 1 > food.stock:
            messages.warning(request, f"Cannot add more. Only {food.stock} units in stock.")
        else:
            cart[food_id_str] = qty + 1
    elif action == 'decrease':
        if qty > 1:
            cart[food_id_str] = qty - 1
        else:
            del cart[food_id_str]
            messages.info(request, "Item removed from cart.")
    elif action == 'set':
        new_qty = int(request.POST.get('quantity', 1))
        if new_qty > 0:
            if food and new_qty > food.stock:
                cart[food_id_str] = food.stock
                messages.warning(request, f"Adjusted to maximum available stock ({food.stock}).")
            else:
                cart[food_id_str] = new_qty
        else:
            del cart[food_id_str]
            messages.info(request, "Item removed from cart.")
            
    request.session['cart'] = cart
    request.session.modified = True
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_data = get_cart_details(request)
        item_total = decimal.Decimal('0.00')
        current_qty = cart.get(food_id_str, 0)
        if food and food_id_str in cart:
            item_total = food.effective_price * current_qty
            
        return JsonResponse({
            'success': True,
            'quantity': current_qty,
            'item_total': float(item_total),
            'subtotal': float(cart_data['subtotal']),
            'delivery_charge': float(cart_data['delivery_charge']),
            'grand_total': float(cart_data['grand_total']),
            'total_items': cart_data['total_items']
        })
        
    return redirect('cart_detail')

def cart_context_processor(request):
    """Context processor to inject total cart items count into all templates"""
    cart = request.session.get('cart', {})
    total_count = sum(int(qty) for qty in cart.values())
    return {
        'cart_count': total_count
    }

