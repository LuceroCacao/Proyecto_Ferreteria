from django.urls import path
from .views import DashboardView, ProductosListView, ClientesListView

app_name = 'inventario'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('productos/', ProductosListView.as_view(), name='productos_list'),
    path('clientes/', ClientesListView.as_view(), name='clientes_list'),
]

