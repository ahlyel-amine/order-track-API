from rest_framework import generics
from .serializers import MenuItemSerializer, CategorySerializer, GroupSerializer
from django.contrib.auth.models import Group, User
from rest_framework import status
from django.http import Http404  # Import Http404 to handle the exception
from djoser.views import UserViewSet
from rest_framework.exceptions import NotFound

from .models import MenuItem, Category
# from rest_framework.authtoken.views import ObtainAuthToken

class CustomUserViewSet(UserViewSet):
    def get_object(self):
        print(self.kwargs)
        if self.request.path.endswith('/me/'):
            return self.request.user
        raise NotFound("User not found")

class GroupView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SingleGroupView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'name'  # Use the name field for lookup
    lookup_url_kwarg = 'name'  # URL parameter is name

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
