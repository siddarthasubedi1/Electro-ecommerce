
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include(('store.urls', 'store'), namespace='store')),
    path('shop', include(('shop.urls', 'shop'), namespace='shop')),
]