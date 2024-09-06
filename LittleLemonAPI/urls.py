from django.urls import path, include
from djoser.views import TokenCreateView, UserViewSet
from . import views

urlpatterns = [

    path('token/login/', TokenCreateView.as_view(), name='token-create'),
    path('users/', include([
        path('', UserViewSet.as_view({'post': 'create'}), name='token-create'),
        path('users/me/', views.CustomUserViewSet.as_view({'get': 'retrieve'}), name='user-me'),
    ])),

    path('menu-items/', views.MenuItemView.as_view(), name='menu-items list'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-item'),

    path('groups/manager/users/', views.ManagerGroupView.as_view(), name='manager group list'),
    path('groups/manager/users/<int:pk>', views.DeleteSingleUserGroupView, {'group_name': 'Manager'}, name='manager group list'),

    path('groups/delivery-crew/users/', views.DeliveryCrewGroupView.as_view(), name='manager group list'),
    path('groups/delivery-crew/users/<int:pk>', views.DeleteSingleUserGroupView, {'group_name': 'Delivery crew'}, name='manager group list'),

    path('cart/menu-items/', views.CartView.as_view(), name='cart list'),
]
