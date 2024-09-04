from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import Group, User


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.P
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerualizer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItem(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
