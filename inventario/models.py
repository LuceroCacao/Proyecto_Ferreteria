# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(db_column='IDCategoria', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)
    descripcion = models.CharField(db_column='Descripcion', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'CategoriaProducto'

    def __str__(self):
        return self.nombre or f"Categoria {self.id_categoria}"


class Cliente(models.Model):
    id_cliente = models.AutoField(db_column='IDCliente', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)
    nit = models.CharField(db_column='NIT', max_length=20, blank=True, null=True)
    telefono = models.CharField(db_column='Telefono', max_length=20, blank=True, null=True)
    direccion = models.CharField(db_column='Direccion', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return self.nombre or f"Cliente {self.id_cliente}"


class CuentaContable(models.Model):
    id_cuenta = models.AutoField(db_column='IDCuenta', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=50, blank=True, null=True)
    codigo = models.CharField(db_column='Codigo', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'CuentaContable'

    def __str__(self):
        return self.nombre or f"Cuenta {self.id_cuenta}"


class Permiso(models.Model):
    id_permiso = models.AutoField(db_column='IDPermiso', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Permiso'

    def __str__(self):
        return self.nombre or f"Permiso {self.id_permiso}"


class Rol(models.Model):
    id_rol = models.AutoField(db_column='IDRol', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Rol'

    def __str__(self):
        return self.nombre or f"Rol {self.id_rol}"


class Usuario(models.Model):
    id_usuario = models.AutoField(db_column='IDUsuario', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)
    username = models.CharField(db_column='Username', max_length=50, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)
    password_hash = models.CharField(db_column='PasswordHash', max_length=255, blank=True, null=True)
    rol = models.ForeignKey(Rol, models.CASCADE, db_column='IDRol', blank=True, null=True)

    class Meta:
        db_table = 'Usuario'

    def __str__(self):
        return self.username or f"Usuario {self.id_usuario}"


class Producto(models.Model):
    id_producto = models.AutoField(db_column='IDProducto', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)
    descripcion = models.CharField(db_column='Descripcion', max_length=255, blank=True, null=True)
    precio_compra = models.DecimalField(db_column='PrecioCompra', max_digits=10, decimal_places=2, blank=True, null=True)
    precio_venta = models.DecimalField(db_column='PrecioVenta', max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(db_column='Stock', blank=True, null=True)
    unidad_medida = models.CharField(db_column='UnidadMedida', max_length=50, blank=True, null=True)
    categoria = models.ForeignKey(CategoriaProducto, models.CASCADE, db_column='IDCategoria', blank=True, null=True)

    class Meta:
        db_table = 'Producto'

    def __str__(self):
        return self.nombre or f"Producto {self.id_producto}"


class IngresoInventario(models.Model):
    id_ingreso = models.AutoField(db_column='IDIngreso', primary_key=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)
    proveedor = models.IntegerField(db_column='IDProveedor', blank=True, null=True)
    usuario_registro = models.ForeignKey(Usuario, models.CASCADE, db_column='UsuarioRegistro', blank=True, null=True)

    class Meta:
        db_table = 'IngresoInventario'

    def __str__(self):
        return f"Ingreso {self.id_ingreso} - {self.fecha:%Y-%m-%d}"


class DetalleIngresoInventario(models.Model):
    id_detalle = models.AutoField(db_column='IDDetalle', primary_key=True)
    ingreso = models.ForeignKey(IngresoInventario, models.CASCADE, db_column='IDIngreso', blank=True, null=True)
    producto = models.ForeignKey(Producto, models.CASCADE, db_column='IDProducto', blank=True, null=True)
    cantidad = models.IntegerField(db_column='Cantidad', blank=True, null=True)
    precio_compra = models.DecimalField(db_column='PrecioCompra', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'DetalleIngresoInventario'

    def __str__(self):
        return f"Detalle {self.id_detalle} - Ingreso {self.ingreso_id}"


class Factura(models.Model):
    id_factura = models.AutoField(db_column='IDFactura', primary_key=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, models.CASCADE, db_column='IDCliente', blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.CASCADE, db_column='IDUsuario', blank=True, null=True)
    total = models.DecimalField(db_column='Total', max_digits=10, decimal_places=2, blank=True, null=True)
    forma_pago = models.CharField(db_column='FormaPago', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Factura'

    def __str__(self):
        return f"Factura {self.id_factura} - {self.fecha:%Y-%m-%d}"


class DetalleFactura(models.Model):
    id_detalle = models.AutoField(db_column='IDDetalle', primary_key=True)
    factura = models.ForeignKey(Factura, models.CASCADE, db_column='IDFactura', blank=True, null=True)
    producto = models.ForeignKey(Producto, models.CASCADE, db_column='IDProducto', blank=True, null=True)
    cantidad = models.IntegerField(db_column='Cantidad', blank=True, null=True)
    precio_unitario = models.DecimalField(db_column='PrecioUnitario', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'DetalleFactura'

    def __str__(self):
        return f"Detalle {self.id_detalle} - Factura {self.factura_id}"


class TransaccionContable(models.Model):
    id_transaccion = models.AutoField(db_column='IDTransaccion', primary_key=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)
    descripcion = models.CharField(db_column='Descripcion', max_length=255, blank=True, null=True)
    monto_total = models.DecimalField(db_column='MontoTotal', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'TransaccionContable'

    def __str__(self):
        return f"Transaccion {self.id_transaccion} - {self.fecha:%Y-%m-%d}"


class DetalleTransaccionContable(models.Model):
    id_detalle = models.AutoField(db_column='IDDetalle', primary_key=True)
    transaccion = models.ForeignKey(TransaccionContable, models.CASCADE, db_column='IDTransaccion', blank=True, null=True)
    cuenta = models.ForeignKey(CuentaContable, models.CASCADE, db_column='IDCuenta', blank=True, null=True)
    monto = models.DecimalField(db_column='Monto', max_digits=10, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'DetalleTransaccionContable'

    def __str__(self):
        return f"DetalleTransaccion {self.id_detalle} - Transaccion {self.transaccion_id}"


class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, models.CASCADE, db_column='IDRol', primary_key=True)
    permiso = models.ForeignKey(Permiso, models.CASCADE, db_column='IDPermiso')

    class Meta:
        db_table = 'RolPermiso'
        unique_together = (('rol', 'permiso'),)

    def __str__(self):
        return f"Rol {self.rol_id} - Permiso {self.permiso_id}"

class Venta(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"

