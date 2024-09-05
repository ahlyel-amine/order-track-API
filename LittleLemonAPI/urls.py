from django.urls import path, include
from djoser.views import TokenCreateView, UserViewSet
from . import views

urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='categories list'),
    path('categories/<int:pk>', views.SingleCategoryView.as_view(), name='category'),
    path('menu-items/', views.MenuItemView.as_view(), name='menu-items list'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-item'),
    path('groups/', views.GroupView.as_view(), name='groups list'),
    path('groups/<str:group_name>', views.SingleGroupView.as_view(), name='group-detail-by-name'),
    path('token/login/', TokenCreateView.as_view(), name='token-create'),
    path('users/', include([
        path('', UserViewSet.as_view({'post': 'create'}), name='token-create'),
        path('users/me/', views.CustomUserViewSet.as_view({'get': 'retrieve'}), name='user-me'),
    ])),
]
