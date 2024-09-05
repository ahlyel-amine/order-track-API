from rest_framework import generics
from .serializers import MenuItemSerializer, CategorySerializer, GroupSerializer
from djoser.views import UserViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Category
from .permissions import IsManager, IsCustomer, IsDeliveryCrew
# from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User

class ManagerGroupView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = GroupSerializer

class CustomUserViewSet(UserViewSet):
    def get_object(self):
        print(self.kwargs)
        if self.request.path.endswith('/me/'):
            return self.request.user
        raise NotFound("User not found")

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsManager()]
        return [IsAuthenticated()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        return [IsManager()]
