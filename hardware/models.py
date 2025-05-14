from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Hardware(models.Model):
    """Base model for all hardware devices"""
    code = models.CharField(_('Código'), max_length=20, unique=True, null=True, blank=True)
    ip = models.CharField(_('IP'), max_length=15, unique=True, blank=True)
    serial_number = models.CharField(_('Número de Serie'), max_length=100, unique=True)
    brand = models.CharField(_('Marca'), max_length=100)
    model = models.CharField(_('Modelo'), max_length=100)
    purchase_date = models.DateField(_('Fecha de Compra'), null=True, blank=True)
    notes = models.TextField(_('Notas'), blank=True)

    class Meta:
        abstract = True
        verbose_name = _('Hardware')
        verbose_name_plural = _('Hardware')

class PC(Hardware):
    """Model for desktop computers"""
    processor = models.CharField(_('Procesador'), max_length=100)
    ram = models.CharField(_('RAM'), max_length=50)
    storage = models.CharField(_('Almacenamiento'), max_length=100)
    operating_system = models.CharField(_('Sistema Operativo'), max_length=100)

    class Meta:
        verbose_name = _('PC')
        verbose_name_plural = _('PCs')

    def __str__(self):
        return f"{self.brand} {self.model} - {self.serial_number}"

class MiniPC(Hardware):
    """Model for mini PCs"""
    processor = models.CharField(_('Procesador'), max_length=100)
    ram = models.CharField(_('RAM'), max_length=50)
    storage = models.CharField(_('Almacenamiento'), max_length=100)
    operating_system = models.CharField(_('Sistema Operativo'), max_length=100)

    class Meta:
        verbose_name = _('Mini PC')
        verbose_name_plural = _('Mini PCs')

    def __str__(self):
        return f"{self.brand} {self.model} - {self.serial_number}"

class Printer(Hardware):
    """Model for printers"""
    printer_type = models.CharField(_('Tipo de Impresora'), max_length=50)
    connection_type = models.CharField(_('Tipo de Conexión'), max_length=50)
    is_color = models.BooleanField(_('Es a Color'), default=False)

    class Meta:
        verbose_name = _('Impresora')
        verbose_name_plural = _('Impresoras')

    def __str__(self):
        return f"{self.brand} {self.model} - {self.serial_number}"

class InkStock(models.Model):
    """Model for printer ink stock"""
    toner_model = models.CharField(_('Modelo de Toner'), max_length=100, null=True, blank=True,)
    ink_type = models.CharField(_('Tipo de Tinta'), max_length=100)
    quantity = models.IntegerField(_('Cantidad'), default=0)
    buying_price = models.IntegerField(_('Precio de Compra'), default=0)
    purchase_date = models.DateField(_('Fecha de Compra'), null=True, blank=True)

    class Meta:
        verbose_name = _('Stock de Tinta')
        verbose_name_plural = _('Stock de Tintas')

    def __str__(self):
        return f"{self.ink_type} para {self.toner_model} - {self.quantity} unidades"

class PrinterMaintenance(models.Model):
    """Model for printer maintenance records"""
    MAINTENANCE_TYPES = [
        ('limpieza', _('Limpieza')),
        ('cambio_toner', _('Cambio de Toner')),
        ('cambio_piezas', _('Cambio de piezas')),
    ]

    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='maintenance_records', verbose_name=_('Impresora'))
    maintenance_type = models.CharField(_('Tipo de Mantenimiento'), max_length=20, choices=MAINTENANCE_TYPES, default='limpieza')
    maintenance_date = models.DateField(_('Fecha de Mantenimiento'))
    description = models.TextField(_('Descripción'))
    performed_by = models.CharField(_('Realizado por'), max_length=100)
    next_maintenance_date = models.DateField(_('Próxima Fecha de Mantenimiento'), null=True, blank=True)
    cost = models.IntegerField(_('Costo'), default=0, null=True, blank=True)
    toner = models.ForeignKey(InkStock, on_delete=models.SET_NULL, related_name='maintenance_records', verbose_name=_('Toner'), null=True, blank=True)

    class Meta:
        verbose_name = _('Mantenimiento de Impresora')
        verbose_name_plural = _('Mantenimientos de Impresoras')
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"Mantenimiento de {self.printer} - {self.maintenance_date}"

class NetworkCable(models.Model):
    """Model for network cables connecting devices"""
    cable_code = models.CharField(_('Código de Cable'), max_length=50, unique=True)
    source_device = models.CharField(_('Dispositivo de Origen'), max_length=100, help_text=_('Servidor o dispositivo de red de origen'))
    destination_device = models.CharField(_('Dispositivo de Destino'), max_length=100, help_text=_('Máquina o dispositivo de destino'))
    port_number = models.CharField(_('Número de Puerto'), max_length=20, help_text=_('Puerto donde está conectado el cable'))
    cable_type = models.CharField(_('Tipo de Cable'), max_length=50, blank=True, help_text=_('Ej: Ethernet, Fibra óptica, etc.'))
    cable_length = models.CharField(_('Longitud del Cable'), max_length=20, blank=True)
    installation_date = models.DateField(_('Fecha de Instalación'), null=True, blank=True)
    notes = models.TextField(_('Notas'), blank=True)

    class Meta:
        verbose_name = _('Cable de Red')
        verbose_name_plural = _('Cables de Red')
        ordering = ['cable_code']

    def __str__(self):
        return f"Cable {self.cable_code}: {self.source_device} → {self.destination_device} (Puerto: {self.port_number})"
