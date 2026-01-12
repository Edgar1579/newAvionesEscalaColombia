from django import forms
from django.forms import ModelChoiceField, ModelForm, widgets
from comunidad.models import Usuario, Tienda
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple 

# forms.py
from django import forms
from .models import Usuario
from django.contrib.auth.models import Group

class UsuarioForm(forms.ModelForm):
    rol = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Rol/Grupo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Usuario
        fields = [
            'primer_nombre', 
            'segundo_nombre', 
            'primer_apellido', 
            'segundo_apellido',
            'correo',
            'telefono',
            'tipo_documento',
            'documento',
            'fecha_registro',
            'imagen'
        ]
        widgets={
            'fecha_registro':widgets.DateInput(attrs={'type':'date'},format='%Y-%m-%d')
        }# ← NO incluyas 'rol' aquí porque no existe en el modelo Usuario
        
class UsuarioEditarForm(ModelForm):
    rol= ModelChoiceField(
    queryset=Group.objects.all(), 
    label="Rol",
    )
    class Meta:
        model= Usuario
        fields= "__all__"
        exclude=["estado","fecha_registro", "documento","user"]

class GroupForm(ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=FilteredSelectMultiple('Permissions', False),
        required=False,
    )
    class Meta:
        model = Group
        fields = ['name','permissions']       

class TiendaForm(ModelForm):
    class Meta:
        model= Tienda
        fields= "__all__"
        exclude=["estado",]
        # widgets = {
        # "usuario": UsuarioWidget,
        # }

class TiendaEditarForm(ModelForm):
    class Meta:
        model= Tienda
        fields= "__all__"
        exclude=["estado",]        
        