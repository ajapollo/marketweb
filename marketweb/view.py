from django.shortcuts import render 
from django.shortcuts import render, redirect
from django.db import connection # Django ya tiene la conexión aquí
from django.core.paginator import Paginator
from django.db import connection
import re
from django.template.loader import render_to_string
from django.http import JsonResponse
def home(request):
    return render(request, 'home.html')
from .models import Proveedor, Producto, Categoria ,Pedido, DetallePedido


from django.core.paginator import Paginator
from django.db.models import Q


from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria


def registrar_cliente(request):
    error = None  # Inicializamos la variable de error en vacío
    
    if request.method == "POST":
        nom = request.POST.get('txtNom', '').strip()
        ape = request.POST.get('txtApe', '').strip()
        cel = request.POST.get('telefono', '').strip()
        dir = request.POST.get('txtDir', '').strip()
        tip = request.POST.get('cboTip', '').strip()
        num = request.POST.get('txtNum', '').strip()
        ema = request.POST.get('txtEma', '').strip()
        
        # Validaciones con expresiones regulares y isdigit()
        es_nombre_valido = bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nom)) if nom else False
        es_apellido_valido = bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', ape)) if ape else False
        es_num_valido = num.isdigit() if num else False
        es_cel_valido = cel.isdigit() if cel else False
        
        # Evaluamos paso a paso para crear el mensaje de alerta exacto
        if not (num and tip and nom and ape and cel and ema):
            error = "¡Atención! Por favor, completa todos los campos obligatorios."
        elif not es_nombre_valido:
            error = "Error: El campo 'Nombre' solo debe contener letras, no números."
        elif not es_apellido_valido:
            error = "Error: El campo 'Apellido' solo debe contener letras, no números."
        elif not es_num_valido:
            error = "Error: El 'Número de Identificación' debe ser completamente numérico."
        elif not es_cel_valido:
            error = "Error: El 'Celular' debe ser completamente numérico."
        else:
            # Si todo es correcto, ejecuta el procedimiento almacenado
            cursor = connection.cursor()
            cursor.execute("CALL sp_insertarcliente(%s, %s, %s, %s, %s, %s, %s)", [num, tip, nom, ape, dir, cel, ema])
            cursor.close()
            return redirect('listarclientes')
            
    # Si hay un error, se lo mandamos al HTML
    return render(request, 'cliente/registrarcliente.html', {'error': error})


from django.db import connection
from django.core.paginator import Paginator
from django.shortcuts import render

from django.core.paginator import Paginator
from django.db import connection
from django.http import JsonResponse
from django.template.loader import render_to_string


def listarclientes(request):
    busqueda = request.GET.get('buscar', '')
    
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_buscarcliente(%s)", [busqueda])
        resultados = cursor.fetchall()
        
    clientes_lista = []
    for row in resultados:
        cliente = {
            'id': row[0],
            'identificacion': row[1],
            'tipo': row[2],
            'nombres': row[3],          # Aquí viene el nombre o la empresa
            'apellidos': row[4],        # Aquí vienen los apellidos (si aplica)
            'direccion': row[5],
            'telefono': row[6],
            'email': row[7],
            'estado': row[8],
        }
        clientes_lista.append(cliente)
        
    # 1. ORDENAR: Los clientes recién creados salen de primero (por ID descendente)
    clientes_lista.sort(key=lambda x: x['id'], reverse=True)
        
    # 2. PAGINACIÓN: Exactamente 10 por página
    paginator = Paginator(clientes_lista, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)

# DETECCIÓN DE AJAX: Renderiza la misma vista principal
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('cliente/listarclientes.html', {'clientes': clientes, 'buscar': busqueda}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'cliente/listarclientes.html', {
        'clientes': clientes, 
        'buscar': busqueda
    })
    

def eliminar_cliente(request, ide):
    cursor = connection.cursor()
    cursor.callproc('sp_eliminarcliente', [ide])
    cursor.close()

    return redirect('listarclientes') 


