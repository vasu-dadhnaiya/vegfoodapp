from foodapp.views.catalog_views import home, menu, food_detail
from foodapp.views.cart_views import cart_detail, cart_add, cart_remove, cart_update, cart_clear, cart_context_processor, get_cart_details
from foodapp.views.checkout_views import checkout, order_success, my_orders, order_detail
from foodapp.views.auth_views import register_view, login_view, logout_view, profile_view
from foodapp.views.review_views import add_review
from foodapp.views.dashboard_views import (
    dashboard_home,
    dashboard_item_list,
    dashboard_item_add,
    dashboard_item_edit,
    dashboard_item_delete,
    dashboard_toggle_availability,
    dashboard_category_list,
    dashboard_category_edit,
    dashboard_category_delete,
    dashboard_order_list,
    dashboard_order_detail,
    dashboard_order_status_update,
    dashboard_inventory
)
from foodapp.views.api_views import api_update_price, api_update_stock
from foodapp.views.error_views import custom_permission_denied, custom_page_not_found, custom_server_error

__all__ = [
    'home',
    'menu',
    'food_detail',
    'cart_detail',
    'cart_add',
    'cart_remove',
    'cart_update',
    'cart_clear',
    'cart_context_processor',
    'get_cart_details',
    'checkout',
    'order_success',
    'my_orders',
    'order_detail',
    'register_view',
    'login_view',
    'logout_view',
    'profile_view',
    'add_review',
    'dashboard_home',
    'dashboard_item_list',
    'dashboard_item_add',
    'dashboard_item_edit',
    'dashboard_item_delete',
    'dashboard_toggle_availability',
    'dashboard_category_list',
    'dashboard_category_edit',
    'dashboard_category_delete',
    'dashboard_order_list',
    'dashboard_order_detail',
    'dashboard_order_status_update',
    'dashboard_inventory',
    'api_update_price',
    'api_update_stock',
    'custom_permission_denied',
    'custom_page_not_found',
    'custom_server_error',
]
