from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from configuracion.models import Slider
from configuracion.forms import SliderForm

def slider(request):
    """Vista para listar y crear sliders"""
    titulo = "Slider"
    accion = "Agregar"
    sliders = Slider.objects.filter(estado=True).order_by('-prioridad')
    
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_slider = form.save()
            messages.success(request, f'¡El Slider "{nuevo_slider.nombre}" se agregó exitosamente!')
            return redirect("sliders")
        else:
            messages.error(request, '¡Error al agregar slider!')
    else:
        form = SliderForm()
    
    context = {
        "titulo": titulo,
        "form": form,
        "sliders": sliders,
        "accion": accion
    }
    return render(request, "configuracion/slider.html", context)


def slider_editar(request, pk):
    """Vista para editar un slider"""
    titulo = "Editar Slider"
    accion = "Editar"
    slider_obj = get_object_or_404(Slider, id=pk)
    sliders = Slider.objects.filter(estado=True).order_by('-prioridad')
    
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES, instance=slider_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡Slider "{slider_obj.nombre}" editado exitosamente!')
            return redirect("sliders")
        else:
            messages.error(request, '¡Error al editar slider!')
    else:
        form = SliderForm(instance=slider_obj)
    
    context = {
        "titulo": titulo,
        "form": form,
        "sliders": sliders,
        "accion": accion
    }
    # Usar el mismo template que crear
    return render(request, "configuracion/slider.html", context)


def slider_eliminar(request, pk):
    """Vista para eliminar (desactivar) un slider"""
    slider_obj = get_object_or_404(Slider, id=pk)
    nombre = slider_obj.nombre
    
    # Cambia el estado a False (eliminación lógica)
    slider_obj.estado = False
    slider_obj.save()
    
    messages.success(request, f'¡Slider "{nombre}" eliminado exitosamente!')
    return redirect("sliders")