# inventario/views.py

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
        ctx['user_count'] = get_user_model().objects.count()

        # 4) Datos para el gráfico: etiquetas y valores
        labels, data = [], []
        for cat in CategoriaProducto.objects.annotate(total_stock=Sum('producto__stock')):
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
    paginate_by = 20  # quita o ajusta según prefieras


class ClientesListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'inventario/clientes_list.html'
    context_object_name = 'clientes'
    paginate_by = 20


class LogoutGetView(LogoutView):
    """
    Permite hacer logout vía GET (redirigiendo internamente al POST).
    Así evitamos el 405 cuando el usuario hace click en “Salir”.
    """
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
