from django.shortcuts import render
from products.models import Product, Category
from decimal import Decimal, ROUND_HALF_UP


def generate_breadcrumbs(request):
    path_parts = [part for part in request.path.strip('/').split('/') if part]
    breadcrumbs = []
    accumulated_path = ''

    for part in path_parts:
        accumulated_path += f'/{part}'
        name = ' '.join(
            [w.capitalize() for w in part.replace('-', ' ').replace('_', ' ').split()]
        )
        breadcrumbs.append({
            'name': name,
            'url': accumulated_path
        })

    if breadcrumbs:
        breadcrumbs[-1]['url'] = ''

    return breadcrumbs


def home(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    products = Product.objects.order_by('order', '-created_at')
    latest_products = Product.objects.order_by('-created_at')[:4]

    discounted_products = []
    for p in products:
        if p.discount:
            try:
                p.discounted_price = (p.price - (p.price * p.discount / Decimal('100'))).quantize(
                    Decimal('0.01'),
                    rounding=ROUND_HALF_UP
                )
                discounted_products.append(p)
            except TypeError:
                pass

    discounted_products = discounted_products[:4]

    categories = Category.objects.order_by('order')[:6]

    return render(request, "core/index.html", {
        "cart_count": cart_count,
        "latest_products": latest_products,
        "discounted_products": discounted_products,
        "categories": categories,
    })


def about_us(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    breadcrumbs = generate_breadcrumbs(request)

    return render(request, "core/about_us.html", {
        "breadcrumbs": breadcrumbs,
        "cart_count": cart_count,
        "title": breadcrumbs[-1]['name'] if breadcrumbs else 'Home'
    })