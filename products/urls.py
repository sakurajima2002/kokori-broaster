from django.urls import path
from . import views

urlpatterns = [
    # Products
    path('catalog/', views.ProductCatalogView.as_view(), name='product_catalog'),
    path('', views.ProductListView.as_view(), name='product_list'),

    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
]