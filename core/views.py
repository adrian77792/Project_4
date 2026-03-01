from django.shortcuts import render, get_object_or_404
from products.models import Product, Category



"""def home(request):
    products = Product.objects.all()
    for p in products:
        if p.discount:
            p.discounted_price = p.price - (p.price * p.discount / 100)
    categories = Category.objects.all()[:6]
    print (categories)
    return render(request, "core/index.html",
                  {"products":products, "categories":categories})"""


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

def home(request):
    products = list(Product.objects.all())

   
    latest_products = sorted(products, key=lambda p: p.id, reverse=True)[:4]

 
    discounted_products = []
    for p in products:
        if p.discount:
            try:
                p.discounted_price = p.price - (p.price * p.discount / 100)
                discounted_products.append(p)
            except TypeError:
                pass  # zabezpieczenie gdyby price/discount były None

    discounted_products = discounted_products[:4]

  
    categories = list(Category.objects.all()[:6])

    return render(request, "core/index.html", {
        "latest_products": latest_products,
        "discounted_products": discounted_products,
        "categories": categories,
    })

def about_us(request):
    breadcrumbs = generate_breadcrumbs(request)
    return render(request, "core/about_us.html", {
        "breadcrumbs": breadcrumbs,
        "title": breadcrumbs[-1]['name'] if breadcrumbs else 'Home'
    })
