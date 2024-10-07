from .models import Order
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from inventory_management.models import Products

@api_view(["POST"])
def place_order(request):
    """
    Place  a order of your desird products.
    If product is available in stock then place order
    """
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        product_name = serializer.validated_data["product_name"]
        customer_name=serializer.validated_data["customer_name"]
        quantity = serializer.validated_data["quantity"]
        delivery_address=serializer.validated_data["delivery_address"]
        

        try:
            product = Products.objects.get(product_name=product_name)
            if product.stock_quantity < quantity:
                return Response({"error": "Stock is Insufficient"}, status=status.HTTP_400_BAD_REQUEST)

            new_order = Order(
                customer_name=serializer.validated_data["customer_name"],
                product_name=product_name,
                customer_name=customer_name,
                quantity=quantity,
                delivery_address=delivery_address

                
            )
            new_order.save()  

            product.stock_quantity =product.stock_quantity - quantity
            product.save() 
            return Response(OrderSerializer(new_order).data, status=status.HTTP_201_CREATED)

        except Products.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def update_order(request, order_id):
    """
    Update the order by the order_id.
    Also manage the inventory stock while updating order.
    """
    try:
        order = Order.objects.get(order_id=order_id)  
        current_quantity = order.quantity  
        product_name = order.product_name 
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data)
    if serializer.is_valid():
     
        new_quantity = serializer.validated_data.get("quantity", current_quantity)
        
        product = Products.objects.get(product_name=product_name) 

        quantity=product.stock_quantity+current_quantity
        if quantity < new_quantity:
            return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
       
        else:
            product.stock_quantity = current_quantity + new_quantity  
            product.save()  

        serializer.save() 
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def cancel_order(request, order_id):
    """
    Deletes the order from the database.
    Also restock the inventory stock quantity.
    """
    try:
        order = Order.objects.get(order_id=order_id)
        product_name = order.product_name  
        quantity = order.quantity 

        product = Products.objects.get(product_name=product_name)

        product.stock_quantity =product.stock_quantity + quantity  
        product.save() 

        order.delete()
        return Response({"message": "Order canceled successfully"}, status=status.HTTP_204_NO_CONTENT)

    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)