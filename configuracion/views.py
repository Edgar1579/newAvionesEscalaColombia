from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from configuracion.models import Slider
from configuracion.forms import SliderForm


def slider(request):
    titulo = "Slider"
    accion = "Agregar"
    sliders = Slider.objects.filter(estado=True).order_by('-prioridad')

    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo = form.save()
            messages.success(request, f'Slider "{nuevo.nombre}" agregado.')
            return redirect("sliders")
    else:
        form = SliderForm()

    return render(request, "configuracion/slider.html", {
        "titulo": titulo,
        "accion": accion,
        "sliders": sliders,
        "form": form,
    })


def slider_editar(request, pk):
    slider_obj = get_object_or_404(Slider, id=pk)
    sliders = Slider.objects.filter(estado=True).order_by('-prioridad')

    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES, instance=slider_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Slider "{slider_obj.nombre}" actualizado.')
            return redirect("sliders")
    else:
        form = SliderForm(instance=slider_obj)

    return render(request, "configuracion/slider.html", {
        "titulo": "Editar Slider",
        "accion": "Editar",
        "sliders": sliders,
        "form": form,
    })


@require_POST
def slider_eliminar(request, pk):
    slider_obj = get_object_or_404(Slider, id=pk)
    slider_obj.estado = False
    slider_obj.save()
    messages.success(request, f'Slider "{slider_obj.nombre}" eliminado.')
    return redirect("sliders")
