from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Category, Product

# Create your views here.


def index(request):
    return render(
        request=request,
        template_name='shop/product/index.html',
        context={
            'section': 'home'
        }
    )


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(klass=Category, slug=category_slug)
        products = products.filter(category=category)

        # pagination with 9 products per page
    paginator = Paginator(object_list=products, per_page=9)
    page_number = request.GET.get('page', 1)
    product_list = paginator.page(number=page_number)

    return render(
        request=request,
        template_name='shop/product/list.html',
        context={
            'category': category,
            'products': product_list,
            'section': 'shop',
            'all_available_products_count': len(products),
            "num_range": range(10),
            'featured_num_range': range(4)
        }
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        klass=Product,
        id=id,
        slug=slug,
        available=True
    )

    return render(
        request=request,
        template_name='shop/product/detail.html',
        context={
            'product': product,
            'section': 'shop'
        }
    )
