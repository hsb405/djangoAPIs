from django.urls import path
from . import views

urlpatterns = [
    path("place", views.place_order, name="create_order"),
    path("update/<order_id>", views.update_order, name="update_order"),
    path("cancel/<order_id>", views.cancel_order, name="get_order_details"),
]
