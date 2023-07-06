from django.contrib import admin
from django.urls import path
from sampleapp.views.entity import GetNamedEnts
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('entity', GetNamedEnts, basename='entities')

urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls
