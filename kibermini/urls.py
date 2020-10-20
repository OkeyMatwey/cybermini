from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('nodes/', include('kibermini_nodes.urls')),
    path('', include('kibermini_web.urls')),
]
