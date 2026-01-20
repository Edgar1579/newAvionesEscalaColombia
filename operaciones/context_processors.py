def carrito_context(request):
    carrito = request.session.get('carrito', {})
    total = 0
    cantidad_items = 0

    for item in carrito.values():
        precio = float(item.get('precio', 0))
        cantidad = int(item.get('cantidad', 0))
        item['subtotal'] = precio * cantidad
        total += item['subtotal']
        cantidad_items += cantidad

    return {
        'carrito': carrito,
        'total': round(total, 2),
        'cantidad_items': cantidad_items
    }
