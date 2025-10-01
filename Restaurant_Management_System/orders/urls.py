from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderHistoryView

router = DefaultRouter()
router.register(r"", OrderViewSet, basename="orders")

urlpatterns = [
    path("history/", OrderHistoryView.as_view(), name="order-history"),
]

urlpatterns += router.urls
