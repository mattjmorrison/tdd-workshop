from sampleapp.views.entity import GetNamedEnts
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('entity', GetNamedEnts, basename='entities')

urlpatterns = router.urls
