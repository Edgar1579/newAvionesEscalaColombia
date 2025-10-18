from django.urls import path
from comunidad.views import usuario_crear, usuario_eliminar, usuario_editar, edit_group

urlpatterns = [
    path('usuarios/', usuario_crear, name="usuarios"),
    path("usuarios/eliminar/<int:pk>/", usuario_eliminar, name="usuario-eliminar"),
    path("usuarios/editar/<int:pk>/", usuario_editar, name="usuario-editar"),
    
    
    path('edit_group/', edit_group, name='create_group'),
    path('edit_group/<int:group_id>/', edit_group, name='edit_group'),
]