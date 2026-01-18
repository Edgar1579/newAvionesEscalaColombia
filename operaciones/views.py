from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from PIL import Image
from operaciones.models import Producto, ImagenProducto
from operaciones.forms import ProductoForm, ProductoEditarForm


# ==========================
# UTILIDADES IMÁGENES
# ==========================

def redimensionar_imagen(imagen_path, size=(500, 500)):
    try:
        img = Image.open(imagen_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(imagen_path)
    except Exception as e:
        print(f"Error al redimensionar imagen: {e}")


def procesar_imagenes_adicionales(request, producto):
    imagenes = request.FILES.getlist('imagenes_adicionales')

    if imagenes:
        ultima_imagen = producto.imagenes_galeria.order_by('-orden').first()
        orden_inicial = ultima_imagen.orden + 1 if ultima_imagen else 1

        for idx, imagen in enumerate(imagenes):
            img = ImagenProducto.objects.create(
                producto=producto,
                imagen=imagen,
                orden=orden_inicial + idx
            )
            if img.imagen:
                redimensionar_imagen(img.imagen.path)


# ==========================
# PRODUCTOS
# ==========================

def producto_crear(request):
    productos = Producto.objects.filter(estado=True)
    titulo = "Producto"
    accion = "Agregar"

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()

            if producto.imagen:
                redimensionar_imagen(producto.imagen.path)

            procesar_imagenes_adicionales(request, producto)

            messages.success(request, f'Producto "{producto.nombre}" agregado correctamente')
            return redirect("productos")
        else:
            messages.error(request, "Error al agregar producto")
    else:
        form = ProductoForm()

    return render(request, "operaciones/productos/productos.html", {
        "titulo": titulo,
        "productos": productos,
        "form": form,
        "accion": accion
    })


def producto_editar(request, pk):
    producto = get_object_or_404(Producto, id=pk)
    productos = Producto.objects.filter(estado=True)
    imagenes_galeria = producto.imagenes_galeria.all()

    if request.method == "POST":
        form = ProductoEditarForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()

            if 'imagen' in request.FILES and producto.imagen:
                redimensionar_imagen(producto.imagen.path)

            procesar_imagenes_adicionales(request, producto)

            messages.success(request, "Producto editado correctamente")
            return redirect("productos")
        else:
            messages.error(request, "Error al editar producto")
    else:
        form = ProductoEditarForm(instance=producto)

    return render(request, "operaciones/productos/productos.html", {
        "titulo": f"Producto {producto.id}",
        "productos": productos,
        "producto": producto,
        "imagenes_galeria": imagenes_galeria,
        "form": form,
        "accion": "Editar"
    })


def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, id=pk)
    producto.estado = False
    producto.save()
    messages.success(request, "Producto eliminado")
    return redirect("productos")


def imagen_galeria_eliminar(request, pk):
    imagen = get_object_or_404(ImagenProducto, id=pk)
    producto_id = imagen.producto.id

    if imagen.imagen:
        imagen.imagen.delete()

    imagen.delete()
    messages.success(request, "Imagen eliminada")
    return redirect("producto_editar", pk=producto_id)


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk, estado=True)
    imagenes_galeria = producto.imagenes_galeria.all()

    return render(request, "operaciones/productos/detalle.html", {
        "producto": producto,
        "imagenes_galeria": imagenes_galeria
    })


# ==========================
# CARRITO
# ==========================

def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})
    pid = str(producto_id)

    if pid in carrito:
        carrito[pid]['cantidad'] += 1
    else:
        carrito[pid] = {
            'producto_id': producto.id,
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': 1,
            'imagen': producto.imagen.url if producto.imagen else ''
        }

    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', '/'))


def sumar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    pid = str(producto_id)

    if pid in carrito:
        carrito[pid]['cantidad'] += 1

    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', '/'))


def restar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    pid = str(producto_id)

    if pid in carrito:
        carrito[pid]['cantidad'] -= 1
        if carrito[pid]['cantidad'] <= 0:
            del carrito[pid]

    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', '/'))


def quitar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    pid = str(producto_id)

    if pid in carrito:
        del carrito[pid]

    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', '/'))


def obtener_carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0
    cantidad_items = 0

    for item in carrito.values():
        precio = float(item.get('precio', 0))
        cantidad = int(item.get('cantidad', 0))

        item['subtotal'] = precio * cantidad   # 👈 CLAVE
        total += item['subtotal']
        cantidad_items += cantidad

    return {
        'carrito': carrito,
        'total': round(total, 2),
        'cantidad_items': cantidad_items
    }


# ==========================
# PEDIDO WHATSAPP
# ==========================

def pedido_whatsapp(request):
    carrito = request.session.get('carrito', {})

    if not carrito:
        return redirect('/')

    telefono = "573202109787"  # CAMBIA ESTE NÚMERO
    mensaje = "🛒 *Nuevo pedido*\n\n"
    total = 0

    for item in carrito.values():
        precio = float(item['precio'])
        cantidad = int(item['cantidad'])
        subtotal = precio * cantidad
        total += subtotal

        mensaje += f"• {item['nombre']} x {cantidad} = ${subtotal:,.0f}\n"

    mensaje += f"\n💰 *Total:* ${total:,.0f}"

    import urllib.parse
    mensaje = urllib.parse.quote(mensaje)

    request.session['carrito'] = {}
    request.session.modified = True

    return redirect(f"https://wa.me/{telefono}?text={mensaje}")


def vaciar_carrito(request):
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', '/'))
