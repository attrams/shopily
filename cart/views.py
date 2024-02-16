from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal
import json

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(
            product=product,
            quantity=cleaned_data['quantity'],
            override_quantity=cleaned_data['override']
        )
        # handle POST request from ajax call
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'redirect': True, 'redirect_url': reverse('cart:cart_detail')})
        else:
            # in case you use form to submit request instead of ajax
            return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(json.loads(request.body)['quantity'])

    cart.add(
        product=product,
        quantity=quantity,
        override_quantity=True
    )

    cart_subtotal = cart.get_total_price()
    updated_item_quantity = cart.cart.get(
        str(product_id), {}).get('quantity', 0)
    updated_item_total_price = quantity * Decimal(product.price)
    cart_total_items_count = len(cart)

    return JsonResponse({
        'cartSubtotalPrice': str(cart_subtotal),
        'cartTotalPrice': str(cart_subtotal),
        'updatedItemQuantity': updated_item_quantity,
        'updatedItemTotalPrice': str(updated_item_total_price),
        'cartTotalItems': cart_total_items_count,
        'success': True
    })


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    return render(request=request, template_name='cart/detail.html', context={'cart': cart, 'section': 'shop'})
