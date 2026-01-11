from django import forms
from django.forms.widgets import Input
from .models import Producto, ImagenProducto


class MultipleFileInput(Input):
    """Widget personalizado para permitir múltiples archivos"""
    input_type = 'file'
    needs_multipart_form = True
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['multiple'] = 'multiple'
        super().__init__(attrs)
    
    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)


class MultipleFileField(forms.FileField):
    """Campo personalizado para permitir múltiples archivos"""
    widget = MultipleFileInput
    
    def clean(self, data, initial=None):
        # Si no hay datos, retornar lista vacía
        if not data:
            return []
        
        # Si es una lista, limpiar cada archivo
        if isinstance(data, list):
            return [super(MultipleFileField, self).clean(f, initial) for f in data if f]
        
        # Si es un solo archivo, retornar como lista
        return [super(MultipleFileField, self).clean(data, initial)]


class ProductoForm(forms.ModelForm):
    # Campo para subir múltiples imágenes adicionales
    imagenes_adicionales = MultipleFileField(
        required=False,
        label='Imágenes adicionales de la galería',
        help_text='Puedes seleccionar múltiples imágenes (Ctrl+Click o Cmd+Click)',
        widget=MultipleFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen', 'precio', 'tienda', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'tienda': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del producto'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductoEditarForm(forms.ModelForm):
    # Campo para subir múltiples imágenes adicionales
    imagenes_adicionales = MultipleFileField(
        required=False,
        label='Agregar más imágenes a la galería',
        help_text='Puedes seleccionar múltiples imágenes (Ctrl+Click o Cmd+Click)',
        widget=MultipleFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen', 'precio', 'tienda', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'tienda': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del producto'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenProducto
        fields = ['imagen', 'orden', 'descripcion']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción opcional'}),
        }