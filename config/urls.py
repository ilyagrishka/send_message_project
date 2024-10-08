from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from django.template.backends import django
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("", include("service.urls", namespace="service")),
                  path("users/", include("users.urls", namespace="users")),
                  path("blogs/", include("blog.urls", namespace="blog"))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
