from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from comunidad.models import Resena
from django.contrib import messages

def es_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(es_admin)
def gestion_resenas(request):
    """Vista para gestionar reseñas desde el panel de administración"""
    resenas = Resena.objects.all().order_by('-fecha')
    
    context = {
        'resenas': resenas,
        'titulo': 'Gestión de Reseñas'
    }
    return render(request, 'resenas/gestion_resenas.html', context)

@login_required
@user_passes_test(es_admin)
def eliminar_resena(request, resena_id):
    """Eliminar una reseña específica"""
    resena = get_object_or_404(Resena, id=resena_id)
    
    if request.method == 'POST':
        comentario = resena.comentario[:30] + "..." if len(resena.comentario) > 30 else resena.comentario
        resena.delete()
        messages.success(request, f'Reseña "{comentario}" eliminada correctamente')
        return redirect('gestion_resenas')
    
    return render(request, 'resenas/confirmar_eliminar.html', {'resena': resena})
