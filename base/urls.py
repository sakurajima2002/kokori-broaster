from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('configuration/', views.SiteParameterListView.as_view(), name='parameter_list'),
    path('configuration/<int:pk>/edit/', views.SiteParameterUpdateView.as_view(), name='parameter_edit'),
]
