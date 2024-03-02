"""
URL configuration for shopily project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from payment import webhooks

from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(route=_('cart/'), view=include('cart.urls', namespace='cart')),
    path(route=_('orders/'), view=include('orders.urls', namespace='orders')),
    path(route=_('payment/'), view=include('payment.urls', namespace='payment')),
    path(route=_('coupons/'), view=include('coupons.urls', namespace='coupons')),
    path(route=_('blog/'), view=include('blog.urls', namespace='blog')),
    path(route=_('accounts/'), view=include('accounts.urls', namespace='accounts')),
    path(route='rosetta/', view=include('rosetta.urls')),
    path(route='', view=include('shop.urls', namespace='shop')),
)

urlpatterns += [
    path('payment/webhook/', webhooks.stripe_webhook, name='stripe-webhook'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
