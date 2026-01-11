from django.db import models
from comunidad.models import Tienda


def get_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    if instance.id:
        filename = f"{instance.id}-{instance.tienda.nombre}.{ext}"
    else:
        filename = f"temp-{instance.tienda.nombre}.{ext}"
    return f"operaciones/productos/{filename}"


def get_gallery_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    if instance.id and instance.producto.id:
        filename = f"{instance.producto.id}-galeria-{instance.id}.{ext}"
    else:
        filename = f"temp-galeria.{ext}"
    return f"operaciones/productos/galeria/{filename}"


class Producto(models.Model):
    imagen = models.ImageField(
        upload_to=get_image_filename, 
        blank=True, 
        null=True, 
        default="operaciones/productos/default.producto.png",
        verbose_name="Imagen Principal"
    )
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    precio = models.PositiveIntegerField(verbose_name="Precio")
    tienda = models.ForeignKey(Tienda, verbose_name="Tienda", on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name="Descripción")
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return self.nombre

    def get_todas_imagenes(self):
        """Retorna todas las imágenes del producto (principal + galería)"""
        imagenes = [self.imagen] if self.imagen else []
        imagenes.extend([img.imagen for img in self.imagenes_galeria.all()])
        return imagenes


class ImagenProducto(models.Model):
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE, 
        related_name='imagenes_galeria',
        verbose_name="Producto"
    )
    imagen = models.ImageField(
        upload_to=get_gallery_image_filename,
        verbose_name="Imagen"
    )
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    descripcion = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="Descripción de la imagen"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de subida")

    class Meta:
        verbose_name = "Imagen del Producto"
        verbose_name_plural = "Imágenes del Producto"
        ordering = ['orden', 'created_at']

    def __str__(self):
        return f"Imagen {self.orden} - {self.producto.nombre}"