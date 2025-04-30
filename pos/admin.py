from django.contrib import admin
from .models import Supplier, Customer, Category, Product, Purchase, Sale, SaleItem, Due, SalesReturn, PurchaseReturn

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')
    search_fields = ('name', 'contact')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')
    search_fields = ('name', 'contact')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'price', 'stock_quantity')
    search_fields = ('code', 'name')
    list_filter = ('category',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'product', 'quantity', 'price', 'discount', 'date')
    list_filter = ('date', 'supplier')
    search_fields = ('product__name', 'supplier__name')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'total_amount', 'payment_method', 'paid')
    list_filter = ('date', 'paid')
    search_fields = ('customer__name',)
    inlines = [SaleItemInline]

@admin.register(Due)
class DueAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'paid', 'date')
    list_filter = ('paid', 'date')
    search_fields = ('customer__name',)

@admin.register(SalesReturn)
class SalesReturnAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'date')
    list_filter = ('date',)
    search_fields = ('product__name',)

@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'product', 'quantity', 'date')
    list_filter = ('date',)
    search_fields = ('product__name',)
