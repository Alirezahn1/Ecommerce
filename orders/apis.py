from rest_framework import generics, permissions, authentication
from .serializers import OrderItemSerializer
from .models import Orderitem


class OrderItemApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    queryset = Orderitem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Orderitem.objects.filter(order__customer__user=self.request.user)


class OrderItemDetailApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    queryset = Orderitem

    def get_queryset(self):
        return super().get_queryset()