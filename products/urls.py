from django.urls import path
from . import views
 
app_name = "products"
 
urlpatterns = [
    path("list", views.product_list, name="list"),
    path("cart/", views.view_cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="cart_remove"),
    path("", views.products_by_category, name="products_by_category"),
    path("<slug:category_slug>/<slug:slug>/", views.product_detail, name="detail"),
    path("<slug:category_slug>/", views.category_products, name="category_products"),
    \
]


urlx = [
    path("category/<slug:slug>/", views.category_products, name="category_products"),
    path("<slug:slug>/", views.product_detail, name="detail"),
]