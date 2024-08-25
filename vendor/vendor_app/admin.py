from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance

# Register your models here.
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)
