from rest_framework import generics, status
from .serializers import MenuItemSerializer, CategorySerializer, GroupSerializer, CartSerializer
from djoser.views import UserViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Cart
from .permissions import IsManager, IsCustomer, IsDeliveryCrew
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication

class DeliveryCrewGroupView(generics.ListCreateAPIView):
    """
    A view for managing the delivery crew group.

    This view allows listing and adding users in the delivery crew group.
    """

    group_name = 'Delivery crew'
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
    """
    A view that returns a list of users belonging to the 'Manager' group.

    Inherits from the DeliveryCrewGroupView class.

    Attributes:
        group_name (str): The name of the group to filter users by.
        queryset (QuerySet): The queryset of users filtered by the group name.

    """
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


class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    # def get_permissions(self):
    #     return [IsAuthenticated()]
