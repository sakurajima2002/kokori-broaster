from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('deliveries/', views.DeliveryListView.as_view(), name='delivery_list'),
    path('ratings/', views.RatingListView.as_view(), name='rating_list'),
]