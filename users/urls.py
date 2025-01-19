from rest_framework import routers
from .views import AuthViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')  # Added basename parameter

urlpatterns = [
    path('', include(router.urls)),
]