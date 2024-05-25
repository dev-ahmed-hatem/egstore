from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
from .forms import UserAdmin


class InlineProductImage(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineProductImage]


admin.site.unregister(Group)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Sale)
