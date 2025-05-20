from django.contrib import admin
from .models import (
    CategoriaProducto, Producto, Cliente, IngresoInventario,
    DetalleIngresoInventario, Factura, DetalleFactura,
    CuentaContable, TransaccionContable, DetalleTransaccionContable,
    Rol, Permiso, RolPermiso, Usuario
)

admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(IngresoInventario)
admin.site.register(DetalleIngresoInventario)
admin.site.register(Factura)
admin.site.register(DetalleFactura)
admin.site.register(CuentaContable)
admin.site.register(TransaccionContable)
admin.site.register(DetalleTransaccionContable)
admin.site.register(Rol)
admin.site.register(Permiso)
admin.site.register(RolPermiso)
admin.site.register(Usuario)
