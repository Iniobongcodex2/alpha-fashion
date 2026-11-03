from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# --- ALPHA FASHION ADMIN BRANDING ---
admin.site.site_header = "ALPHA FASHION Management"
admin.site.site_title = "ALPHA FASHION Admin Portal"
admin.site.index_title = "Welcome to the ALPHA FASHION Control Center"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# This is the magic line that tells Django where to find the uploaded images!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)