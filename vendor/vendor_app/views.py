from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer


class VendorListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating vendors.
    """
    auth_class = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         self.permission_classes = [IsAdminUser]
    #     else:
    #         self.permission_classes = [IsAuthenticated]
    #     return super().get_permissions()


class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a vendor.
    """
    auth_class = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_object(self):
        """
        Retrieve a vendor instance based on the provided primary key.
        """
        # Get the vendor object based on the provided primary key
        vendor_pk = self.kwargs.get('pk')
        try:
            vendor = Vendor.objects.get(pk=vendor_pk)
            return vendor
        except Vendor.DoesNotExist:
            return Response(
                {'error': 'Vendor does not exist'}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        """
        Update a vendor instance based on the provided primary key.
        """
        # Get the existing vendor object
        vendor = self.get_object()
        # Serialize the request data with the existing vendor instance
        serializer = self.serializer_class(
            vendor, data=request.data, partial=True)
        if serializer.is_valid():
            # Save the updated vendor instance
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderListCreateView(ListCreateAPIView):
    """
    API endpoint for listing and creating purchase orders.
    """
    auth_class = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a purchase order.
    """
    auth_class = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class VendorPerformanceView(RetrieveAPIView):
    """
    API endpoint for retrieving a vendor's performance metrics.
    """
    auth_class = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a vendor instance and return its performance metrics.
        """
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
    auth_class = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Update the acknowledgment date of a purchase order and calculate the average response time for the vendor.
        """
        instance = self.get_object()
        # Updating the acknowledgment date of the purchase order
        instance.acknowledgment_date = request.data.get('acknowledgment_date')
        instance.save()

        # Calculating average response time for the vendor
        response_times = PurchaseOrder.objects.filter(
            vendor=instance.vendor, acknowledgment_date__isnull=False
        ).values_list('acknowledgment_date', 'issue_date')

        # Calculating the average response time
        total_seconds = sum(abs((ack_date - issue_date).total_seconds())
                            for ack_date, issue_date in response_times)
        average_response_time = total_seconds / \
            len(response_times) if response_times else 0

        # Updating the average response time
        instance.vendor.average_response_time = average_response_time
        instance.vendor.save()  # Saving the updated vendor instance

        # Returning acknowledgment date in the response
        return Response({'acknowledgment_date': instance.acknowledgment_date})


class UserCreateView(CreateAPIView):
    """
    API endpoint for creating a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
