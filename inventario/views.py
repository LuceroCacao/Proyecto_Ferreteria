# inventario/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, ListView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Sum, F
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView

from .models import Producto, Cliente, CategoriaProducto


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['total_cost'] = (
            Producto.objects.aggregate(
                total=Sum(F('precio_compra') * F('stock'))
            )['total'] or 0
        )
        ctx['low_stock'] = Producto.objects.filter(stock__lt=10).count()
        ctx['user_count'] = get_user_model().objects.count()

        labels, data = [], []
        for cat in CategoriaProducto.objects.annotate(total_stock=Sum('producto__stock')):
            labels.append(cat.nombre)
            data.append(cat.total_stock or 0)
        ctx['category_labels'] = labels
        ctx['category_data'] = data
        ctx['product_count'] = Producto.objects.count()

        return ctx


class ProductosListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/productos_list.html'
    context_object_name = 'productos'
    paginate_by = 20


class ClientesListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'inventario/clientes_list.html'
    context_object_name = 'clientes'
    paginate_by = 20


class LogoutGetView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    fields = [
        'nombre', 'categoria',
        'precio_compra', 'precio_venta',
        'stock', 'unidad_medida', 'descripcion'
    ]
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('inventario:productos_list')


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    fields = [
        'nombre', 'categoria',
        'precio_compra', 'precio_venta',
        'stock', 'unidad_medida', 'descripcion'
    ]
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('inventario:productos_list')


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('inventario:productos_list')


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ['nombre', 'nit', 'telefono', 'direccion']  # ← Aquí está el cambio
    template_name = 'inventario/cliente_form.html'
    success_url = reverse_lazy('inventario:clientes_list')


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nombre', 'nit', 'telefono', 'correo', 'direccion']
    template_name = 'inventario/cliente_form.html'
    success_url = reverse_lazy('inventario:clientes_list')


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'inventario/cliente_confirm_delete.html'
    success_url = reverse_lazy('inventario:clientes_list')

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ['nombre', 'nit', 'telefono', 'direccion']
    template_name = 'inventario/cliente_form.html'
    success_url = reverse_lazy('inventario:clientes_list')


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nombre', 'nit', 'telefono', 'direccion']
    template_name = 'inventario/cliente_form.html'
    success_url = reverse_lazy('inventario:clientes_list')


