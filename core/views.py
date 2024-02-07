from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters

# For authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from . import serializers
from . import models

# for permissions
from . import permissions
from rest_framework.permissions import IsAuthenticated


class HelloApiView(APIView):
    """Test API View"""
    
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        apiview = [
            "Uses HTTP methods as function (get, post, put, patch, delete)",
            "Is similar to a traditional Django view",
            "Gives you the most control over your app logic",
            "Is mapped manually to the URL"
        ]
        
        return Response({"message": "Hello!", "apiview": apiview})
    
    def post(self, request):
        """Create a hello message with the given name"""
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Greetings {name}!"

            return Response(data={"message": message}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        """Handling complete update of an object"""
        return Response({"method": "PUT"})
    
    def patch(self, request, pk=None):
        """Handling partial update of an object"""
        return Response({"method": "PATCH"})
    
    def delete(self, request, pk=None):
        """Handling deletion of an object"""
        return Response({"method": "DELETE"})
    

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        viewset = [
            "Uses actions (list, retrieve, create, update, partial_update, destroy)",
            "Automatically maps to URLs using Routers",
            "Provides more functionality with less code"
        ]
        return Response({"message": "Hello", "viewset": viewset})
    
    def retrieve(self, request, pk=None):
        """Get an object by its ID"""

        return Response({"method": "GET"})
    
    def create(self, request):
        """Create an object according to the data passed
            Analogous to POST request
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            
            return Response({"Message": f"Greetings {name}"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """Update an object Analogous to PUT request"""

        return Response({"method": "PUT"})
    
    def partial_update(self, request, pk=None):
        """Partially update an object. Analogous to PATCH request"""

        return Response({"method": "PATCH"})
    
    def destroy(self, request, pk=None):
        """Delete an object. Analgous to DELETE request"""

        return Response({"method": "DELETE"})


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.UpdateOwnProfile]
    filter_backends = [filters.SearchFilter,]
    search_fileds = ["name", "email",]


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.ProfileFeedItemSerializers
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = [permissions.UpdateOwnStatus, IsAuthenticated]

    # Since we want the `user` field to be read_only, we need to override a function
    # called perform_create inside this viewset which is responsible for creating data
    # whenever an HTTP POST request is made.

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user=self.request.user)