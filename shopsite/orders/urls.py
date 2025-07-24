from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderCreateView, UserOrderListView, UpdateOrderStatusView
from .views import AddressViewSet  # <-- import your Address viewset

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('place/', OrderCreateView.as_view(), name='order-place'),
    path('my-orders/', UserOrderListView.as_view(), name='my-orders'),
    path('orders/<int:pk>/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('', include(router.urls)),
]
