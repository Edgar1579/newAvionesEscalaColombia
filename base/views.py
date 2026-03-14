from django.shortcuts import render, redirect
from configuracion.models import Slider
from comunidad.models import Usuario, Tienda, Resena
from operaciones.models import Producto
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings



def principal(request):
    titulo = "Bienvenido"
    sliders= Slider.objects.filter(estado=True)
    productos= Producto.objects.all()
    resenas = Resena.objects.all().order_by('-fecha')[:6]  # Últimas 6 reseñas
    
    context={
        "titulo": titulo,
        "sliders": sliders,
        "productos": productos,
        "resenas": resenas,  # Agregar reseñas al contexto
    }
    return render(request, "index.html", context)


@login_required
def principal_admin(request):
    titulo = "Bienvenido"
    
    # Obtener las cantidades correctas
    usuarios = Usuario.objects.all().count()
    tiendas = Tienda.objects.all().count()  
    productos = Producto.objects.all().count() 
    resenas = Resena.objects.all().count()  # Agregar conteo de reseñas

    # Obtener nombres de tiendas y cantidad de productos por tienda
    tiendas_con_productos = Tienda.objects.annotate(cantidad_productos=Count('producto', filter=Q(producto__estado=True))).values('nombre', 'cantidad_productos')
    
    
    usuarios_obj = Usuario.objects.all()

    context = {
        "titulo": titulo,
        "usuarios_cantidad": usuarios,
        "tiendas_cantidad": tiendas,
        "productos_cantidad": productos,
        "resenas_cantidad": resenas,  # Agregar al contexto
        "usuarios_obj": usuarios_obj,
        "tiendas_con_productos": tiendas_con_productos
    }

    return render(request, "index-admin.html", context)

def logout_user(request):
    logout(request)
    return redirect('index')

def agregar_resena(request):
    """Procesar el formulario de reseñas del modal"""
    if request.method == 'POST':
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario')
        
        # Validaciones básicas
        if not puntuacion or not comentario:
            messages.error(request, 'Por favor completa todos los campos')
            return redirect('index')
        
        try:
            puntuacion = int(puntuacion)
            if puntuacion < 1 or puntuacion > 5:
                messages.error(request, 'La puntuación debe ser entre 1 y 5 estrellas')
                return redirect('index')
        except ValueError:
            messages.error(request, 'Puntuación inválida')
            return redirect('index')
        
        # Crear la reseña
        resena = Resena.objects.create(
            puntuacion=puntuacion,
            comentario=comentario.strip()
        )
        
        # Enviar correo de notificación
        try:
            asunto = f'⭐ Nueva Reseña - {puntuacion} estrellas'
            mensaje = f'''
Nueva reseña recibida en Aviones a Escala Colombia:

📊 Calificación: {puntuacion} estrellas {'⭐' * puntuacion}
💬 Comentario: "{comentario}"
📅 Fecha: {resena.fecha.strftime('%d/%m/%Y %H:%M')}

---
Este es un mensaje automático de tu aplicación Django.
            '''
            
            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                ['avecbm2024@gmail.com'],  # Tu correo para recibir notificaciones
                fail_silently=False,
            )
            
            messages.success(request, '¡Gracias por tu opinión! Tu reseña ha sido enviada correctamente.')
            
        except Exception as e:
            # Si el correo falla, igual guardamos la reseña
            print(f"Error al enviar correo: {e}")
            messages.success(request, '¡Gracias por tu opinión! Tu reseña ha sido guardada.')
        
        return redirect('index')
    
    return redirect('index')