from rest_framework import serializers
from .models import Product, Order, OrderItem, CustomerProfile


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price_at_order']

    def create(self, validated_data):
        validated_data['product'] = validated_data.pop('product_id')
        return super().create(validated_data)
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'order_date', 'items', 'total_price']
        read_only_fields = ['order_date', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            item_data['product'] = item_data.pop('product_id')
            OrderItem.objects.create(order=order, **item_data)
        
        return order
    
    def get_total_price(self, obj):
        return obj.total_price()
 