def editar_cliente(request, ide):
    cursor = connection.cursor()
    cursor.callproc('sp_buscarcliente', [ide])
    cliente = cursor.fetchone() 
    cursor.close()
    

    if request.method == 'POST':
        tip = request.POST.get('tipo')
        nom = request.POST.get('nombres')
        ape = request.POST.get('apellidos')
        dir = request.POST.get('direccion')
        tel = request.POST.get('telefono')
        correo = request.POST.get('email')
        estado = request.POST.get('estado')
        
        cursor = connection.cursor()
        cursor.callproc('sp_actualizarcliente', [ide, tip, nom, ape, dir, tel, correo, estado])
        cursor.close()

        return redirect('listarclientes')
        

    return render(request, 'cliente/editar_cliente.html', {'cliente': cliente})


def buscar_clientes_ajax(request):
    busqueda = request.GET.get('term', '')
    cursor = connection.cursor()
    # Usamos tu procedimiento almacenado
    cursor.execute("CALL sp_filtrarclientes(%s)", [busqueda])
    resultados = cursor.fetchall()
    cursor.close()
    
    # Convertimos los resultados a una lista de diccionarios para enviarlos como JSON
    data = []
    for c in resultados:
        data.append({
            'num': c[1], 'tipo': c[2], 'nom': c[3], 'ape': c[4], 
            'dir': c[5], 'tel': c[6], 'email': c[7], 'estado': c[8]
        })
    return JsonResponse({'clientes': data})
#endregion







#region proveedores
def registrar_proveedor(request):
    if request.method == "POST":
        nom = request.POST.get('txtNom')
        cel = request.POST.get('telefono')
        dir = request.POST.get('txtDir')
        tip = request.POST.get('cboTip')
        num = request.POST.get('txtNum')
        ema = request.POST.get('txtEma')
        
        if nom and cel and dir and tip and num and ema:
            proveedor = Proveedor()
            proveedor.nombre = nom
            proveedor.identificacion = num
            proveedor.direccion = dir
            proveedor.telefono = cel
            proveedor.email = ema
            proveedor.tipo = tip
            proveedor.save()
            
    return render(request, 'proveedor/registrar_proveedor.html')





def listar_proveedores(request):
    busqueda = request.GET.get('buscar', '')
    page = request.GET.get('page', 1)
    
    if busqueda:
        # Filtramos por TODOS los campos usando Q con icontains
        lista_proveedores_qs = Proveedor.objects.filter(
            Q(tipo__icontains=busqueda) |
            Q(identificacion__icontains=busqueda) | 
            Q(nombre__icontains=busqueda) |
            Q(direccion__icontains=busqueda) |
            Q(telefono__icontains=busqueda) |
            Q(email__icontains=busqueda)
        )
    else:
        lista_proveedores_qs = Proveedor.objects.all()

    paginator = Paginator(lista_proveedores_qs, 10)
    page_obj = paginator.get_page(page)

    # Si la petición viene por AJAX, renderizamos solo el bloque de la tabla/paginación
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_completo = render_to_string('proveedor/listar_proveedores.html', {
            'lista_proveedores': page_obj, 
            'buscar': busqueda
        }, request=request)
        return JsonResponse({'html': html_completo})

    return render(request, 'proveedor/listar_proveedores.html', {
        'lista_proveedores': page_obj, 
        'buscar': busqueda
    })





def editar_proveedor(request, idp):
    # Usamos .get() para traer UN SOLO objeto proveedor por su ID
    proveedor = Proveedor.objects.get(id=idp)
    
    if request.method == "POST":
        nom = request.POST.get('txtNom')
        cel = request.POST.get('telefono')
        dir = request.POST.get('txtDir')
        tip = request.POST.get('cboTip')
        num = request.POST.get('txtNum')
        ema = request.POST.get('txtEma')
        
        if nom and cel and dir and tip and num and ema:
            # Actualizamos los datos del objeto existente
            proveedor.nombre = nom
            proveedor.identificacion = num
            proveedor.direccion = dir
            proveedor.telefono = cel
            proveedor.email = ema
            proveedor.tipo = tip
            proveedor.save()
            
            return redirect ('listar_proveedores') # O la ruta de tu listado
            
    # Al entrar por GET, mandamos el objeto individual a la variable 'provee'
    return render(request, 'proveedor/editar_proveedor.html', {'provee': proveedor})



