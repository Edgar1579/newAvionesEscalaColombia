from django.urls import path
from operaciones.views import (
    producto_crear, 
    producto_eliminar, 
    producto_editar,
    imagen_galeria_eliminar,
    producto_detalle,
)

urlpatterns = [
    path('productos/', producto_crear, name="productos"),
    path("productos/eliminar/<int:pk>/", producto_eliminar, name="producto-eliminar"),
    path("productos/editar/<int:pk>/", producto_editar, name="producto-editar"),
    
    # Nueva ruta para eliminar imágenes de la galería
    path('imagen-galeria/eliminar/<int:pk>/', imagen_galeria_eliminar, name='imagen_galeria_eliminar'),
    path('productos/detalle/<int:pk>/', producto_detalle, name='producto-detalle'),
]