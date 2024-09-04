from django.urls import path, include
from . import views

urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='categories list'),
    path('categories/<int:pk>', views.SingleCategoryView.as_view(), name='category'),
    path('menu-items/', views.MenuItemView.as_view(), name='menu-items list'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-item'),
    path('groups/', views.GroupView.as_view(), name='groups list'),
    path('users/', views.UserView.as_view(), name='sing-up'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