def eliminar_proveedor(request, idp):  # <-- Debe llamarse 'idp' igual que en la URL
    proveedor = Proveedor.objects.get(id=idp)
    proveedor.estado = False
    proveedor.save()
    return redirect('listar_proveedores')
#endregion






#region Productos

def registrar_productos(request):
    mensaje = None
    
    if request.method == 'POST':
        try:
            # Capturamos los datos del formulario
            codigo = request.POST.get('codigo')
            nombre = request.POST.get('nombre')
            costo = request.POST.get('costo')
            precio = request.POST.get('precio')
            iva = request.POST.get('iva') or None
            stock = request.POST.get('stock')
            minstock = request.POST.get('minstock')
            imagen = request.POST.get('imagen')  # Aquí recibe el texto (ej: "pollito.jpg")
            id_categorias = request.POST.get('idCategorias')
            
            # Guardamos el producto usando el ORM de Django
            # Usamos idCategorias_id para asignar directamente por la llave foránea numérica
            Producto.objects.create(
                codigo=codigo,
                nombre=nombre,
                costo=costo,
                precio=precio,
                iva=iva,
                stock=stock,
                minstock=minstock,
                imagen=imagen,
                idCategorias_id=id_categorias, 
                estado=True
            )
            
            mensaje = "¡Producto registrado con éxito!"
        except Exception as e:
            mensaje = f"Error al registrar el producto: {str(e)}"

    # Consultamos todas las categorías directamente con el modelo de Django
    categorias = Categoria.objects.all()

    contexto = {
        'categorias': categorias,
        'mensaje': mensaje
    }
    
    return render(request, 'productos/registrar_productos.html', contexto)




from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    categorias = Categoria.objects.all()
    mensaje = None

    if request.method == 'POST':
        try:
            producto.codigo = request.POST.get('codigo')
            producto.nombre = request.POST.get('nombre')
            producto.costo = request.POST.get('costo')
            producto.precio = request.POST.get('precio')
            producto.iva = request.POST.get('iva') or None
            producto.stock = request.POST.get('stock')
            producto.minstock = request.POST.get('minstock')
            producto.imagen = request.POST.get('imagen')
            
            categoria_id = request.POST.get('idCategorias')
            if categoria_id:
                producto.idCategorias_id = categoria_id

            producto.save()
            mensaje = "¡Producto actualizado con éxito!"
        except Exception as e:
            mensaje = f"Error al actualizar el producto: {str(e)}"

    contexto = {
        'producto': producto,
        'categorias': categorias,
        'mensaje': mensaje
    }
    
    # Asegúrate de usar 'Productos/' con P mayúscula aquí:
    return render(request, 'Productos/editar_producto.html', contexto)







def listar_productos(request):
    busqueda = request.GET.get('buscar', '')
    page = request.GET.get('page', 1)
    
    if busqueda:
        productos_qs = Producto.objects.filter(
            Q(codigo__icontains=busqueda) |
            Q(nombre__icontains=busqueda)
        ).order_by('id')  
    else:
        productos_qs = Producto.objects.all().order_by('id')

    paginator = Paginator(productos_qs, 8)
    page_obj = paginator.get_page(page)

    contexto = {
        'productos': page_obj,
        'buscar': busqueda
    }
    return render(request, 'Productos/listar_productos.html', contexto)

