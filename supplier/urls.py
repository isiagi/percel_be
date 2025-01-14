from rest_framework import routers
from .views import SupplierViewSet

router = routers.DefaultRouter()
router.register('suppliers', SupplierViewSet)

urlpatterns = router.urls