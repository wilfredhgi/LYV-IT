from django import forms
from .models import PC, MiniPC, Printer, PrinterMaintenance, InkStock, NetworkCable
from django.utils.translation import gettext_lazy as _
from django.db.models import Max

class PCForm(forms.ModelForm):
    class Meta:
        model = PC
        fields = ['code', 'serial_number', 'ip', 'brand', 'model', 'purchase_date', 
                 'processor', 'ram', 'storage', 'operating_system', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate default code if this is a new PC
        if not self.instance.pk and not self.initial.get('code'):
            # Find the highest existing code number
            prefix = 'lyv-pc-'
            highest_pc = PC.objects.filter(code__startswith=prefix).order_by('-code').first()
            highest_minipc = MiniPC.objects.filter(code__startswith=prefix).order_by('-code').first()

            highest_num = 0
            if highest_pc:
                try:
                    highest_num = max(highest_num, int(highest_pc.code[len(prefix):]))
                except ValueError:
                    pass

            if highest_minipc:
                try:
                    highest_num = max(highest_num, int(highest_minipc.code[len(prefix):]))
                except ValueError:
                    pass

            # Generate new code with incremented number
            new_num = highest_num + 1
            self.initial['code'] = f"{prefix}{new_num:02d}"

class MiniPCForm(forms.ModelForm):
    class Meta:
        model = MiniPC
        fields = ['code', 'serial_number', 'ip', 'brand', 'model', 'purchase_date', 
                 'processor', 'ram', 'storage', 'operating_system', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate default code if this is a new MiniPC
        if not self.instance.pk and not self.initial.get('code'):
            # Find the highest existing code number
            prefix = 'lyv-pc-'
            highest_pc = PC.objects.filter(code__startswith=prefix).order_by('-code').first()
            highest_minipc = MiniPC.objects.filter(code__startswith=prefix).order_by('-code').first()

            highest_num = 0
            if highest_pc:
                try:
                    highest_num = max(highest_num, int(highest_pc.code[len(prefix):]))
                except ValueError:
                    pass

            if highest_minipc:
                try:
                    highest_num = max(highest_num, int(highest_minipc.code[len(prefix):]))
                except ValueError:
                    pass

            # Generate new code with incremented number
            new_num = highest_num + 1
            self.initial['code'] = f"{prefix}{new_num:02d}"

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['code', 'serial_number', 'ip', 'brand', 'model', 'purchase_date', 
                 'printer_type', 'connection_type', 'is_color', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate default code if this is a new Printer
        if not self.instance.pk and not self.initial.get('code'):
            # Find the highest existing code number
            prefix = 'lyv-im-'
            highest_printer = Printer.objects.filter(code__startswith=prefix).order_by('-code').first()

            highest_num = 0
            if highest_printer:
                try:
                    highest_num = int(highest_printer.code[len(prefix):])
                except ValueError:
                    pass

            # Generate new code with incremented number
            new_num = highest_num + 1
            self.initial['code'] = f"{prefix}{new_num:02d}"

class PrinterMaintenanceForm(forms.ModelForm):
    class Meta:
        model = PrinterMaintenance
        fields = ['printer', 'maintenance_type', 'toner', 'maintenance_date', 'description', 'performed_by', 'next_maintenance_date', 'cost']
        widgets = {
            'maintenance_type': forms.Select(),
            'toner': forms.Select(attrs={'class': 'form-select'}),
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'cost': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
        }

class InkStockForm(forms.ModelForm):
    class Meta:
        model = InkStock
        fields = ['toner_model', 'ink_type', 'quantity', 'buying_price', 'purchase_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'buying_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

class NetworkCableForm(forms.ModelForm):
    class Meta:
        model = NetworkCable
        fields = ['cable_code', 'source_device', 'destination_device', 'port_number', 
                 'cable_type', 'cable_length', 'installation_date', 'notes']
        widgets = {
            'installation_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate default code if this is a new NetworkCable
        if not self.instance.pk and not self.initial.get('cable_code'):
            # Find the highest existing code number
            prefix = 'lyv-net-'
            highest_cable = NetworkCable.objects.filter(cable_code__startswith=prefix).order_by('-cable_code').first()

            highest_num = 0
            if highest_cable:
                try:
                    highest_num = int(highest_cable.cable_code[len(prefix):])
                except ValueError:
                    pass

            # Generate new code with incremented number
            new_num = highest_num + 1
            self.initial['cable_code'] = f"{prefix}{new_num:02d}"
