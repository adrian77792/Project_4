from django.shortcuts import render, get_object_or_404
from products.models import Product
from products.models import Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()[:4]
    print (categories)
    return render(request, "core/index.html",
                  {"products":products, "categories":categories})
