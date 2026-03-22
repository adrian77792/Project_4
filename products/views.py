from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .models import Category
from decimal import Decimal

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
            "categories": categories
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


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('products:cart')

def view_cart(request):
    cart = request.session.get('cart', {})  # sesyjny koszyk
    cart_items = []
    cart_count = sum(cart.values())    
    
    total_price = Decimal(0)
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
        total_price += product.price * quantity

    breadcrumbs = [{'name': 'Home', 'url': '/'}, {'name': 'Cart', 'url': ''}]
    
    products = list(Product.objects.all())
    latest_products = sorted(products, key=lambda p: p.id, reverse=True)[:4]

    return render(request, 'products/cart.html', {
        "latest_products": latest_products,
        'cart_items': cart_items,
        "cart_count": cart_count,
        'total_price': total_price,
        'breadcrumbs': breadcrumbs
    })