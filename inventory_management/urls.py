from . import views
from django.urls import path

urlpatterns = [
    path("add/product", views.add_product, name="add_product"),
    path("update/product/<product_id>", views.update_stock, name="update_stock"),
    path("check/stock/<product_id>", views.check_stock, name="check_stock"),
    path("alert",views.stock_alert,name="stock_alert")
]
