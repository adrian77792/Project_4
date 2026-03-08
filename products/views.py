from django.shortcuts import render, get_object_or_404
from .models import Product
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html",
                  {"products":products})
def product_detail(request, slug):
    breadcrumbs = generate_breadcrumbs(request)
    product = get_object_or_404(Product, slug=slug)
    return render(request, "products/product_page.html", {"product": product,"breadcrumbs": breadcrumbs } )


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