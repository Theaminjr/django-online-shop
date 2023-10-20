from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order,OrderItem
from core.api.auth import login_required
from order.api.serializers import OrderSerializer,OrderItemSerializer



class OrderView(APIView):

    @login_required
    def get(self,request):
        orders = Order.objects.filter(user=request.jwt)
        serializer = OrderSerializer(orders,many=True)
        return Response(serializer.data,status=200)

        
    @login_required
    def post(self,request):
        
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.jwt)
            return Response('order submitted',status=201)
        return Response(status=400)

        



