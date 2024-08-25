from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from django.db.models import F
from django.utils import timezone


class Vendor(models.Model):
    """
    Model representing a vendor.
    """
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(
        max_length=50, unique=True, primary_key=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    """
    Model representing a purchase order.
    """
    STATUS_CHOICES = [  # Choices for the status of the purchase order
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    delivered_data = models.DateTimeField(
        null=True, blank=True)

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    """
    Model representing historical performance metrics of a vendor.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    """
    Signal receiver to update vendor performance metrics after a purchase order is saved.
    """
    if instance.status == 'completed' and instance.delivered_data is None:
        instance.delivered_data = timezone.now()
        instance.save()

    # Update On-Time Delivery Rate
    completed_orders = PurchaseOrder.objects.filter(
        vendor=instance.vendor, status='completed')
    on_time_deliveries = completed_orders.filter(
        delivery_date__gte=F('delivered_data'))
    on_time_delivery_rate = on_time_deliveries.count() / completed_orders.count()
    instance.vendor.on_time_delivery_rate = on_time_delivery_rate if on_time_delivery_rate else 0

    # Update Quality Rating Average
    completed_orders_with_rating = completed_orders.exclude(
        quality_rating__isnull=True)
    quality_rating_avg = completed_orders_with_rating.aggregate(
        Avg('quality_rating'))['quality_rating__avg'] or 0

    instance.vendor.quality_rating_avg = quality_rating_avg if quality_rating_avg else 0
    instance.vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_response_time(sender, instance, **kwargs):
    """
    Signal receiver to update average response time of a vendor after a purchase order is saved.
    """
    response_times = PurchaseOrder.objects.filter(
        vendor=instance.vendor, acknowledgment_date__isnull=False).values_list('acknowledgment_date', 'issue_date')
    average_response_time = sum((ack_date - issue_date).total_seconds()
                                for ack_date, issue_date in response_times)
    if average_response_time < 0:
        average_response_time = 0
    if response_times:
        average_response_time = average_response_time / len(response_times)
    else:
        average_response_time = 0

    instance.vendor.average_response_time = average_response_time
    instance.vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, **kwargs):
    """
    Signal receiver to update fulfillment rate of a vendor after a purchase order is saved.
    """
    fulfilled_orders = PurchaseOrder.objects.filter(
        vendor=instance.vendor, status='completed')
    fulfillment_rate = fulfilled_orders.count(
    ) / PurchaseOrder.objects.filter(vendor=instance.vendor).count()

    instance.vendor.fulfillment_rate = fulfillment_rate
    instance.vendor.save()
