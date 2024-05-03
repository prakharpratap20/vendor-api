from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer


class VendorListCreateView(ListCreateAPIView):
    """
    API endpoint for listing and creating vendors.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a vendor.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderListCreateView(ListCreateAPIView):
    """
    API endpoint for listing and creating purchase orders.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a purchase order.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class VendorPerformanceView(RetrieveAPIView):
    """
    API endpoint for retrieving a vendor's performance metrics.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Extracting relevant performance metrics and returning them in the response
        return Response({
            'on_time_delivery_rate': serializer.data['on_time_delivery_rate'],
            'quality_rating_avg': serializer.data['quality_rating_avg'],
            'average_response_time': serializer.data['average_response_time'],
            'fulfillment_rate': serializer.data['fulfillment_rate']
        })


class AcknowledgePurchaseOrderView(UpdateAPIView):
    """
    API endpoint for acknowledging a purchase order.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        # Updating the acknowledgment date of the purchase order
        instance.acknowledgment_date = request.data.get('acknowledgment_date')
        instance.save()

        # Calculating average response time for the vendor
        response_times = PurchaseOrder.objects.filter(
            vendor=instance.vendor, acknowledgment_date__isnull=False
        ).values_list('acknowledgment_date', 'issue_date')

        total_seconds = sum(abs((ack_date - issue_date).total_seconds())
                            for ack_date, issue_date in response_times)
        average_response_time = total_seconds / \
            len(response_times) if response_times else 0

        instance.vendor.average_response_time = average_response_time
        instance.vendor.save()

        # Returning acknowledgment date in the response
        return Response({'acknowledgment_date': instance.acknowledgment_date})
