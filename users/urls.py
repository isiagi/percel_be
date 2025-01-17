from rest_framework import routers
from .views import AuthViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('auth', AuthViewSet)


# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = router.urls



