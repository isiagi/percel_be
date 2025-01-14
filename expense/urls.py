from rest_framework import routers
from .views import ExpenseViewSet

router = routers.DefaultRouter()
router.register('expenses', ExpenseViewSet)

urlpatterns = router.urls