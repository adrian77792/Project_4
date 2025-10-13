from django.urls import path
from . import views
 
app_name = "products"
 
urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:slug>/", views.product_detail, name="detail"),
    path("list", views.product_list, name="list"),
]