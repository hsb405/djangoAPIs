from bson import ObjectId
from .models import Products
from rest_framework import status
from .serializers import ProductsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from order_processing.serializers import OrderSerializer


@api_view(["POST"])
def add_product(request):
    """
    Add a new product in the Database.
    Validates all the data is in correct format.
    """
    serializer = ProductsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_stock(request, product_id):
    """
    Updates the stock quantity in the database.
    First validates the data and then update.
    """
    try:
        product_id = ObjectId(product_id)
    except Exception:
        return Response(
            {"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = Products.objects.get(product_id=product_id)
    except Products.DoesNotExist:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductsSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def check_stock(request):
    """
    Check the stock quantity before placing order,
    whether it is enough or not
    """
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        product_name = serializer.validated_data["product_name"]
        quantity = serializer.validated_data["quantity"]

        try:
            product = Products.objects.get(product_name=product_name)

            if product.stock_quantity < quantity:
                return Response(
                    {"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {"message": "Stock is available"}, status=status.HTTP_200_OK
            )

        except Products.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def stock_alert(request):
    """
    Provide the alert that inventory stock is running short.
    """

    serializer=ProductsSerializer(fdata=request.data)
    if serializer.is_valid():
        product_id =serializer.validated_data["product_id"]
        current_stock=serializer.validated_data["stock_quantity"]
        threshold_value=serializer.validated_data["threshold"]

        if current_stock<threshold_value:
            return Response({"message":"Stock level is very low"})
        else:
            return Response({"message":"Stock quantity is sufficient"})
    
    return Response(status=status.HTTP_200_OK)



