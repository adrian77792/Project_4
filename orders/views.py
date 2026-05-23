from django.shortcuts import render
from products.models import Product
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from decimal import Decimal


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_success(request):
    return render(request, "orders/payment_success.html")

def checkout(request):

    cart = request.session.get("cart", {})

    line_items = []

    total = 0

    for product_id, qty in cart.items():

        product = Product.objects.get(id=product_id)

        # cena po rabacie
        final_price = product.price

        if product.discount:
            final_price = product.price * (Decimal("1") - (Decimal(product.discount) / Decimal("100")))
        else:
            final_price = product.price

        total += final_price * qty

        line_items.append({
            "price_data": {
                "currency": "pln",
                "product_data": {
                    "name": product.name,
                },
                "unit_amount": int(final_price * 100),
            },
            "quantity": qty,
        })

    # 🚚 DOSTAWA
    delivery_cost = 20  # albo logika z Twojego view

    line_items.append({
        "price_data": {
            "currency": "pln",
            "product_data": {
                "name": "Dostawa",
            },
            "unit_amount": int(delivery_cost * 100),
        },
        "quantity": 1,
    })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("orders:payment_success")
        ),
        cancel_url=request.build_absolute_uri(
            reverse("products:cart")
        ),
    )

    return redirect(session.url)