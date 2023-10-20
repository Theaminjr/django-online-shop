from rest_framework import serializers
from order.models import Order,OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','count','product_option']

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['address', 'orderitems','date','status']

    def create(self, validated_data):
        order_items_data = validated_data['orderitems']
        order = Order.objects.create(user=validated_data['user'],address = validated_data['address'])
        for order_item_data in order_items_data:
            orderitem = OrderItem(order=order, **order_item_data)
            orderitem.save()
        return order


    


