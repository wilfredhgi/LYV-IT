from django.urls import path
from . import views

urlpatterns = [
    # Home/Dashboard
    path('', views.home, name='home'),

    # PC URLs
    path('pcs/', views.PCListView.as_view(), name='pc-list'),
    path('pcs/<int:pk>/', views.PCDetailView.as_view(), name='pc-detail'),
    path('pcs/new/', views.PCCreateView.as_view(), name='pc-create'),
    path('pcs/<int:pk>/update/', views.PCUpdateView.as_view(), name='pc-update'),
    path('pcs/<int:pk>/delete/', views.PCDeleteView.as_view(), name='pc-delete'),

    # MiniPC URLs
    path('minipcs/', views.MiniPCListView.as_view(), name='minipc-list'),
    path('minipcs/<int:pk>/', views.MiniPCDetailView.as_view(), name='minipc-detail'),
    path('minipcs/new/', views.MiniPCCreateView.as_view(), name='minipc-create'),
    path('minipcs/<int:pk>/update/', views.MiniPCUpdateView.as_view(), name='minipc-update'),
    path('minipcs/<int:pk>/delete/', views.MiniPCDeleteView.as_view(), name='minipc-delete'),

    # Printer URLs
    path('printers/', views.PrinterListView.as_view(), name='printer-list'),
    path('printers/<int:pk>/', views.PrinterDetailView.as_view(), name='printer-detail'),
    path('printers/new/', views.PrinterCreateView.as_view(), name='printer-create'),
    path('printers/<int:pk>/update/', views.PrinterUpdateView.as_view(), name='printer-update'),
    path('printers/<int:pk>/delete/', views.PrinterDeleteView.as_view(), name='printer-delete'),

    # Maintenance URLs
    path('maintenance/', views.MaintenanceListView.as_view(), name='maintenance-list'),
    path('maintenance/<int:pk>/', views.MaintenanceDetailView.as_view(), name='maintenance-detail'),
    path('maintenance/new/', views.MaintenanceCreateView.as_view(), name='maintenance-create'),
    path('maintenance/<int:pk>/update/', views.MaintenanceUpdateView.as_view(), name='maintenance-update'),
    path('maintenance/<int:pk>/delete/', views.MaintenanceDeleteView.as_view(), name='maintenance-delete'),

    # InkStock URLs
    path('inkstock/', views.InkStockListView.as_view(), name='inkstock-list'),
    path('inkstock/<int:pk>/', views.InkStockDetailView.as_view(), name='inkstock-detail'),
    path('inkstock/new/', views.InkStockCreateView.as_view(), name='inkstock-create'),
    path('inkstock/<int:pk>/update/', views.InkStockUpdateView.as_view(), name='inkstock-update'),
    path('inkstock/<int:pk>/delete/', views.InkStockDeleteView.as_view(), name='inkstock-delete'),

    # API URLs
    path('api/printer/<int:printer_id>/toners/', views.get_printer_toners, name='api-printer-toners'),
]
