from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('deliveries/', views.DeliveryListView.as_view(), name='delivery_list'),
    path('deliveries/<int:pk>/update/', views.UpdateDeliveryStatusView.as_view(), name='update_delivery_status'),
    path('ratings/', views.RatingListView.as_view(), name='rating_list'),
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
]