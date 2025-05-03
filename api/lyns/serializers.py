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


    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    
    def validate_price_at_order(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_product_id(self, value):
        if not value.is_active:  # Assuming `Product` has an `is_active` field
            raise serializers.ValidationError("This product is not available for ordering.")
        return value

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

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("An order must contain at least one item.")
        return value

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'address', 'phone_number']
