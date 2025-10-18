from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from comunidad.forms import UsuarioForm, UsuarioEditarForm, GroupForm
from comunidad.models import Usuario
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from PIL import Image

# Create your views here.
def usuario_crear(request):
    titulo="Usuario"
    accion="Agregar"
    usuarios=Usuario.objects.all()
    if request.method == "POST":
        form=UsuarioForm(request.POST,request.FILES)
        if form.is_valid():
            if not User.objects.filter(username=request.POST['documento']):
                user = User.objects.create_user('nombre','email@email','pass')
                user.username= request.POST['documento']
                user.first_name= request.POST['primer_nombre']
                user.last_name= request.POST['primer_apellido']
                user.email= request.POST['correo']
                user.password=make_password("@" + request.POST['primer_nombre'][0] + request.POST['primer_apellido'][0] + request.POST['documento'][-4:])
                user.save()
            else:
                user= User.objects.get(username=request.POST['documento'])
                
            usuario = Usuario.objects.create(
                primer_nombre=request.POST['primer_nombre'],
                segundo_nombre=request.POST['segundo_nombre'],
                primer_apellido=request.POST['primer_apellido'],
                segundo_apellido=request.POST['segundo_apellido'],
                fecha_registro=request.POST['fecha_registro'],
                imagen=request.FILES.get('imagen'),  # Asume que tu formulario maneja archivos
                correo=request.POST['correo'],
                tipo_documento=request.POST['tipo_documento'],
                documento=request.POST['documento'],
                user=user,
                rol=request.POST['rol'],                
            )
            messages.success(request, f'¡El Usuario se agregó de forma exitosa!')    
            return redirect('usuarios')
            """ if usuario.imagen:
                 img = Image.open(usuario.imagen.path)
                 img= img.resize((500,500))
                 img.save(usuario.imagen.path)
            usuario.save() """
            
            
        else:
            ##agregar mensaje error
            messages.success(request, f'¡Error al agregar al Usuario!')
            
    else:
        form=UsuarioForm()
    context={ 
        "titulo":titulo,
        "usuarios":usuarios,
        "form":form,
        "accion":accion,
    }
    return render(request,"comunidad/usuarios/usuarios.html",context)

def usuario_editar(request,pk):
    usuario=Usuario.objects.get(id=pk)
    usuarios=Usuario.objects.all()
    accion="Editar"
    nombre=f"{usuario.primer_nombre} {usuario.primer_apellido}"
    titulo=f"Usuario {nombre}"
    
    if request.method == "POST":
        form=UsuarioEditarForm(request.POST,request.FILES, instance=usuario)
        if form.is_valid():
            usuario=form.save()
            if usuario.imagen:
                img = Image.open(usuario.imagen.path)
                img= img.resize((500,500))
                img.save(usuario.imagen.path)
            usuario.save()
            messages.success(request, f'¡{nombre} se editó de forma exitosa!')
            return redirect('usuarios')
        else:
            ##agregar mensaje error
            messages.error(request, f'¡Error al editar a {nombre}!')
            
            
    else:
            form=UsuarioEditarForm(instance=usuario)
    context={ 
        "titulo":titulo,
        "usuarios":usuarios,
        "form":form,
        "accion":accion,
    }
    return render(request,"comunidad/usuarios/usuarios.html",context) 
def usuario_eliminar(request,pk):
    usuario=Usuario.objects.filter(id=pk)
    usuario.update(estado=False)
    
    ## Agregar mensaje de exito
    return redirect('usuarios')

def edit_group(request, group_id=None):
    groups = Group.objects.all()
    if group_id:
        group = get_object_or_404(Group, id=group_id)
    else:
        group = None

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('edit_group')  # Cambia 'list_groups' por el nombre de la URL donde se listan los grupos
    else:
        form = GroupForm(instance=group)
    context={
    'groups':groups,
    'group': group,
    'form': form
    }
    return render(request, 'comunidad/usuarios/grupos.html', context)