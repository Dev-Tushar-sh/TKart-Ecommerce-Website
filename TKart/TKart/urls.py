from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.root),
    path('admin/', admin.site.urls),
    path('shop/',include('shop.urls')),    #it checks someone say shop/ it redirect it to the shop
    path('blog/',include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
