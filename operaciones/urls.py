from django.urls import path
from operaciones.views import (
    producto_crear, 
    producto_eliminar, 
    producto_editar,
    imagen_galeria_eliminar,
    producto_detalle,
    agregar_carrito,
    sumar_carrito,
    restar_carrito,
    quitar_carrito,
    pedido_whatsapp,
    vaciar_carrito
)

urlpatterns = [
    path('productos/', producto_crear, name="productos"),
    path("productos/eliminar/<int:pk>/", producto_eliminar, name="producto-eliminar"),
    path("productos/editar/<int:pk>/", producto_editar, name="producto-editar"),
    
    # Nueva ruta para eliminar imágenes de la galería
    path('imagen-galeria/eliminar/<int:pk>/', imagen_galeria_eliminar, name='imagen_galeria_eliminar'),
    path('productos/detalle/<int:pk>/', producto_detalle, name='producto-detalle'),
    path("agregar/<int:producto_id>/", agregar_carrito, name="agregar_carrito"),
    path("sumar/<int:producto_id>/", sumar_carrito, name="sumar_carrito"),
    path("restar/<int:producto_id>/", restar_carrito, name="restar_carrito"),
    path("quitar/<int:producto_id>/", quitar_carrito, name="quitar_carrito"),
    path("pedido/whatsapp/", pedido_whatsapp, name="pedido_whatsapp"),
    path("vaciar/", vaciar_carrito, name="vaciar_carrito"),

]