from django.contrib import admin
from .models import Maquina, Apontamento

class ApontamentoInline(admin.StackedInline):
    model = Apontamento
    extra = 0
    can_delete = False
    verbose_name = "Progresso de Produção"
    
    # Organizamos os campos em grupos visuais (fieldsets)
    fieldsets = (
        ('Comum a todos', {
            'fields': ('ade_nr12', 'vistoria_final')
        }),
        ('Específico: Dobradeira', {
            'fields': ('dob_start_eletrico', 'dob_regulagem', 'dob_teste_dobra'),
            'classes': ('group-especifico-dobradeira',),
            'description': "Preencher apenas se for Dobradeira"
        }),
        ('Específico: Laser', {
            'fields': (
                'las_nivelamento', 'las_montagem_cabecote', 'las_posicionamento_perif',
                'las_passagem_fibra', 'las_montagem_cab_elet', 'las_alimentacao',
                'las_alin_cabecote', 'las_alin_bico', 'las_testes_corte'
            ),
            'classes': ('group-especifico-laser',),
            'description': "Preencher apenas se for Laser"
        }),
    )

@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    # O que aparece na lista principal
    list_display = ('matricula_br', 'cliente', 'tipo', 'data_entrega', 'get_progresso')
    list_filter = ('tipo', 'data_entrega')
    search_fields = ('matricula_br', 'cliente')
    
    # Inclui o formulário de apontamento dentro da tela da máquina
    inlines = [ApontamentoInline]

    def get_queryset(self, request):
        # O prefetch_related carrega os apontamentos de uma só vez na memória
        return super().get_queryset(request).prefetch_related('apontamento')

    def get_progresso(self, obj):
        ultimo = obj.apontamento.last()
        # Mostra o totalizador direto na lista de máquinas
        if ultimo:
            return f"{ultimo.total_geral:.1f}%"
        return "0%"
    
        # if hasattr(obj, 'apontamento'):
        #     return f"{obj.apontamento.total_geral:.1f}%"
        # return "0%"
    
    get_progresso.short_description = 'Progresso Total'

    # Isso injeta o JavaScript na página do Admin da Máquina
    class Media:
        js = ('js/admin_filter.js',)