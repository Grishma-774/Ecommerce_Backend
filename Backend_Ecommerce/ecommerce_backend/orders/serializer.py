
from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from products.serializer import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]   


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    shipping_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "name",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
            "payment",
            "payment_status",
            "order_status",
            "subtotal",
            "shipping_fee",
            "total",
            "items"
        ]

    def create(self, validated_data):

        items_data = validated_data.pop("items")
        user = self.context["request"].user

        subtotal = 0

        # Step 1: calculate subtotal using REAL product price
        for item in items_data:
            product = item["product"]
            subtotal += product.price * item["quantity"]

        # Step 2: shipping logic
        if subtotal > 500:
            shipping = 0
        else:
            shipping = 40

        total = subtotal + shipping

        payment_method = validated_data.get("payment")

        if payment_method == "upi":
            payment_status = "paid"
        else:
            payment_status = "pending"


        # Step 3: create order
        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            shipping_fee=shipping,
            total=total,
            payment_status=payment_status,
            **validated_data
        )

        # Step 4: create order items
        for item in items_data:
            product = item["product"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=product.price   # snapshot price
            )

        return order


# ------------------------------------------------------------------------------------------------------


class Order_HistorySerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:

        model = OrderItem
        fields = ["id","quantity","price","product"]


class OrderDetailsSerializer(serializers.ModelSerializer):

    items = Order_HistorySerializer(many=True,read_only=True)

    payment = serializers.CharField(source="get_payment_display", read_only=True)

    payment_status = serializers.CharField(
        source="get_payment_status_display",
        read_only=True
    )

    order_status = serializers.CharField(
        source="get_order_status_display",
        read_only=True
    )


    class Meta: 

        model = Order
        fields = ["id","name","total","order_code","shipping_fee","subtotal","payment","payment_status","order_status","items"]


# -----------------------------------------------------------------------------------------------------------------


class OneOrderDetailsSerializer(serializers.ModelSerializer):

    items = Order_HistorySerializer(many=True,read_only=True)

    payment = serializers.CharField(source="get_payment_display", read_only=True)

    payment_status = serializers.CharField(
        source="get_payment_status_display",
        read_only=True
    )

    order_status = serializers.CharField(
        source="get_order_status_display",
        read_only=True
    )

    

    class Meta: 

        model = Order
        fields = ["id","total","name","order_code","shipping_fee","subtotal","payment","payment_status","order_status","items"]



# --------------------------------------------------------------------------------------------------------------------------

#Admin 

class AdminOrderDetailsSerializer(serializers.ModelSerializer):

    items = Order_HistorySerializer(many=True,read_only=True)

    
    class Meta: 

        model = Order
        fields = ["id","total","name","phone","address","city","state","pincode","created_at","order_code","shipping_fee","subtotal","payment","payment_status","order_status","items"]




class AdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Order
        
        fields = ["order_status","payment_status"]
        
    