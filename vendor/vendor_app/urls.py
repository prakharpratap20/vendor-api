from django.urls import path
from .views import *

urlpatterns = [
    # Endpoint for listing and creating vendors
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    # Endpoint for retrieving, updating, and deleting a vendor
    path('vendors/<str:pk>/', VendorRetrieveUpdateDeleteView.as_view(),
         name='vendor-retrieve-update-delete'),
    # Endpoint for listing and creating purchase orders
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(),
         name='purchase-order-list-create'),
    # Endpoint for retrieving, updating, and deleting a purchase order
    path('purchase_orders/<str:pk>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(),
         name='purchase-order-retrieve-update-delete'),
    # Endpoint for retrieving a vendor's performance metrics
    path('vendors/<str:pk>/performance/',
         VendorPerformanceView.as_view(), name='vendor-performance'),
    # Endpoint for acknowledging a purchase order
    path('purchase_orders/<str:pk>/acknowledge/',
         AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
]
