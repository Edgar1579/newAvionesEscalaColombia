from django.db import models
from django.utils.translation import gettext_lazy as _

def get_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.documento}.{ext}"
    return f"comunidad/usuarios/{filename}"
# Create your models here.
class Usuario(models.Model):
    primer_nombre = models.CharField(max_length=45, verbose_name="Primer Nombre")
    segundo_nombre = models.CharField(max_length=45, verbose_name="Segundo Nombre", blank=True, null=True)
    primer_apellido = models.CharField(max_length=45, verbose_name="Primer Apellido")
    segundo_apellido = models.CharField(max_length=45, verbose_name="Segundo Apellido")
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    imagen = models.ImageField(upload_to=get_image_filename, blank=True, null=True,default="comunidad\default-user.jpeg")
    fecha_registro= models.DateField(verbose_name="Fecha de Registro")
    class Rol(models.TextChoices):
        ADMINISTRADOR = "AD", _("Administrador")
        CLIENTES = "CL", _("Cliente")
        EMPLEADOS = "EM", _("Empleado")
    rol=models.CharField(max_length=2,choices=Rol.choices,default=Rol.CLIENTES,verbose_name="Rol")

    class TipoDocumento(models.TextChoices):
            CEDULA = 'CC', _("Cédula")
            CEDULA_EXTRANJERIA = 'CE', _("Cédula de Extrangería")

    tipo_documento = models.CharField(max_length=2, choices=TipoDocumento.choices, verbose_name="Tipo de Documento")
    documento = models.PositiveIntegerField(verbose_name="Documento", unique=True)        
    estado=models.BooleanField(default=True)
    def clean(self):
            self.primer_nombre = self.primer_nombre.title() 

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"
    class Meta:
        verbose_name_plural = "Usuarios"
        
    @property
    def full_name(self):
        if self.segundo_nombre:
            return f"{self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido}"
        else:
            return f"{self.primer_nombre} {self.primer_apellido} {self.segundo_apellido}"      
    