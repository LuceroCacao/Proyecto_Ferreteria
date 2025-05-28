from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.db.models import Sum, F, Count
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Venta

from .models import Producto, Cliente, CategoriaProducto, Venta

# Dashboard
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


# Productos
class ProductosListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/productos_list.html'
    context_object_name = 'productos'
    paginate_by = 20


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


# Clientes
class ClientesListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'inventario/clientes_list.html'
    context_object_name = 'clientes'
    paginate_by = 20


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


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'inventario/cliente_confirm_delete.html'
    success_url = reverse_lazy('inventario:clientes_list')

# Logout
class LogoutGetView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ReporteInventarioView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/reportes_inventario.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        categoria_filtro = self.request.GET.get('categoria', '')
        stock_bajo_filtro = self.request.GET.get('stock_bajo') == '1'

        productos = Producto.objects.select_related('categoria')

        if categoria_filtro.isdigit():
            productos = productos.filter(categoria_id=int(categoria_filtro))

        if stock_bajo_filtro:
            productos = productos.filter(stock__lt=10)

        categorias = productos.values('categoria__nombre').annotate(total=Count('id_producto'))
        total = productos.count()
        bajo_stock = productos.filter(stock__lt=10).count()
        suficientes = total - bajo_stock

        ctx.update({
            'productos': productos,
            'categorias_disponibles': list(CategoriaProducto.objects.values('id_categoria', 'nombre')),
            'categoria_filtro': categoria_filtro,
            'stock_bajo_filtro': stock_bajo_filtro,
            'categorias': categorias,
            'total_productos': total,
            'productos_bajo_stock': bajo_stock,
            'productos_suficientes': suficientes,
            'fecha_actual': timezone.now().strftime("%d/%m/%Y %H:%M"),
        })

        return ctx

class ReporteVentasView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/reportes_ventas.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ventas = Venta.objects.select_related('cliente').all()
        ctx['ventas'] = ventas
        ctx['fecha_actual'] = timezone.now().strftime("%d/%m/%Y %H:%M")
        return ctx

class ExportarVentasPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ventas = Venta.objects.select_related('cliente').all()
        template = get_template('inventario/reporte_ventas_pdf.html')
        context = {
            'ventas': ventas,
            'fecha_actual': timezone.now().strftime("%d/%m/%Y %H:%M"),
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generando PDF', status=500)
        return response
    
class ReporteVentasPDFView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        ventas = Venta.objects.all().order_by('-fecha')
        template_path = 'inventario/reporte_ventas_pdf.html'
        context = {'ventas': ventas}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        return response

