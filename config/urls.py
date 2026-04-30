"""
XinRange URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('vulns/', include('app.vulns.urls')),
    path('api/', include('app.core.urls')),
]

# 开发模式下提供 /uploads/ 访问
if settings.DEBUG:
    urlpatterns += static('/uploads/', document_root=settings.MEDIA_ROOT)
