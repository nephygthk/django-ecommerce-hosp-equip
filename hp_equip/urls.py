from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='frontend')),
    path('store/', include('store.urls', namespace='store')),
    path('account/', include('account.urls', namespace='account')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('orders/', include('orders.urls', namespace='orders')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
