from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('django-rq/', include('django_rq.urls')),
    path('admin/', admin.site.urls),
    path('', include('kibermini_web.urls')),
]
