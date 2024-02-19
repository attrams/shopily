from io import BytesIO
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task
import weasyprint

from orders.models import Order


@shared_task
def payment_completed(order_id):
    '''
    Task to send an e-mail notification when an order is successfully paid.
    '''
    order = Order.objects.get(id=order_id)

    # create invoice email
    subject = f'Shopily - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email='admin@shopily.com',
        to=[order.email]

    )

    # generate pdf
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach PDF file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # send e-mail
    email.send()
