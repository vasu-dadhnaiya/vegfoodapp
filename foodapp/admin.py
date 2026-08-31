from django.contrib import admin
from foodapp.models import Category, FoodItem, Order, OrderItem, Review

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount_price", "stock", "is_available", "created_at")
    list_filter = ("is_available", "category")
    search_fields = ("name", "description", "slug")
    list_editable = ("price", "discount_price", "stock", "is_available")
    prepopulated_fields = {"slug": ("name",)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("food_item", "food_name", "quantity", "price", "subtotal")


    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = "Subtotal (₹)"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "name", "email", "phone", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "name", "email", "phone", "delivery_address")
    list_editable = ("status",)
    inlines = [OrderItemInline]
    readonly_fields = ("order_number", "total_amount", "created_at")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "food_item", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "food_item__name", "comment")
