from django.forms import ModelForm, widgets
from comunidad.models import Usuario
from django.contrib.auth.models import Group

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
        exclude = ["estado","user"]
        widgets = {
            "fecha_registro": widgets.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
        }
        
class UsuarioEditarForm(ModelForm):
    class Meta:
        model= Usuario
        fields= "__all__"
        exclude=["estado","fecha_registro", "documento","user"]

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']       

        
        