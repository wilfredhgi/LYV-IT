from django.contrib import admin
from .models import PC, MiniPC, Printer, PrinterMaintenance

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
