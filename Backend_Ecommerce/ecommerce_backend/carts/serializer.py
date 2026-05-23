
from rest_framework import serializers
from .models import Cart,CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=["id","product","quantity"]



class CartSerializer(serializers.ModelSerializer):

    items=CartItemSerializer(many=True)

    class Meta: 

        model = Cart
        fields = ["id","user","items"]
        read_only_fields = ["user"]
        

    def create(self,validated_data):
        
        user = self.context["request"].user

        item_data = validated_data.pop("items")

        cart, created = Cart.objects.get_or_create(user=user)

        for item in item_data:

            product = item["product"]
            quantity = item["quantity"]
            
            cartItem,item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity":quantity}
            )

            if not item_created:
                cartItem.quantity += quantity
                cartItem.save()
         

        return cart


# ------------------------------------------------------------------------------------------------------------------------


from products.models import Product
from products.serializer import ProductSerializer


class CartItemGetSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id","product", "quantity"]


class CartGetSerializer(serializers.ModelSerializer):

    items = CartItemGetSerializer(many=True, read_only=True)

    subtotal = serializers.SerializerMethodField()

    shipping_fee = serializers.SerializerMethodField()

    final_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "subtotal",
            "shipping_fee",
            "final_total",
             "items",
        ]

        read_only_fields = ["user"]

    def get_subtotal(self, obj):

        subtotal = 0

        for item in obj.items.all():

            subtotal += item.product.price * item.quantity

        return subtotal

    def get_shipping_fee(self, obj):

        subtotal = self.get_subtotal(obj)

        if subtotal > 500:
            return 0

        return 40

    def get_final_total(self, obj):

        subtotal = self.get_subtotal(obj)

        shipping = self.get_shipping_fee(obj)

        return subtotal + shipping

# ---------------------------------------------------------------------------------------------------------------------

# serializers.py

from rest_framework import serializers
from .models import CartItem


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ["quantity"]

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0"
            )

        if value>10:
            raise serializers.ValidationError(
                "Quantity limit is up to 10"
            )


        return value






