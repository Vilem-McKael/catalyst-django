from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user

# Create your views here.

"""
        USER AUTHENTICATION VIEWS
"""

# Accessed at /auth/signup/
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    # Called when we call a POST request on our corresponding URI
    # Attempts to create a new user in our system
    def post(self, request:Request):

        # grabs the payload of the request
        data = request.data

        # renders a deserialized version of our data
        serializer = self.serializer_class(data=data)

        # checks if our incoming User data passes all of the tests in our Serializer
        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User created successfully",
                "data": serializer.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Accessed at /auth/login/
class LoginView(APIView):

    permission_classes = []

    # Called when we make a POST request to our login URL
    # Attempts to sign in a user based on provided credentials
    def post(self, request:Request):
        
        # retrieve the email and password fields of the request
        email = request.data.get("email")
        password = request.data.get("password")

        # authenticate finds a User object with the corresponding email,
        # and checks the entered password against the stored hashed password.
        # Returns None if there is no such User, i.e. the credentials are incorrect
        user = authenticate(email=email, password=password)
        
        # If the entered credentials match those of an existing user, log them in
        if user is not None:

            tokens=create_jwt_pair_for_user(user)
            userData = User.objects.filter(username=user)[0]

            response = {
                "message": "Login Successful",
                "tokens": tokens
            }

            return Response(data=response, status=status.HTTP_200_OK)
        
        else:
            return Response(data={"message": "Invalid email or password"})
        
    
    def get(self, request:Request):

        # user is the information of the user who made the request
        # auth gives us access to the token of the user

        content = {
            "user": str(request.user),
            "auth": str(request.auth),
        }

        return Response(data=content, status=status.HTTP_200_OK)
    

"""
        CUSTOM TOKEN VIEWS
"""
#https://stackoverflow.com/questions/54544978/customizing-jwt-response-from-django-rest-framework-simplejwt

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user'] = {
            "user_id": user.id,
            "username": user.username
            # add communities here
        }
        # token['communities'] = user.communities.communities.values_list('name', flat=True)

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer