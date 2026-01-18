from .views import obtener_carrito

def carrito_context(request):
    return obtener_carrito(request)
