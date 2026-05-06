from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers # Added this
from .models import Product, Sale, Debt

# 1. Define a Serializer so the Browser shows you a Form with boxes
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']

@api_view(['GET', 'POST'])
def list_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        # Use the serializer to turn data into JSON
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        # Use the serializer to validate and save the data
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST']) 
def process_sale(request):
    if request.method == 'GET':
        return Response({"message": "Send a POST request with product_id and quantity."})

    p_id = request.data.get('product_id')
    qty = request.data.get('quantity')

    if not p_id or not qty:
        return Response({"error": "Please provide both product_id and quantity"}, status=400)

    try:
        product = Product.objects.get(id=p_id)
        qty = int(qty)
        
        if product.stock < qty:
            return Response({"error": "Insufficient stock"}, status=400)
            
        total = product.price * qty
        product.stock -= qty
        product.save()
        
        Sale.objects.create(product=product, quantity=qty, total_amount=total)
        
        return Response({
            "status": "success",
            "total_price": float(total),
            "remaining_stock": product.stock
        })
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    except ValueError:
        return Response({"error": "Quantity must be a number"}, status=400)

@api_view(['POST'])
def record_debt(request):
    customer = request.data.get('customer_name')
    amount = request.data.get('amount')

    if not customer or not amount:
        return Response({"error": "Provide customer_name and amount"}, status=400)

    debt = Debt.objects.create(customer_name=customer, amount=amount)
    return Response({
        "status": "Debt recorded",
        "id": debt.id,
        "customer": debt.customer_name,
        "amount": float(debt.amount)
    })