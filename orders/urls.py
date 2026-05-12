from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/edit/', views.StaffOrderEditView.as_view(), name='staff_order_edit'),
    path('deliveries/', views.DeliveryListView.as_view(), name='delivery_list'),
    path('deliveries/<int:pk>/update/', views.UpdateDeliveryStatusView.as_view(), name='update_delivery_status'),
    path('ratings/', views.RatingListView.as_view(), name='rating_list'),
    # path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    
    # Rating routes
    path('<int:order_id>/rate/', views.RatingCreateView.as_view(), name='rating_create'),
    path('ratings/<int:pk>/edit/', views.RatingUpdateView.as_view(), name='rating_update'),
    path('ratings/<int:pk>/delete/', views.RatingDeleteView.as_view(), name='rating_delete'),
    path('ratings/<int:pk>/staff_delete/', views.StaffRatingDeleteView.as_view(), name='staff_rating_delete'),


    # Municipality Management
    path('municipalities/', views.MunicipalityListView.as_view(), name='municipality_list'),
    path('municipalities/create/', views.MunicipalityCreateView.as_view(), name='municipality_create'),
    path('municipalities/<int:pk>/update/', views.MunicipalityUpdateView.as_view(), name='municipality_update'),
    path('municipalities/<int:pk>/delete/', views.MunicipalityDeleteView.as_view(), name='municipality_delete'),
]