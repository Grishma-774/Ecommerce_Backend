from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializer import OrderSerializer,OrderDetailsSerializer,OneOrderDetailsSerializer
from .models import Order


class OrderViews(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = OrderSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Successfully placed the order",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class GetOrderHistory(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        order_detail = Order.objects.filter(user=request.user).order_by("-created_at")

        serializer = OrderDetailsSerializer(order_detail,many=True)

        return Response( serializer.data )


class  GetOrderDetails(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        
        specific_order_detail = Order.objects.get(id=pk,user=request.user)

        serializer =  OneOrderDetailsSerializer(specific_order_detail)

        return Response(serializer.data)


# -------------------------------------------------------------------------------------------------------------------------



from rest_framework.permissions import IsAdminUser

from .serializer import AdminUpdateSerializer,AdminOrderDetailsSerializer



class AdminAllOrders(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        orders = Order.objects.all().order_by("-created_at")

        serializer = OrderDetailsSerializer(orders, many=True)

        return Response(serializer.data)


class AdminGetOrderDetails(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request,pk):

        orders = Order.objects.get(id=pk)

        serializer = AdminOrderDetailsSerializer(orders)

        return Response(serializer.data)


class AdminUpdateOrders(APIView):

    permission_classes = [IsAdminUser]

    def patch(self,request,pk):

        order = Order.objects.get(id=pk)

        serializer = AdminUpdateSerializer(order, data=request.data,partial=True)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)





        





