"""
URL configuration for auto_market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

from .swagger import schema_view

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('frontend.urls', namespace='frontend')),
    path('admin/', admin.site.urls),
    path('api/', include(
        [
            path('', include('authentication.urls', namespace='auth')),
            path('', include('car_listing.urls', namespace='car_listing')),
            path('myprofile/', include('userprofile.urls', namespace='profiles')),
            path('messaging/', include('messaging.urls', namespace='messaging')),
        ]
    )),
    path(
        'swagger/', 
        schema_view.with_ui('swagger', cache_timeout=0), 
        name='schema-swagger-ui'
    ),
    path(
        'redoc/', 
        schema_view.with_ui('redoc', cache_timeout=0), 
        name='schema-redoc'
    ),
    
] + debug_toolbar_urls()

handler404 = TemplateView.as_view(template_name='extras/404.html')

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

