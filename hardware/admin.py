from django.contrib import admin
from .models import PC, MiniPC, Printer, PrinterMaintenance, NetworkCable, InkStock

# Register your models here.
@admin.register(PC)
class PCAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'brand', 'model', 'processor', 'ram', 'purchase_date')
    list_filter = ('brand', 'purchase_date')
    search_fields = ('serial_number', 'brand', 'model', 'processor')
    date_hierarchy = 'purchase_date'

@admin.register(MiniPC)
class MiniPCAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'brand', 'model', 'processor', 'ram', 'purchase_date')
    list_filter = ('brand', 'purchase_date')
    search_fields = ('serial_number', 'brand', 'model', 'processor')
    date_hierarchy = 'purchase_date'

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'brand', 'model', 'printer_type', 'connection_type', 'is_color', 'purchase_date')
    list_filter = ('brand', 'printer_type', 'is_color', 'purchase_date')
    search_fields = ('serial_number', 'brand', 'model')
    date_hierarchy = 'purchase_date'

@admin.register(PrinterMaintenance)
class PrinterMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('printer', 'maintenance_date', 'performed_by', 'next_maintenance_date')
    list_filter = ('maintenance_date', 'next_maintenance_date', 'printer')
    search_fields = ('printer__serial_number', 'printer__brand', 'printer__model', 'performed_by', 'description')
    date_hierarchy = 'maintenance_date'
    autocomplete_fields = ['printer']

@admin.register(InkStock)
class InkStockAdmin(admin.ModelAdmin):
    list_display = ('toner_model', 'ink_type', 'quantity', 'buying_price', 'purchase_date')
    list_filter = ('ink_type', 'purchase_date')
    search_fields = ('toner_model', 'ink_type')
    date_hierarchy = 'purchase_date'

@admin.register(NetworkCable)
class NetworkCableAdmin(admin.ModelAdmin):
    list_display = ('cable_code', 'source_device', 'destination_device', 'port_number', 'cable_type', 'installation_date')
    list_filter = ('cable_type', 'installation_date')
    search_fields = ('cable_code', 'source_device', 'destination_device', 'port_number')
    date_hierarchy = 'installation_date'