#region Categorias
def listar_categorias(request):
    busqueda = request.GET.get('buscar', '')
    page = request.GET.get('page', 1)
    
    if busqueda:
        categorias_qs = Categoria.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        ).order_by('id')
    else:
        categorias_qs = Categoria.objects.all().order_by('id')

    paginator = Paginator(categorias_qs, 10)
    page_obj = paginator.get_page(page)

    contexto = {
        'categorias': page_obj,
        'buscar': busqueda
    }
    return render(request, 'productos/listar_categorias.html', contexto)


def registrar_categoria(request):
    mensaje = None
    
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            
            if nombre and descripcion:
                Categoria.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    estado=True
                )
                return redirect('listar_categorias')
            else:
                mensaje = "Por favor, completa todos los campos obligatorios."
        except Exception as e:
            mensaje = f"Error al registrar la categoría: {str(e)}"

    contexto = {
        'mensaje': mensaje
    }
    return render(request, 'productos/registrar_categoria.html', contexto)
#endregion
#endregion







def catalogo(request):
    categoria_id = request.GET.get('categoria', '')
    page = request.GET.get('page', 1)

    productos_qs = Producto.objects.all().order_by('id')

    if categoria_id:
        productos_qs = productos_qs.filter(idCategorias=categoria_id)

    paginator = Paginator(productos_qs, 8)
    page_obj = paginator.get_page(page)

    contexto = {
        'productos': page_obj,
        'categorias': Categoria.objects.all(),
        'categoria_seleccionada': categoria_id,
    }
    return render(request, 'Productos/catalogo.html', contexto)




def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for pid, data in carrito.items():
        subtotal = float(data['precio']) * data['cantidad']
        total += subtotal
        items.append({
            'id': pid,
            'nombre': data['nombre'],
            'precio': data['precio'],
            'imagen': data.get('imagen', ''),
            'cantidad': data['cantidad'],
            'subtotal': subtotal,
        })
    return render(request, 'carrito.html', {'items': items, 'total': total})

def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = request.session.get('carrito', {})
    pid = str(producto_id)

    if pid in carrito:
        carrito[pid]['cantidad'] += 1
    else:
        carrito[pid] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'imagen': str(producto.imagen) if producto.imagen else '',
            'cantidad': 1,
        }

    request.session['carrito'] = carrito
    request.session.modified = True

    return JsonResponse({
        'ok': True,
        'nombre': producto.nombre,
        'total_items': sum(item['cantidad'] for item in carrito.values())
    })


def eliminar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    pid = str(producto_id)
    if pid in carrito:
        del carrito[pid]
        request.session['carrito'] = carrito
        request.session.modified = True
    return redirect('ver_carrito')




def actualizar_cantidad_carrito(request, producto_id, accion):
    carrito = request.session.get('carrito', {})
    pid = str(producto_id)

    if pid in carrito:
        if accion == 'sumar':
            carrito[pid]['cantidad'] += 1
        elif accion == 'restar':
            carrito[pid]['cantidad'] -= 1
            if carrito[pid]['cantidad'] <= 0:
                del carrito[pid]

        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('ver_carrito')





def vaciar_carrito(request):
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect('ver_carrito')




#region Checkout y Factura
def checkout(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('carrito')

    items = []
    total = 0
    for pid, data in carrito.items():
        subtotal = float(data['precio']) * data['cantidad']
        total += subtotal
        items.append({
            'nombre': data['nombre'],
            'precio': data['precio'],
            'cantidad': data['cantidad'],
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        pedido = Pedido.objects.create(
            nombre_cliente=nombre,
            telefono=telefono,
            direccion=direccion,
            total=total,
        )

        for item in items:
            DetallePedido.objects.create(
                pedido=pedido,
                nombre_producto=item['nombre'],
                precio_unitario=item['precio'],
                cantidad=item['cantidad'],
                subtotal=item['subtotal'],
            )

        request.session['carrito'] = {}
        request.session.modified = True

        return redirect('factura', pedido_id=pedido.numero)

    return render(request, 'checkout.html', {'items': items, 'total': total})


def factura(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    return render(request, 'factura.html', {'pedido': pedido})
#endregion