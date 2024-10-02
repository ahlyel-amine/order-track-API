from django.urls import path
from djoser.views import TokenCreateView, UserViewSet
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [

    path('token/login/', TokenCreateView.as_view(), name='token-create'),

    path('users/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('users/users/me/', views.CustomUserViewSet.as_view({'get': 'retrieve'}), name='user-me'),

    path('categories/', views.CategoryView.as_view(), name='categories list'),
    path('categories/<int:pk>', views.SingleCategoryView.as_view(), name='category'),

    path('menu-items/', views.MenuItemView.as_view(), name='menu-items list'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-item'),

    path('groups/manager/users/', views.ManagerGroupView.as_view(), name='manager group list'),
    path('groups/manager/users/<int:pk>', views.DeleteSingleUserGroupView, {'group_name': 'Manager'}, name='manager group list'),

    path('groups/delivery-crew/users/', views.DeliveryCrewGroupView.as_view(), name='Delivery group list'),
    path('groups/delivery-crew/users/<int:pk>', views.DeleteSingleUserGroupView, {'group_name': 'Delivery'}, name='Delivery group list'),

    path('cart/menu-items/', views.CartView.as_view(), name='cart'),

    path('orders/', views.OrderView.as_view(), name='orders list'),
    path('orders/<int:pk>', views.SingleOrderView.as_view(), name='order view'),
]
