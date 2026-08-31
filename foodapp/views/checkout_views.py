from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from foodapp.models import Order, OrderItem, FoodItem
from foodapp.forms import CheckoutForm
from foodapp.views.cart_views import get_cart_details

@login_required
def checkout(request):
    cart_data = get_cart_details(request)
    if not cart_data['cart_items']:
        messages.warning(request, "Your cart is empty! Add items from the menu first.")
        return redirect('menu')
        
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create the main order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_amount = cart_data['grand_total']
                    order.save()
                    
                    for item in cart_data['cart_items']:
                        food = item['food']
                        qty = item['quantity']
                        
                        # Lock and fetch current stock in database
                        db_food = FoodItem.objects.select_for_update().get(id=food.id)
                        
                        if not db_food.is_available:
                            raise ValueError(f"Sorry, '{db_food.name}' is no longer available.")
                            
                        if db_food.stock < qty:
                            raise ValueError(f"Sorry, only {db_food.stock} units of '{db_food.name}' are available. Please adjust your cart.")
                            
                        # Deduct inventory stock
                        db_food.stock -= qty
                        if db_food.stock == 0:
                            db_food.is_available = False
                        db_food.save()
                        
                        # Create OrderItem with price and snapshot name
                        OrderItem.objects.create(
                            order=order,
                            food_item=db_food,
                            food_name=db_food.name,
                            quantity=qty,
                            price=db_food.effective_price
                        )
                    
                    # Clear session cart
                    request.session['cart'] = {}
                    request.session.modified = True
                    
                    messages.success(request, f"Order #{order.order_number} placed successfully!")
                    return redirect('order_success', order_id=order.id)
                    
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "An unexpected error occurred while placing your order. Please try again.")
        else:
            messages.error(request, "Please fix the errors in the form before submitting.")
    else:
        initial_data = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)
        
    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_data['cart_items'],
        'subtotal': cart_data['subtotal'],
        'delivery_charge': cart_data['delivery_charge'],
        'grand_total': cart_data['grand_total'],
    })

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    timeline = ['pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered']
    
    current_step = 0
    if order.status in timeline:
        current_step = timeline.index(order.status) + 1
    elif order.status == 'cancelled':
        current_step = -1
        
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'current_step': current_step,
        'timeline': timeline,
    })
