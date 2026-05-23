
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return None


class ProductWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'





