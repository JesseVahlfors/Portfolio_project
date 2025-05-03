from rest_framework import viewsets, permissions, serializers
from .models import Product, Order, OrderItem, CustomerProfile
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, CustomerProfileSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise serializers.ValidationError({"error creating order": str(e)})


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        #only return profiles for the authenticated user
        return self.queryset.filter(user=self.request.user)