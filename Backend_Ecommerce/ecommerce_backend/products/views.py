from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q


from .models import Product
from .serializer import ProductSerializer,ProductWriteSerializer


@api_view(['GET'])
def product_list(request):

    products = Product.objects.all()

    search = request.GET.get("search")

    if search:
        products = products.filter(
            Q(title__icontains=search) |
            Q(category__icontains=search)
        )

    category = request.GET.get("category")

    if category and category.lower() != "all":
        products = products.filter(category__iexact=category)

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def product(request,pk):

    products = Product.objects.get(pk=pk)

    serializer = ProductSerializer(products)

    return Response(serializer.data)



# ---------------------------------------------------------------------------------------------------------------------

from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q


class AdminProductListCreate(APIView):

    permission_classes = [IsAdminUser]

    parser_classes = [MultiPartParser, FormParser]

    # GET ALL PRODUCTS
    def get(self, request):

        products = Product.objects.all()

        search = request.GET.get("search")
        category = request.GET.get("category")

        # ---------------- SEARCH ----------------
        if search:
            products = products.filter(
                Q(title__icontains=search) |
                Q(category__icontains=search)
            )

        # ---------------- CATEGORY FILTER ----------------
        if category and category.lower() != "all":
            products = products.filter(category__iexact=category)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # CREATE PRODUCT
    def post(self, request):
        serializer = ProductWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class AdminProductDetail(APIView):

    permission_classes = [IsAdminUser]

    # UPDATE PRODUCT
    def patch(self, request, pk):
        product = Product.objects.get(id=pk)

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE PRODUCT
    def delete(self, request, pk):
        product = Product.objects.get(id=pk)
        product.delete()
        return Response({"message": "Product deleted"})