from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'customers', views.CustomerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
