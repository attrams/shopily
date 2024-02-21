from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

import weasyprint

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from shop.recommender import Recommender

# Create your views here.


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            order.save()

            # products for recommendation
            products = []

            for item in cart:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                products.append(order_item.product)

            # Record products bought together
            recommender = Recommender()
            recommender.products_bought(products)

            # clear cart
            cart.clear()

            # Remove the coupon from the session after order creation
            if 'coupon_id' in request.session:
                del request.session['coupon_id']

            # send mail asynchronously
            order_created.delay(order.id)

            # set the order in the session
            request.session['order_id'] = order.id

            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()

    return render(
        request=request,
        template_name='orders/order/create.html',
        context={
            'cart': cart,
            'form': form,
            'section': 'shop'
        })


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(
        request=request,
        template_name='admin/orders/order/detail.html',
        context={
            'order': order
        }
    )


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')
    ])

    return response
