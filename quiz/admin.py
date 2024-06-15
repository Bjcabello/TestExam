from django.contrib import admin
from .models import Pregunta, Opcion, Resultado

# Register your models here.

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 1

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto',)
    inlines = [OpcionInline]

class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pregunta', 'opcion_seleccionada', 'es_correcta')
    list_filter = ('usuario', 'es_correcta')
    search_fields = ('usuario__username', 'pregunta__texto', 'opcion_seleccionada__texto')

admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Resultado, ResultadoAdmin)
