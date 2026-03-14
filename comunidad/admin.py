from django.contrib import admin
from comunidad.models import Usuario, Tienda, Resena

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Tienda)

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('puntuacion', 'comentario_truncado', 'fecha', 'eliminar_rapido')
    list_filter = ('puntuacion', 'fecha')
    search_fields = ('comentario',)
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)
    
    def comentario_truncado(self, obj):
        return obj.comentario[:50] + "..." if len(obj.comentario) > 50 else obj.comentario
    comentario_truncado.short_description = 'Comentario'
    
    def eliminar_rapido(self, obj):
        return f'<a href="/admin/comunidad/resena/{obj.id}/delete/" class="button">🗑️ Eliminar</a>'
    eliminar_rapido.allow_tags = True
    eliminar_rapido.short_description = 'Acción'