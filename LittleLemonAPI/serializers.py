from rest_framework import serializers
# from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework.permissions import IsAuthenticated

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
    #         return [IsAuthenticated()]
    #     else :
    #         return []

class CartSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(default=serializers.CurrentUserDefault())
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), )

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerualizer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItem(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
