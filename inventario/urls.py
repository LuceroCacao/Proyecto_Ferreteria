from django.urls import path
from .views import (
    DashboardView,
    ProductosListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView,
    ClientesListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    LogoutGetView,
)

app_name = 'inventario'

urlpatterns = [
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),

    # Productos
    path('productos/', ProductosListView.as_view(), name='productos_list'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/borrar/', ProductoDeleteView.as_view(), name='producto_delete'),

    # Clientes
    path('clientes/', ClientesListView.as_view(), name='clientes_list'),
    path('clientes/nuevo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/borrar/', ClienteDeleteView.as_view(), name='cliente_delete'),
        

    # Logout
    path('logout/', LogoutGetView.as_view(next_page='login'), name='logout'),
]

