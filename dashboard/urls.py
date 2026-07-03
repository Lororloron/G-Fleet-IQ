from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("drivers/", views.drivers, name="drivers"),
    path("customers/", views.customers, name="customers"),
    path("trucks/", views.trucks, name="trucks"),
    path("loads/", views.loads, name="loads"),
]