from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from foodapp.decorators import superuser_required
from foodapp.models import FoodItem, Category, Order, OrderItem
from foodapp.forms import FoodItemForm, CategoryForm
from foodapp.utils import get_dashboard_stats

@superuser_required
def dashboard_home(request):
    """
    Super User Overview Dashboard: Stat Cards, Recent Orders, Low Stock Alerts.
    """
    stats = get_dashboard_stats()
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:8]
    low_stock_items = FoodItem.objects.filter(Q(stock__lte=10) | Q(is_available=False)).select_related('category')[:8]
    
    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'recent_orders': recent_orders,
        'low_stock_items': low_stock_items,
        'active_nav': 'overview'
    })

# --- Product Management ---

@superuser_required
def dashboard_item_list(request):
    """
    Super User Product Management List with search & category filtering.
    """
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    stock_status = request.GET.get('stock', '')

    items = FoodItem.objects.all().select_related('category')

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id and category_id.isdigit():
        items = items.filter(category_id=category_id)

    if stock_status == 'out':
        items = items.filter(Q(stock=0) | Q(is_available=False))
    elif stock_status == 'low':
        items = items.filter(stock__gt=0, stock__lte=10, is_available=True)
    elif stock_status == 'available':
        items = items.filter(stock__gt=0, is_available=True)

    categories = Category.objects.all()

    return render(request, 'dashboard/items/list.html', {
        'items': items,
        'categories': categories,
        'selected_category': category_id,
        'selected_stock': stock_status,
        'query': query,
        'active_nav': 'items'
    })

@superuser_required
def dashboard_item_add(request):
    """
    Super User Add Food Item View with validation.
    """
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save()
            messages.success(request, f"Food item '{food.name}' added successfully!")
            return redirect('dashboard_item_list')
        else:
            messages.error(request, "Please correct the errors in the food item form.")
    else:
        form = FoodItemForm()

    return render(request, 'dashboard/items/form.html', {
        'form': form,
        'title': 'Add New Food Item',
        'button_text': 'Create Item',
        'active_nav': 'items'
    })

@superuser_required
def dashboard_item_edit(request, pk):
    """
    Super User Edit Food Item & Price Management View.
    """
    food = get_object_or_404(FoodItem, pk=pk)

    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            updated_food = form.save()
            messages.success(request, f"Food item '{updated_food.name}' updated successfully!")
            return redirect('dashboard_item_list')
        else:
            messages.error(request, "Please correct the errors in the food item form.")
    else:
        form = FoodItemForm(instance=food)

    return render(request, 'dashboard/items/form.html', {
        'form': form,
        'food': food,
        'title': f"Edit Item: {food.name}",
        'button_text': 'Update Item',
        'active_nav': 'items'
    })

@superuser_required
@require_POST
def dashboard_item_delete(request, pk):
    """
    Super User Safe Delete Item View.
    """
    food = get_object_or_404(FoodItem, pk=pk)
    food_name = food.name

    try:
        food.delete()
        messages.success(request, f"Item '{food_name}' deleted successfully.")
    except Exception as e:
        # Fallback to soft delete if protected foreign keys exist
        food.is_available = False
        food.stock = 0
        food.save()
        messages.warning(request, f"Item '{food_name}' has associated orders. It has been marked as unavailable instead of total deletion.")

    return redirect('dashboard_item_list')

@superuser_required
@require_POST
def dashboard_toggle_availability(request, pk):
    """
    Quickly toggle food item availability.
    """
    food = get_object_or_404(FoodItem, pk=pk)
    food.is_available = not food.is_available
    food.save()

    status_str = "Available" if food.is_available else "Unavailable"
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'is_available': food.is_available, 'status': status_str})

    messages.info(request, f"Item '{food.name}' is now {status_str}.")
    return redirect('dashboard_item_list')


# --- Category Management ---

@superuser_required
def dashboard_category_list(request):
    """
    Super User Category Management List & Add Form.
    """
    categories = Category.objects.annotate(item_count=Count('foods'))
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created successfully!")
            return redirect('dashboard_category_list')
        else:
            messages.error(request, "Please correct the errors in the category form.")

    return render(request, 'dashboard/categories/list.html', {
        'categories': categories,
        'form': form,
        'active_nav': 'categories'
    })

@superuser_required
def dashboard_category_edit(request, pk):
    """
    Super User Edit Category View.
    """
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated successfully!")
            return redirect('dashboard_category_list')
        else:
            messages.error(request, "Please correct the errors in the category form.")
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/categories/form.html', {
        'form': form,
        'category': category,
        'active_nav': 'categories'
    })

@superuser_required
@require_POST
def dashboard_category_delete(request, pk):
    """
    Super User Delete Category View.
    """
    category = get_object_or_404(Category, pk=pk)
    cat_name = category.name

    if category.foods.exists():
        messages.error(request, f"Cannot delete category '{cat_name}' because it contains food items. Move or delete the items first.")
        return redirect('dashboard_category_list')

    category.delete()
    messages.success(request, f"Category '{cat_name}' deleted successfully.")
    return redirect('dashboard_category_list')


# --- Order Management ---

@superuser_required
def dashboard_order_list(request):
    """
    Super User All Customer Orders View with status filters.
    """
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()

    orders = Order.objects.select_related('user').all().order_by('-created_at')

    if status_filter:
        orders = orders.filter(status=status_filter)

    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    return render(request, 'dashboard/orders/list.html', {
        'orders': orders,
        'selected_status': status_filter,
        'query': query,
        'status_choices': Order.STATUS_CHOICES,
        'active_nav': 'orders'
    })

@superuser_required
def dashboard_order_detail(request, pk):
    """
    Super User Individual Order Management & Status Change View.
    """
    order = get_object_or_404(Order.objects.select_related('user').prefetch_related('items__food_item'), pk=pk)
    
    return render(request, 'dashboard/orders/detail.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
        'active_nav': 'orders'
    })

@superuser_required
@require_POST
def dashboard_order_status_update(request, pk):
    """
    Super User Change Order Status Endpoint.
    """
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status', '')

    valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
    if new_status in valid_statuses:
        old_status = order.get_status_display()
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.order_number} status changed from '{old_status}' to '{order.get_status_display()}'.")
    else:
        messages.error(request, "Invalid status choice selected.")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'new_status': order.status, 'status_display': order.get_status_display()})

    next_url = request.POST.get('next', '')
    if next_url:
        return redirect(next_url)
    return redirect('dashboard_order_detail', pk=pk)


# --- Inventory Stock Management ---

@superuser_required
def dashboard_inventory(request):
    """
    Super User Quick Stock & Inventory Management View.
    """
    if request.method == 'POST':
        # Batch update stock values
        updated_count = 0
        for key, value in request.POST.items():
            if key.startswith('stock_'):
                try:
                    item_id = int(key.split('_')[1])
                    new_stock = int(value)
                    if new_stock >= 0:
                        item = FoodItem.objects.get(id=item_id)
                        item.stock = new_stock
                        if new_stock == 0:
                            item.is_available = False
                        elif new_stock > 0 and not item.is_available:
                            item.is_available = True
                        item.save()
                        updated_count += 1
                except (ValueError, FoodItem.DoesNotExist):
                    continue

        messages.success(request, f"Updated stock for {updated_count} food items successfully.")
        return redirect('dashboard_inventory')

    items = FoodItem.objects.all().select_related('category').order_by('stock')

    return render(request, 'dashboard/inventory.html', {
        'items': items,
        'active_nav': 'inventory'
    })
