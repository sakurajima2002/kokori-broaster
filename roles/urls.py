from django.urls import path
from . import views

app_name = 'roles'

urlpatterns = [
    path('', views.GroupListView.as_view(), name='group_list'),
    path('create/', views.GroupCreateView.as_view(), name='group_create'),
    path('<int:pk>/edit/', views.GroupUpdateView.as_view(), name='group_edit'),
    path('<int:pk>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),
    
    path('users/<int:pk>/roles/', views.UserRoleUpdateView.as_view(), name='user_role_edit'),
]