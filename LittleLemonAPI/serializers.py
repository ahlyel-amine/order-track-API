from rest_framework import serializers
# from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError, PermissionDenied
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
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    menuitem = MenuItemSerializer(read_only=True)
    price = serializers.SerializerMethodField(source='get_price', read_only=True)
    unit_price = serializers.DecimalField(source='menuitem.price', read_only=True, max_digits=6, decimal_places=2)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price', 'menuitem_id']
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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    delivery_crew = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(groups__name='Delivery'), required=False)
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']

    def get_total(self, cart:Cart):
        total = 0
        for item in cart:
            total += item.price
        return total

    def create_order_items(self, order:Order, cart:Cart):
        for item in cart:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )

    def create(self, validated_data):
        user = validated_data['user']
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            raise ValidationError("Cart is empty")
        validated_data['total'] = self.get_total(cart_items)
        order = super().create(validated_data)
        self.create_order_items(order, cart_items)
        cart_items.delete()
        return order

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        if user.groups.filter(name='Manager').exists():
            if 'delivery_crew' in validated_data:
                instance.delivery_crew = validated_data['delivery_crew']
            if 'status' in validated_data:
                instance.status = validated_data['status']
        elif user.groups.filter(name='Delivery').exists():
            if 'status' in validated_data:
                instance.status = validated_data['status']
            else:
                raise PermissionDenied("Delivery can only update the status.")
        else:
            raise PermissionDenied("Only managers and Delivery can update orders.")
        instance.save()
        return instance
