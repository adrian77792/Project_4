from django.shortcuts import render, get_object_or_404
from products.models import Product
from products.models import Category


def home(request):
    products = Product.objects.all()
    for p in products:
        if p.discount:
            p.discounted_price = p.price - (p.price * p.discount / 100)
    categories = Category.objects.all()[:4]
    print (categories)
    return render(request, "core/index.html",
                  {"products":products, "categories":categories})
