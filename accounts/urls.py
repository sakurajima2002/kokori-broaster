from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/toggle-staff/', views.UserStaffStatusToggleView.as_view(), name='user_staff_toggle'),
    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address_detail'),

    # Public user views
    path('my-account/', views.MyAccountView.as_view(), name='my_account'),
    path('my-account/address/<int:pk>/delete/', views.DeleteAddressView.as_view(), name='delete_address'),
    path('my-orders/', views.MyOrdersView.as_view(), name='my_orders'),
]