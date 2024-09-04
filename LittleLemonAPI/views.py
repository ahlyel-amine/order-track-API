from rest_framework import generics
from .serializers import MenuItemSerializer, CategorySerializer, GroupSerializer, UserSerializer
from django.contrib.auth.models import Group, User
from .models import MenuItem, Category
from rest_framework.authtoken.views import ObtainAuthToken

# class UserView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
class UserView(ObtainAuthToken, generics.CreateAPIView):
    queryset = User.objects.all()
    # serializer_class = UserSerializer

class GroupView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

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
