from django.urls import path
from . import views

urlpatterns = [
    path("place", views.place_order, name="place_order"),
    path("update/<order_id>", views.update_order, name="update_order"),
    path("cancel/<order_id>", views.cancel_order, name="cancel_order"),
    path("status",views.order_status,name="order_status"),
    path("history",views.order_history,name="order_history")
]
