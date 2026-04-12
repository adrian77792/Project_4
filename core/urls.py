from django.urls import path
from . import views
 
app_name = "core"
 
urlpatterns = [
    path("", views.home, name="home"),
    path("about_us", views.about_us, name="about us"),
    path("contact", views.contact, name="contact"),
    path('news/', views.news_list, name='news_list'),
]