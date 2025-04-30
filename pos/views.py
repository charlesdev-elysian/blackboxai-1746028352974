from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Category, Product, Sale, SaleItem, Customer
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'pos/index.html', {'categories': categories, 'products': products})

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'cart': cart})
    return JsonResponse({'status': 'fail'}, status=400)

def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        qty = cart.get(str(product.id), 0)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
    return render(request, 'pos/order_summary.html', {'cart_items': cart_items, 'total': total})

@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_name = data.get('customer_name', 'Walk-in Customer')
        payment_method = data.get('payment_method', 'Cash')
        cart = request.session.get('cart', {})
        if not cart:
            return JsonResponse({'status': 'fail', 'message': 'Cart is empty'}, status=400)
        customer, created = Customer.objects.get_or_create(name=customer_name)
        total_amount = 0
        sale = Sale.objects.create(customer=customer, date=timezone.now(), total_amount=0, payment_method=payment_method, paid=True)
        for product_id, qty in cart.items():
            product = Product.objects.get(id=product_id)
            SaleItem.objects.create(sale=sale, product=product, quantity=qty)
            total_amount += product.price * qty
        sale.total_amount = total_amount
        sale.save()
        request.session['cart'] = {}
        return JsonResponse({'status': 'success', 'sale_id': sale.id})
    return JsonResponse({'status': 'fail'}, status=400)
