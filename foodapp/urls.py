from django.urls import path
from foodapp import views

urlpatterns = [
    # Customer Catalog
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('food/<int:pk>/', views.food_detail, name='food_detail'),
    
    # Shopping Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:food_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:food_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('food/<int:food_id>/review/', views.add_review, name='add_review'),
    
    # Authentication & User Profile
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # --- Strict Super User Management Dashboard Routes ---
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    
    # Super User Food Item / Product Management
    path('dashboard/items/', views.dashboard_item_list, name='dashboard_item_list'),
    path('dashboard/items/add/', views.dashboard_item_add, name='dashboard_item_add'),
    path('dashboard/items/<int:pk>/edit/', views.dashboard_item_edit, name='dashboard_item_edit'),
    path('dashboard/items/<int:pk>/delete/', views.dashboard_item_delete, name='dashboard_item_delete'),
    path('dashboard/items/<int:pk>/toggle-availability/', views.dashboard_toggle_availability, name='dashboard_toggle_availability'),
    
    # Super User Category Management
    path('dashboard/categories/', views.dashboard_category_list, name='dashboard_category_list'),
    path('dashboard/categories/<int:pk>/edit/', views.dashboard_category_edit, name='dashboard_category_edit'),
    path('dashboard/categories/<int:pk>/delete/', views.dashboard_category_delete, name='dashboard_category_delete'),
    
    # Super User Order Fulfillment & Tracking
    path('dashboard/orders/', views.dashboard_order_list, name='dashboard_order_list'),
    path('dashboard/orders/<int:pk>/', views.dashboard_order_detail, name='dashboard_order_detail'),
    path('dashboard/orders/<int:pk>/status/', views.dashboard_order_status_update, name='dashboard_order_status_update'),
    
    # Super User Stock / Inventory Management
    path('dashboard/inventory/', views.dashboard_inventory, name='dashboard_inventory'),
    
    # Super User Protected APIs
    path('api/admin/items/<int:food_id>/price/', views.api_update_price, name='api_update_price'),
    path('api/admin/items/<int:food_id>/stock/', views.api_update_stock, name='api_update_stock'),
]