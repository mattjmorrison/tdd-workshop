from django.contrib import admin
from django.urls import path
from sampleapp.urls import urlpatterns as sampleapp_urls

urlpatterns = [
    path('admin/', admin.site.urls),
] + sampleapp_urls
