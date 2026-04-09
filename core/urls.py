from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import HomeView

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def custom_403(request, exception=None):
    return render(request, '403.html', status=403)

handler404 = custom_404
handler403 = custom_403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('roles/', include(('roles.urls', 'roles'))),
    path('products/', include(('products.urls', 'products'))),
    path('orders/', include(('orders.urls', 'orders'))),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns.append(re_path(r'^.*$', custom_404))
