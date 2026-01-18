# operaciones/context_processors.py
def carrito_context(request):
    """
    Context processor para hacer el carrito disponible en todas las plantillas
    """
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    cantidad_items = sum(item['cantidad'] for item in carrito.values())
    
    return {
        'carrito': carrito,
        'total': total,
        'cantidad_items': cantidad_items
    }