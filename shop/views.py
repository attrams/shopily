from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender
from blog.models import Post
from .forms import SearchForm

# Create your views here.


def index(request):
    posts = Post.published.all()[:3]

    return render(
        request=request,
        template_name='shop/product/index.html',
        context={
            'section': 'home',
            'posts': posts
        }
    )


def product_search(request):
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector(
                'name', 'description', 'category__name'
            )
            search_query = SearchQuery(query)
            results = Product.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    return render(
        request=request,
        template_name='shop/product/search.html',
        context={
            'results': results,
            'section': 'shop'
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
        }
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        klass=Product,
        id=id,
        slug=slug,
        available=True
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(
        request=request,
        template_name='shop/product/detail.html',
        context={
            'product': product,
            'section': 'shop',
            'cart_product_form': cart_product_form,
            'recommended_products': recommended_products
        }
    )
