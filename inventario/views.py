from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.db.models import Sum, F
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView

from .models import Producto, Cliente, CategoriaProducto

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 1) Coste total de inventario
        ctx['total_cost'] = (
            Producto.objects.aggregate(
                total=Sum(F('precio_compra') * F('stock'))
            )['total'] or 0
        )

        # 2) Productos con stock bajo (<10)
        ctx['low_stock'] = Producto.objects.filter(stock__lt=10).count()

        # 3) Usuarios en el sistema
        User = get_user_model()
        ctx['user_count'] = User.objects.count()

        # 4) Datos para el gráfico: etiquetas y valores
        labels, data = [], []
        qs = CategoriaProducto.objects.annotate(
            total_stock=Sum('producto__stock')
        )
        for cat in qs:
            labels.append(cat.nombre)
            data.append(cat.total_stock or 0)
        ctx['category_labels'] = labels
        ctx['category_data']   = data

        # 5) Total de productos (para la tarjeta “Productos”)
        ctx['product_count'] = Producto.objects.count()

        return ctx


class ProductosListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/productos_list.html'
    context_object_name = 'productos'


class ClientesListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'inventario/clientes_list.html'
    context_object_name = 'clientes'

class LogoutGetView(LogoutView):
    """
    Cuando reciba un GET, lo trata internamente como POST
    para que LogoutView no devuelva 405.
    """
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
