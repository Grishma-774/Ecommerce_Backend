from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializer import CartSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import CartGetSerializer
from .models import Cart,CartItem
from .serializer import UpdateCartItemSerializer



# Create your views here.

class CartAddView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        
        serializer = CartSerializer( context={"request": request} , data=request.data)

        if(serializer.is_valid()):

            serializer.save()
            return Response({"data":serializer.data},status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)




class CartGetView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        serializer = CartGetSerializer(cart)

        return Response(
            {
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class UpdateQuantityView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        cart_item = CartItem.objects.get(
            id=pk,
            cart__user=request.user
        )

        serializer = UpdateCartItemSerializer(
            cart_item,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Quantity updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class DeleteCartItem(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        cart_item = CartItem.objects.get(
            id=pk,
            cart__user=request.user
        )

        cart_item.delete()

        return Response(
            {
                "message": "Item removed from cart"
            },
            status=status.HTTP_200_OK
        )


class DeleteAllCartItem(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self,request):

        cart = Cart.objects.get(user=request.user)

        cart.items.all().delete()

        return Response(
            {
                "message": "cart emptied"
            },
            status=status.HTTP_200_OK
        )




