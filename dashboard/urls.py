from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("drivers/", views.drivers, name="drivers"),
    path("customers/", views.customers, name="customers"),
    path("trucks/", views.trucks, name="trucks"),
    path("loads/", views.loads, name="loads"),
    path("trailers/", views.trailers, name="trailers"),
    path("ai-dispatch/", views.ai_dispatch, name="ai_dispatch"),
]
path("dispatch-board/", views.dispatch_board, name="dispatch_board"),