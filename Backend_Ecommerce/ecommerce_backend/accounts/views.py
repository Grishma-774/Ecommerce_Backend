from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import AllowAny,IsAuthenticated

from .serializer import RegisterSerializer

from rest_framework import status

from django.contrib.auth.models import User



class Register_view(APIView):
    
    permission_classes = [AllowAny]


    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=201)

        return Response(serializer.errors, status=400)




from .serializer import UserSerializer


class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)
