from django.db import models
from django.utils import timezone

class Proveedor(models.Model):
    tipo = models.CharField(max_length=50, blank=True, null=True)
    identificacion = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=45)
    estado = models.BooleanField(default=True)

    class Meta:
        app_label = 'marketweb'  # <--- Todos deben tener 'marketweb'
        db_table = 'proveedores'


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=245)
    estado = models.BooleanField(default=True)

    class Meta:
        app_label = 'marketweb'  # <--- Todos deben tener 'marketweb'
        db_table = 'categorias'


class Producto(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField()
    minstock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    estado = models.BooleanField(default=True)
    idCategorias = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='idCategorias')

    class Meta:
        app_label = 'marketweb'  # <--- Todos deben tener 'marketweb'
        db_table = 'productos'


class Pedido(models.Model):
    numero = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30)
    direccion = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.numero} - {self.nombre_cliente}"

    class Meta:
        app_label = 'marketweb'  # <--- Todos deben tener 'marketweb'
        db_table = 'pedidos'


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=150)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.nombre_producto} x{self.cantidad}"

    class Meta:
        app_label = 'marketweb'  # <--- Todos deben tener 'marketweb'
        db_table = 'detalle_pedidos'