from django.shortcuts import render, redirect, get_object_or_404
from PIL import Image
from django.contrib import messages
from operaciones.models import Producto, ImagenProducto
from operaciones.forms import ProductoForm, ProductoEditarForm


def redimensionar_imagen(imagen_path, size=(500, 500)):
    """Función auxiliar para redimensionar imágenes"""
    try:
        img = Image.open(imagen_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(imagen_path)
    except Exception as e:
        print(f"Error al redimensionar imagen: {e}")


def procesar_imagenes_adicionales(request, producto):
    """Función auxiliar para procesar múltiples imágenes"""
    imagenes = request.FILES.getlist('imagenes_adicionales')
    
    if imagenes:
        # Obtener el último orden de las imágenes existentes
        ultima_imagen = producto.imagenes_galeria.order_by('-orden').first()
        orden_inicial = ultima_imagen.orden + 1 if ultima_imagen else 1
        
        for idx, imagen in enumerate(imagenes):
            imagen_producto = ImagenProducto.objects.create(
                producto=producto,
                imagen=imagen,
                orden=orden_inicial + idx
            )
            # Redimensionar cada imagen de la galería
            if imagen_producto.imagen:
                redimensionar_imagen(imagen_producto.imagen.path)


def producto_crear(request):
    titulo = "Producto"
    accion = "Agregar"
    productos = Producto.objects.filter(estado=True)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            
            # Redimensionar imagen principal
            if producto.imagen:
                redimensionar_imagen(producto.imagen.path)
            
            # Procesar imágenes adicionales de la galería
            procesar_imagenes_adicionales(request, producto)
            
            producto.save()
            messages.success(request, f'¡El Producto "{producto.nombre}" se agregó de forma exitosa!') 
            return redirect("productos")
        else:
            messages.error(request, '¡Error al agregar el Producto! Verifica los datos.') 
    else:
        form = ProductoForm()
    
    context = {
        "titulo": titulo,
        "productos": productos,
        "form": form,
        "accion": accion
    }
    return render(request, "operaciones/productos/productos.html", context)


def producto_editar(request, pk):
    producto = get_object_or_404(Producto, id=pk)
    productos = Producto.objects.filter(estado=True)
    imagenes_galeria = producto.imagenes_galeria.all()
    
    accion = "Editar"
    nombre = f"{producto.nombre}"
    titulo = f"Producto {producto.id} - {nombre}"

    if request.method == "POST":
        form = ProductoEditarForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            
            # Redimensionar imagen principal si se actualizó
            if 'imagen' in request.FILES and producto.imagen:
                redimensionar_imagen(producto.imagen.path)
            
            # Procesar nuevas imágenes adicionales
            procesar_imagenes_adicionales(request, producto)
            
            producto.save()
            messages.success(request, f'¡{nombre} se editó de forma exitosa!')
            return redirect("productos")
        else:
            messages.error(request, f'¡Error al editar {nombre}!')
    else:
        form = ProductoEditarForm(instance=producto)
    
    context = {
        "titulo": titulo,
        "productos": productos,
        "producto": producto,
        "imagenes_galeria": imagenes_galeria,
        "form": form,
        "accion": accion
    }
    return render(request, "operaciones/productos/productos.html", context)


def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, id=pk)
    nombre = producto.nombre
    producto.estado = False
    producto.save()
    
    messages.success(request, f'¡El Producto "{nombre}" se eliminó correctamente!')
    return redirect('productos')


def imagen_galeria_eliminar(request, pk):
    """Vista para eliminar una imagen específica de la galería"""
    imagen = get_object_or_404(ImagenProducto, id=pk)
    producto_id = imagen.producto.id
    
    # Eliminar el archivo físico
    if imagen.imagen:
        imagen.imagen.delete()
    
    imagen.delete()
    messages.success(request, '¡Imagen eliminada de la galería!')
    return redirect('producto_editar', pk=producto_id)
def producto_detalle(request, pk):
    """Vista para ver el detalle de un producto con todas sus imágenes"""
    producto = get_object_or_404(Producto, pk=pk, estado=True)
    imagenes_galeria = producto.imagenes_galeria.all()
    
    context = {
        'producto': producto,
        'imagenes_galeria': imagenes_galeria,
    }
    return render(request, 'operaciones/productos/detalle.html', context)