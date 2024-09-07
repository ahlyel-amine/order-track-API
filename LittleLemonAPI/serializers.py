from rest_framework import serializers
# from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.validators import UniqueTogetherValidator
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

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value


class CartSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(read_only=True)
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault(), source='user')
    menuitem = MenuItemSerializer(read_only=True)
    price = serializers.SerializerMethodField(source='get_price', read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price', 'menuitem_id', 'user_id']
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=['user_id', 'menuitem_id'],
                message="This user already has an order for this menu item."
            )
        ]

    def validate_menuitem_id(self, value):
        if not MenuItem.objects.filter(id=value).exists():
            raise serializers.ValidationError("MenuItem does not exist.")
        return value
    def get_price(self, product:Cart):
        print("unit price : " + str(product.unit_price) + " quantity : " + str(product.quantity) + " total : " + str(product.unit_price * product.quantity))
        return product.unit_price * product.quantity

    def create(self, validated_data):
        menuitem = MenuItem.objects.get(id=validated_data['menuitem_id'])
        validated_data['unit_price'] = menuitem.price  # Assign unit price from menuitem
        validated_data['price'] = validated_data['unit_price'] * validated_data['quantity']  # Calculate total price
        return super().create(validated_data)

class OrderSerualizer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItem(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
