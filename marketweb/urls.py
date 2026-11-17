from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path





from marketweb.view import (
    eliminar_carrito, home, registrar_cliente, listarclientes, eliminar_cliente, editar_cliente, 
    buscar_clientes_ajax, registrar_proveedor, listar_proveedores, editar_proveedor, 
    eliminar_proveedor, registrar_productos, listar_productos, registrar_categoria, listar_categorias,
    editar_producto, catalogo, ver_carrito, agregar_carrito, ver_carrito, actualizar_cantidad_carrito, vaciar_carrito, checkout, factura
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('registrar-cliente/', registrar_cliente, name='registrar_cliente'),
    path('listar-clientes/', listarclientes, name='listarclientes'),
    path('eliminar-cliente/<str:ide>/', eliminar_cliente, name='eliminar_cliente'),
    path('editar-cliente/<str:ide>/', editar_cliente, name='editar_cliente'),
    path('buscar-clientes/', buscar_clientes_ajax, name='buscar_clientes_ajax'),


    path('registrarproveedor/', registrar_proveedor, name='registrar_proveedor'),
    path('listar_proveedor/', listar_proveedores, name='listar_proveedores'),
    path('editar-proveedor/<int:idp>/', editar_proveedor, name='editar_proveedor'),
    path('eliminar-proveedor/<int:idp>/', eliminar_proveedor, name='eliminar_proveedor'),


    path('registrarproductos/', registrar_productos, name='registrar_productos'),
    path('listarproductos',listar_productos, name='listar_productos'),
    path('editar-producto/<int:pk>/', editar_producto, name='editar_producto'),


    path('listar-categorias/', listar_categorias, name='listar_categorias'),
    path('registrar-categoria/', registrar_categoria, name='registrar_categoria'),


    path('admin/', admin.site.urls),


    path('catalogo/', catalogo, name='catalogo'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', agregar_carrito, name='agregar_carrito'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_carrito, name='eliminar_carrito'),
    path('carrito/sumar/<int:producto_id>/', actualizar_cantidad_carrito, {'accion': 'sumar'}, name='sumar_cantidad'),
    path('carrito/restar/<int:producto_id>/', actualizar_cantidad_carrito, {'accion': 'restar'}, name='restar_cantidad'),
    path('carrito/vaciar/', vaciar_carrito, name='vaciar_carrito'),
    path('checkout/', checkout, name='checkout'),
    path('factura/<int:pedido_id>/', factura, name='factura'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)