from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product
from .models import Product
from .models import Category
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html",
                  {"products":products})
                  

def product_detail(request, category_slug, slug):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    product = get_object_or_404(
        Product,
        slug=slug,
        category__slug=category_slug
    )

    breadcrumbs = generate_breadcrumbs(request)

    return render(
        request,
        "products/product_page.html",
        {
            "product": product,
            "cart_count": cart_count,
            "breadcrumbs": breadcrumbs
        }
    )

def generate_breadcrumbs(request):
    path_parts = [part for part in request.path.strip('/').split('/') if part]
    breadcrumbs = []
    accumulated_path = ''

    for part in path_parts:
        accumulated_path += f'/{part}'
        name = ' '.join([w.capitalize() for w in part.replace('-', ' ').replace('_', ' ').split()])
        breadcrumbs.append({
            'name': name,
            'url': accumulated_path
        })
    if breadcrumbs:
        breadcrumbs[-1]['url'] = ''
    return breadcrumbs
    

def category_list(request):
    categories = Category.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())    
    return render(request, "products/category_list.html", {
        "categories": categories,
        "cart_count": cart_count
    })    
    
    
def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())    
    products = category.products.all()
    paginator = Paginator(products, 12)  # 12 produktów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = list(Category.objects.all()[:6])

    breadcrumbs = generate_breadcrumbs(request)

    return render(
        request,
        "products/category_products.html",
        {
            "category": category,
            "cart_count": cart_count,
            "products": products,
            "breadcrumbs": breadcrumbs,
            "categories": categories,
            'page_obj': page_obj
        }
    )    
    
def products_by_category(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    categories = Category.objects.prefetch_related("products")

    return render(request, "products/products_by_category.html", {
        "categories": categories
    })
    
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))
    
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
def subtract_from_cart(request, product_id):

    get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        cart[pid] -= 1

        if cart[pid] <= 0:
            del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER', '/'))    


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('products:cart')

def view_cart(request):
    today = date.today()
    delivery_from = today + timedelta(days=3)
    delivery_to = today + timedelta(days=7)

    cart = request.session.get('cart', {})
    cart_items = []

    cart_count = sum(cart.values())

    total_price = Decimal('0.00')          # po rabatach
    total_full_price = Decimal('0.00')     # bez rabatów
    total_discount_value = Decimal('0.00') # suma rabatów
    delivery_cost = Decimal('20.00')

    invalid_keys = []

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            invalid_keys.append(product_id)
            continue

        full_price = product.price * quantity

        discount_multiplier = Decimal('1.0') - (Decimal(product.discount or 0) / Decimal('100'))
        effective_unit_price = product.price * discount_multiplier
        effective_unit_price = effective_unit_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        subtotal = (effective_unit_price * quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        full_subtotal = full_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        discount_value = (full_subtotal - subtotal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': effective_unit_price,
            'subtotal': subtotal
        })

        total_price += subtotal
        total_full_price += full_subtotal
        total_discount_value += discount_value

    for key in invalid_keys:
        del cart[key]

    if invalid_keys:
        request.session['cart'] = cart
        request.session.modified = True

    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Cart', 'url': ''}
    ]

    latest_products = Product.objects.order_by('-id')[:4]
    
    total_price = total_price + delivery_cost

    return render(request, 'products/cart.html', {
        'latest_products': latest_products,
        'cart_items': cart_items,
        'cart_count': sum(cart.values()),
        'total_price': total_price,
        'total_full_price': total_full_price,
        'total_discount_value': total_discount_value,
        'delivery_cost': delivery_cost,
        'breadcrumbs': breadcrumbs,
        "delivery_from": delivery_from,
        "delivery_to": delivery_to
    })


@require_POST
def update_cart(request, product_id):

    cart = request.session.get('cart', {})

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    product_id = str(product_id)

    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('products:cart')