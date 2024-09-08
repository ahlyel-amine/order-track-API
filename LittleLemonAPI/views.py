from rest_framework import generics, status
from .serializers import MenuItemSerializer, CategorySerializer, GroupSerializer, CartSerializer, OrderSerializer
from djoser.views import UserViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import MenuItem, Cart, Order, Category
from .permissions import IsManager, IsDeliveryCrew, IsManagerOrReadOnly, isCostumer
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

class DeliveryCrewGroupView(generics.ListCreateAPIView):
    group_name = 'Delivery'
    queryset = User.objects.filter(groups__name=group_name)
    serializer_class = GroupSerializer

    def post(self, request):
        if request.method == 'POST':
            username = request.data.get('username')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error':'user not found'}, status=status.HTTP_404_NOT_FOUND)
            if user.groups.filter(name=self.group_name).exists():
                return Response({'error':'this user already exist'}, status=status.HTTP_409_CONFLICT)
            try:
                group = Group.objects.get(name=self.group_name)
            except Group.DoesNotExist:
                return Response({'error':'group not found'}, status=status.HTTP_404_NOT_FOUND)
            user.groups.add(group)
            user.save()
            return Response(status=status.HTTP_201_CREATED)

    def get_permissions(self):
        return [IsManager()]

class ManagerGroupView(DeliveryCrewGroupView):
    group_name = 'Manager'
    queryset = User.objects.filter(groups__name=group_name)


@api_view(['DELETE'])
@permission_classes([IsManager])
def DeleteSingleUserGroupView(request, pk, group_name=None):
    try:
        user = User.objects.get(pk=pk)
        if not user.groups.filter(name=group_name).exists():
            raise User.DoesNotExist
    except User.DoesNotExist:
        return Response({'error':'user not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return Response({'error':'group not found'}, status=status.HTTP_404_NOT_FOUND)
    user.groups.remove(group)
    user.save()
    return Response(status=status.HTTP_200_OK)

class CustomUserViewSet(UserViewSet):
    def get_object(self):
        print(self.kwargs)
        if self.request.path.endswith('/me/'):
            return self.request.user
        raise NotFound("User not found")

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]
    # def get_permissions(self):
    #     if self.request.method in ['POST']:
    #         return [IsManager()]
    #     return [IsAuthenticated()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]

    # def get_permissions(self):
    #     if self.request.method in ['GET']:
    #         return [IsAuthenticated()]
    #     return [IsManager()]


class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, isCostumer]

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        if self.request.user.groups.filter(name='Delivery').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            raise ValidationError("Cart is empty")
        order = serializer.save(user=user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
        cart_items.delete()

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        if self.request.user.groups.filter(name='Delivery').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        return Order.objects.filter(user=self.request.user)
    # def perform_create(self, serializer):

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        if self.request.method in ['PATCH']:
            # if self.request.user.groups.filter(name='Delivery').exists():
                # print(self.request.user.groups.all())
            # return [IsDeliveryCrew()]
            pass
        if self.request.method in ['PUT']:
            # if self.request.user.groups.filter(name='Manager').exists():
            return [IsDeliveryCrew()]
        if self.request.method == 'DELETE':
            return [IsManager()]
        return super().get_permissions()

    def perform_update(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Delivery').exists() and 'status' in self.request.data:
            serializer.save(status=self.request.data.get('status'))
        else:
            serializer.save()