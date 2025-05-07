from django.db.models import Count, Sum, F, OuterRef, Subquery
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from .models import PC, MiniPC, Printer, PrinterMaintenance, InkStock
from .forms import PCForm, MiniPCForm, PrinterForm, PrinterMaintenanceForm, InkStockForm

# Create your views here.
@login_required
def home(request):
    """Home view that serves as a dashboard"""
    context = {
        'pc_count': PC.objects.count(),
        'minipc_count': MiniPC.objects.count(),
        'printer_count': Printer.objects.count(),
        'maintenance_count': PrinterMaintenance.objects.count(),
        'title': _('Panel de Control'),
    }
    return render(request, 'hardware/home.html', context)

# PC Views
class PCListView(LoginRequiredMixin, ListView):
    model = PC
    template_name = 'hardware/pc_list.html'
    context_object_name = 'pcs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Lista de PCs')
        return context

class PCDetailView(LoginRequiredMixin, DetailView):
    model = PC
    template_name = 'hardware/pc_detail.html'
    context_object_name = 'pc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Detalles del PC')
        return context

class PCCreateView(LoginRequiredMixin, CreateView):
    model = PC
    template_name = 'hardware/pc_form.html'
    form_class = PCForm
    success_url = reverse_lazy('pc-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Añadir PC')
        return context

class PCUpdateView(LoginRequiredMixin, UpdateView):
    model = PC
    template_name = 'hardware/pc_form.html'
    form_class = PCForm

    def get_success_url(self):
        return reverse_lazy('pc-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Actualizar PC')
        return context

class PCDeleteView(LoginRequiredMixin, DeleteView):
    model = PC
    template_name = 'hardware/pc_confirm_delete.html'
    success_url = reverse_lazy('pc-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Eliminar PC')
        return context

# MiniPC Views
class MiniPCListView(LoginRequiredMixin, ListView):
    model = MiniPC
    template_name = 'hardware/minipc_list.html'
    context_object_name = 'minipcs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Lista de Mini PCs')
        return context

class MiniPCDetailView(LoginRequiredMixin, DetailView):
    model = MiniPC
    template_name = 'hardware/minipc_detail.html'
    context_object_name = 'minipc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Detalles del Mini PC')
        return context

class MiniPCCreateView(LoginRequiredMixin, CreateView):
    model = MiniPC
    template_name = 'hardware/minipc_form.html'
    form_class = MiniPCForm
    success_url = reverse_lazy('minipc-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Añadir Mini PC')
        return context

class MiniPCUpdateView(LoginRequiredMixin, UpdateView):
    model = MiniPC
    template_name = 'hardware/minipc_form.html'
    form_class = MiniPCForm

    def get_success_url(self):
        return reverse_lazy('minipc-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Actualizar Mini PC')
        return context

class MiniPCDeleteView(LoginRequiredMixin, DeleteView):
    model = MiniPC
    template_name = 'hardware/minipc_confirm_delete.html'
    success_url = reverse_lazy('minipc-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Eliminar Mini PC')
        return context

# PrinterMaintenance Views
class MaintenanceListView(LoginRequiredMixin, ListView):
    model = PrinterMaintenance
    template_name = 'hardware/maintenance_list.html'
    context_object_name = 'maintenance_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Registros de Mantenimiento')

        # Calculate total maintenance costs
        total_costs = PrinterMaintenance.objects.aggregate(total=Sum('cost'))
        context['total_maintenance_costs'] = total_costs['total'] or 0

        return context

class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    model = PrinterMaintenance
    template_name = 'hardware/maintenance_detail.html'
    context_object_name = 'maintenance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Detalles del Mantenimiento')
        return context

class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    model = PrinterMaintenance
    template_name = 'hardware/maintenance_form.html'
    form_class = PrinterMaintenanceForm
    success_url = reverse_lazy('maintenance-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Añadir Registro de Mantenimiento')
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Pre-select printer if provided in URL
        printer_id = self.request.GET.get('printer')
        if printer_id:
            try:
                form.initial['printer'] = Printer.objects.get(pk=printer_id)
            except Printer.DoesNotExist:
                pass
        return form

    def form_valid(self, form):
        # Check if this is a toner change maintenance and set cost to toner price
        if form.instance.maintenance_type == 'cambio_toner' and form.instance.toner:
            # Set the cost to the toner's buying price
            form.instance.cost = form.instance.toner.buying_price

        response = super().form_valid(form)

        # Check if this is a toner change maintenance
        if form.instance.maintenance_type == 'cambio_toner' and form.instance.toner:
            # Get the toner and decrease its quantity
            toner = form.instance.toner
            if toner.quantity > 0:
                toner.quantity -= 1
                toner.save()

        return response

