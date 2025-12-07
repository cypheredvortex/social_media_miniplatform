from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('apps.pages.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls')),
    path('content/', include('apps.content.urls')),
    path('like/', include('apps.like.urls')),
    path('profile/', include('apps.profil.urls')),
    path('report/', include('apps.report.urls')),
    path('notification/', include('apps.notification.urls')),
    path('follow/', include('apps.follow.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)