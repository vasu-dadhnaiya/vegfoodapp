"""
URL configuration for vegfood project.

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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "VegFood Admin"
admin.site.site_title = "Food app Project"
admin.site.index_title = "Welcome to Your Food Project Administration"

handler403 = 'foodapp.views.custom_permission_denied'
handler404 = 'foodapp.views.custom_page_not_found'
handler500 = 'foodapp.views.custom_server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('foodapp.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