class MaintenanceUpdateView(LoginRequiredMixin, UpdateView):
    model = PrinterMaintenance
    template_name = 'hardware/maintenance_form.html'
    form_class = PrinterMaintenanceForm

    def get_success_url(self):
        return reverse_lazy('maintenance-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Actualizar Registro de Mantenimiento')
        return context

    def form_valid(self, form):
        # Check if maintenance type was changed to 'cambio_toner'
        was_toner_change = False
        old_toner = None
        if self.object.maintenance_type == 'cambio_toner':
            was_toner_change = True
            old_toner = self.object.toner

        # Check if this is a toner change maintenance and set cost to toner price
        if form.instance.maintenance_type == 'cambio_toner' and form.instance.toner:
            # Set the cost to the toner's buying price
            form.instance.cost = form.instance.toner.buying_price

        response = super().form_valid(form)

        # If this is a new toner change maintenance or the toner was changed
        if form.instance.maintenance_type == 'cambio_toner' and form.instance.toner:
            # If this is a new toner change or the toner was changed
            if not was_toner_change or (old_toner and old_toner.pk != form.instance.toner.pk):
                # Get the toner and decrease its quantity
                toner = form.instance.toner
                if toner.quantity > 0:
                    toner.quantity -= 1
                    toner.save()

        return response

class MaintenanceDeleteView(LoginRequiredMixin, DeleteView):
    model = PrinterMaintenance
    template_name = 'hardware/maintenance_confirm_delete.html'
    success_url = reverse_lazy('maintenance-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Eliminar Registro de Mantenimiento')
        return context


class PrinterListView(LoginRequiredMixin, ListView):
    model = Printer
    template_name = 'hardware/printer_list.html'
    context_object_name = 'printers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Lista de Impresoras')

        # Calculate total maintenance costs
        total_costs = PrinterMaintenance.objects.aggregate(total=Sum('cost'))
        context['total_maintenance_costs'] = total_costs['total'] or 0

        # Find the most costly printer
        printers_with_costs = Printer.objects.annotate(
            total_cost=Sum('maintenance_records__cost')
        ).filter(total_cost__isnull=False).order_by('-total_cost')

        if printers_with_costs.exists():
            most_costly_printer = printers_with_costs.first()
            context['most_costly_printer'] = most_costly_printer
            context['most_costly_printer_cost'] = most_costly_printer.total_cost

        return context

class PrinterDetailView(LoginRequiredMixin, DetailView):
    model = Printer
    template_name = 'hardware/printer_detail.html'
    context_object_name = 'printer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintenance_records'] = self.object.maintenance_records.all()
        context['title'] = _('Detalles de la Impresora')

        total_costs = PrinterMaintenance.objects.aggregate(total=Sum('cost'))
        context['total_maintenance_costs'] = total_costs['total'] or 0

        return context

class PrinterCreateView(LoginRequiredMixin, CreateView):
    model = Printer
    template_name = 'hardware/printer_form.html'
    form_class = PrinterForm
    success_url = reverse_lazy('printer-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Añadir Impresora')
        return context

class PrinterUpdateView(LoginRequiredMixin, UpdateView):
    model = Printer
    template_name = 'hardware/printer_form.html'
    form_class = PrinterForm

    def get_success_url(self):
        return reverse_lazy('printer-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Actualizar Impresora')
        return context

class PrinterDeleteView(LoginRequiredMixin, DeleteView):
    model = Printer
    template_name = 'hardware/printer_confirm_delete.html'
    success_url = reverse_lazy('printer-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Eliminar Impresora')
        return context

# InkStock Views
class InkStockListView(LoginRequiredMixin, ListView):
    model = InkStock
    template_name = 'hardware/inkstock_list.html'
    context_object_name = 'inkstocks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Lista de Stock de Tinta')
        return context

class InkStockDetailView(LoginRequiredMixin, DetailView):
    model = InkStock
    template_name = 'hardware/inkstock_detail.html'
    context_object_name = 'inkstock'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Detalles del Stock de Tinta')
        return context

class InkStockCreateView(LoginRequiredMixin, CreateView):
    model = InkStock
    template_name = 'hardware/inkstock_form.html'
    form_class = InkStockForm
    success_url = reverse_lazy('inkstock-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Añadir Stock de Tinta')
        return context

class InkStockUpdateView(LoginRequiredMixin, UpdateView):
    model = InkStock
    template_name = 'hardware/inkstock_form.html'
    form_class = InkStockForm

    def get_success_url(self):
        return reverse_lazy('inkstock-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Actualizar Stock de Tinta')
        return context

class InkStockDeleteView(LoginRequiredMixin, DeleteView):
    model = InkStock
    template_name = 'hardware/inkstock_confirm_delete.html'
    success_url = reverse_lazy('inkstock-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Eliminar Stock de Tinta')
        return context

# API Views
@login_required
def get_printer_toners(request, printer_id):
    """API endpoint to get available toners"""
    # Since we no longer have a printer field in InkStock, we'll just return all toners with quantity > 0
    toners = InkStock.objects.filter(quantity__gt=0)
    toner_data = [
        {
            'id': toner.id,
            'toner_model': toner.toner_model,
            'ink_type': toner.ink_type,
            'quantity': toner.quantity,
            'buying_price': str(toner.buying_price)
        }
        for toner in toners
    ]
    return JsonResponse(toner_data, safe=False)
